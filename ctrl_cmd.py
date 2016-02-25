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

initialCall=True

print ('VREP Simulation Program')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    print ('Connected to remote API server')
    joystick = quadCTRL()
else:
    print('Connection Failure')
    sys.exit('Abort Connection')
    
while True:
    try:
        demands = joystick.DetectAction()
        #demands = RescaleInputs(gpCmd)
        print("R: " + str(demands[0]) + " " +str(demands[1]) + " " + 
              "L: " + str(demands[2]) + " " +str(demands[3]))           
    except KeyboardInterrupt:
        print "Oops! Something wrong.  Try again..."
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

print('EOS')