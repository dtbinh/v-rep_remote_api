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
_,Quadbase=vrep.simxGetObjectHandle(clientID,'Quadricopter_base',vrep.simx_opmode_oneshot_wait)                                                                                                  

while True:
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
        time.sleep(1.0)             
                                                          
print ('EOS')
