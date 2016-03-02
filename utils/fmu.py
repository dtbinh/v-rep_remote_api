'''
fmu.py - Flight Management Unit class

    Copyright (C) 2014 Bipeen Acharya, Fred Gisa, and Simon D. Levy

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as 
    published by the Free Software Foundation, either version 3 of the 
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

'''

# PID parameters (I is currently unused) ==========================================

IMU_PITCH_ROLL_Kp  = .1   # original: .25
IMU_PITCH_ROLL_Kd  = .025
IMU_PITCH_ROLL_Ki  = 0

IMU_YAW_Kp 	   = .3
IMU_YAW_Kd 	   = .1
IMU_YAW_Ki    = .01

# We don't need K_d because we use first derivative
ALTITUDE_Kp        = .25
ALTITUDE_Kd        = .1

# Empirical constants  ============================================================

ROLL_DEMAND_FACTOR      = .1
PITCH_DEMAND_FACTOR     = .1
YAW_DEMAND_FACTOR       = .5

# Imports =========================================================================

from pidcontrol import Stability_PID_Controller, Yaw_PID_Controller, Hover_PID_Controller
import math

# FMU class ==================================================================

class FMU(object):

    def __init__(self):
        '''
        Creates a new Quadrotor object.
        '''  
        # Create PD controllers for pitch, roll based on angles from Inertial Measurement Unit (IMU)
        self.pitch_Stability_PID = Stability_PID_Controller(IMU_PITCH_ROLL_Kp, IMU_PITCH_ROLL_Kd, IMU_PITCH_ROLL_Ki)      
        self.roll_Stability_PID  = Stability_PID_Controller(IMU_PITCH_ROLL_Kp, IMU_PITCH_ROLL_Kd, IMU_PITCH_ROLL_Ki)

        # Special handling for yaw from IMU
        #self.yaw_IMU_PID   = Yaw_PID_Controller(IMU_YAW_Kp, IMU_YAW_Kd, IMU_YAW_Ki)
        self.yaw_IMU_PID   = Hover_PID_Controller(IMU_YAW_Kp, IMU_YAW_Kd, IMU_YAW_Ki)

        # Create PD controller for altitude-hold
        self.altitude_PID = Hover_PID_Controller(ALTITUDE_Kp, ALTITUDE_Kd)
        
        # Altitude hold z-pisition
        self.target_altitude = 0.5
        self.target_yaw = 0.0

    def getMotors(self, imuAngles, altitude, controllerInput, timestep):
        '''
        Gets motor thrusts based on current telemetry:

            imuAngles      IMU pitch, roll, yaw angles in radians
            altitude       altitude in meters
            controllInput  (pitchDemand, rollDemand, yawDemand, climbDemand, switch) 
            timestep       timestep in seconds
        '''
        # Convert flight-stick controllerInput
        pitchDemand = controllerInput[0]
        rollDemand  = controllerInput[1]
        #yawDemand   = controllerInput[2]
        yawDemand   = 0.0
        #climbDemand = controllerInput[3]
        climbDemand = 0.0

        # Compute altitude hold if we want it
        altitudeCorrection = self.altitude_PID.getCorrection(altitude, self.target_altitude, timestep)

        # PID control for pitch, roll based on angles from Inertial Measurement Unit (IMU)
        imuPitchCorrection = self.pitch_Stability_PID.getCorrection(imuAngles[0], timestep)      
        imuRollCorrection  = self.roll_Stability_PID.getCorrection(-imuAngles[1], timestep)

        # Special PID for yaw
        #yawCorrection   = self.yaw_IMU_PID.getCorrection(imuAngles[2], yawDemand, timestep)
        yawCorrection   = self.yaw_IMU_PID.getCorrection(imuAngles[2], self.target_yaw, timestep)
        
        # Overall pitch, roll correction is sum of stability and position-hold 
        pitchCorrection = imuPitchCorrection
        rollCorrection  = imuRollCorrection
        
        if altitudeCorrection != 0:
            climbDemand = 0.5 + altitudeCorrection
            
        # Overall thrust is baseline plus climb demand plus correction from PD controller
        thrust = 4*math.sqrt(math.sqrt(climbDemand)) + 2
        #print('thrust: ' + str(climbDemand) + ' ' + str(altitudeHold) + ' ' + str(altitude))
        
        # Change the thrust values depending upon the pitch, roll, yaw and climb values 
        # received from the joystick and the # quadrotor model corrections. A positive 
        # pitch value means, thrust increases for two back propellers and a negative 
        # is opposite; similarly for roll and yaw.  A positive climb value means thrust 
        # increases for all 4 propellers.

        psign = [+1, -1, -1, +1]    
        rsign = [-1, -1, +1, +1]
        ysign = [+1, -1, +1, -1]

        thrusts = [0]*4
 
        for i in range(4):
            thrusts[i] = (thrust + rsign[i]*rollDemand*ROLL_DEMAND_FACTOR \
                                 + psign[i]*pitchDemand*PITCH_DEMAND_FACTOR \
                                 + ysign[i]*yawDemand*YAW_DEMAND_FACTOR)*(1 + rsign[i]*rollCorrection + psign[i]*pitchCorrection + ysign[i]*yawCorrection) 

        return thrusts
