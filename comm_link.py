# -*- coding: utf-8 -*-
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
import numpy as np

from quadstick import PS3 as Controller

initialCall=True

print ('VREP Simulation Program')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    print ('Connected to remote API server')
    controller = Controller(('Stabilize', 'Hold Altitude', 'Unused'))
else:
    print('Connection Failure')
    sys.exit('Abort Connection')

# Object handle                                  
_,Quadbase=vrep.simxGetObjectHandle(clientID,'Quadricopter_base',
                                    vrep.simx_opmode_oneshot_wait)                                                                                                  

while True:
    # Code for testing...
    if initialCall:
        mode = vrep.simx_opmode_streaming
        initialCall = False
    else:
        mode = vrep.simx_opmode_buffer
        
    errorFlag,rawStringData=vrep.simxGetStringSignal(clientID,'rawMeasuredData',mode)
    if errorFlag == 0:
        rawFloatData=vrep.simxUnpackFloats(rawStringData)
    else:
        print('Measurements Awaiting')             
                                                     
    # gamepad test
#    gpCmd = gpad.DetectAction()
#    demands = RescaleInputs(gpCmd)
#    print("R: " + str(gpCmd[0]) + " " +str(gpCmd[1]) + " " + 
#          "L: " + str(gpCmd[2]) + " " +str(gpCmd[3]))
#    
#    errorFlag, data_string = vrep.simxGetStringSignal(clientID,
#                                                     'data_string',
#                                                     vrep.simx_opmode_streaming)
    #print(data_string)                                                     
                                                               
print ('EOS')                                          
