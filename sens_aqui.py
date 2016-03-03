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
import time
import numpy as np

initialCall=True

print ('VREP Simulation Program')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    print ('Connected to remote API server')
else:
    print('Connection Failure')
    sys.exit('Abort Connection')

# Object handle                                  
_,quadBase=vrep.simxGetObjectHandle(clientID,'Quadricopter_base',vrep.simx_opmode_oneshot_wait)
_,jointPole=vrep.simxGetObjectHandle(clientID,'Pole_joint',vrep.simx_opmode_oneshot_wait)                                                                                                 

while True:
    # Code for testing...
    if initialCall:
        mode = vrep.simx_opmode_streaming
        initialCall = False
    else:
        mode = vrep.simx_opmode_buffer
        
    errorFlag,jointPos=vrep.simxGetJointPosition(clientID,jointPole,mode)    
    if errorFlag == vrep.simx_return_ok:
        print(str(jointPos))
    else:
        print('Measurements Awaiting')
        time.sleep(1.0)
