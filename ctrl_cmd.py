# -*- coding: utf-8 -*-
try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')
import sys
import os
import numpy as np
from utils.quadpad import quadCTRL
from utils.fmu import FMU
from utils.geometry import rotate

initialCall=True

print ('VREP Simulation Program')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    print ('Connected to remote API server')
    joystick = quadCTRL()
    fmu = FMU()
else:
    print('Connection Failure')
    sys.exit('Abort Connection')
    
while True:
    try:
        # Code for testing...
        if initialCall:
            mode = vrep.simx_opmode_streaming
            initialCall = False
        else:
            mode = vrep.simx_opmode_buffer
            
        errorFlag,rawStringData=vrep.simxGetStringSignal(clientID,'rawMeasuredData',mode)    
        if errorFlag == vrep.simx_return_ok:
            rawFloatData=vrep.simxUnpackFloats(rawStringData)
            print(len(rawFloatData))
        else:
            print('Measurements Awaiting')
            
        # Convert Euler angles to pitch, roll, yaw
        rollRad, pitchRad = rotate((rawFloatData[-4],rawFloatData[-3]),rawFloatData[-2])
        pitchRad = -pitchRad
        yawRad   = -rawFloatData[-2]
    
        # Get altitude directly from position Z
        altiMeters = rawFloatData[-5]
        #print(str(altiMeters))
        
        # Poll controller
        demands = joystick.DetectAction()
        print("R: " + str(demands[0]) + " " +str(demands[1]) + " " + 
              "L: " + str(demands[2]) + " " +str(demands[3]))
    
        # Get motor thrusts from FMU model
        thrusts = fmu.getMotors((pitchRad, rollRad, yawRad), altiMeters,
                                demands, rawFloatData[-1])
        for t in range(4):
            errorFlag = vrep.simxSetFloatSignal(clientID,
                                                'thrusts'+str(t+1),
                                                thrusts[t],
                                                vrep.simx_opmode_oneshot) 
    except KeyboardInterrupt:
        print "Oops!"
        try:
            joystick.Destroyer()
            sys.exit(0)
        except SystemExit:
            os._exit(0)

print('EOS')