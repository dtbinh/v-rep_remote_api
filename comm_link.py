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
import time
import utils.vrep_pad
import numpy

print ('Program started')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    print ('Connected to remote API server')
    gpad = utils.vrep_pad.XBOX360()
else:
    print('Connection Failure')
    sys.exit('Abort Connection')

    
# Object handle                                  
errorFlag, Quadbase = vrep.simxGetObjectHandle(clientID,
                                               'Quadricopter_base',
                                               vrep.simx_opmode_oneshot_wait)
errorFlag, Quadobj = vrep.simxGetObjectHandle(clientID,
                                              'Quadricopter',
                                              vrep.simx_opmode_oneshot_wait)                                                                                                  
t = time.time()

## reset
#resetFlag = vrep.simxRemoveModel(clientID,
#                                 Quadobj,
#                                 vrep.simx_opmode_oneshot_wait)
#resetFlag, quad = vrep.simxLoadModel(clientID,
#                                     'C:/Users/originholic/Documents/Python Scripts/RL/vrep/QuadSim.ttm',
#                                     0,
#                                     vrep.simx_opmode_oneshot_wait)
                                             
    
errorFlag, Quadbase = vrep.simxGetObjectHandle(clientID,
                                               'Quadricopter_base',
                                               vrep.simx_opmode_oneshot_wait)
time.sleep(1)
    
while (time.time()-t)<60:
    # Code for testing...
    errorFlag, basePos = vrep.simxGetObjectPosition(clientID,
                                                    Quadbase,-1,
                                                    vrep.simx_opmode_streaming)
    errorFlag, test_data = vrep.simxGetFloatSignal(clientID,
                                                     'testPTV',
                                                     vrep.simx_opmode_streaming)                
    if errorFlag != 0 :
        print('data fetch failure')
    else:
        print('x: '+ str(test_data))                                                      
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
                                                               
print ('End of Script')                                          
