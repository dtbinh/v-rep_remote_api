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
from utils.quadpad import quadCTRL
#from quadstick import PS3 as Controller

initialCall=True

print ('VREP Simulation Program')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    print ('Connected to remote API server')
    joystick = quadCTRL()
    # Object handle                                  
#    _,Quadbase=vrep.simxGetObjectHandle(clientID,'Quadricopter_base',vrep.simx_opmode_oneshot_wait)                                                                                                  

else:
    print('Connection Failure')
    sys.exit('Abort Connection')
    
while True:
    # Code for testing...
    if initialCall:
        mode = vrep.simx_opmode_streaming
        initialCall = False
    else:
        mode = vrep.simx_opmode_buffer

    # Poll controller
    demands = joystick.DetectAction()
    print("R: " + str(demands[0]) + " " +str(demands[1]) + " " + 
          "L: " + str(demands[2]) + " " +str(demands[3]))
    demandString=vrep.simxPackFloats(demands)
    vrep.simxSetStringSignal(clientID,'demandstring',demandString,vrep.simx_opmode_oneshot)
            
print('EOS')