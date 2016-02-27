"""test.py - integrating xinput.XInputJoystick with pygame for Windows + Xbox 360 controller

Windows Xbox 360 cannot use pygame events for the left and right trigger. The axis doesn't come through distinctly.
This alternative corrects that issue, and adds functions unique to the Xbox controller.

General approach:

1. Detect joysticks.
2. Detect Windows.
3. Detect Xbox 360 controller.
4. Set up the joystick device platform+controller option.

For non-Windows controllers use pygame's joystick.Joystick as usual.

For Xbox 360 controller on Windows use xinput.XInputJoystick:

1. Do "joystick = xinput.XInputJoystick()".
2. Do "if WINDOWS_XBOX_360: joystick.dispatch_events()" each game tick to poll the device.
3. Handle pygame events as usual.

References:
https://github.com/r4dian/Xbox-360-Controller-for-Python
http://support.xbox.com/en-US/xbox-360/accessories/controllers
"""

import xinput
import platform
import pygame
import numpy
from operator import attrgetter
from pygame.locals import *

__version__ = '1.0.0'

class quadCTRL:
    
    def  __init__(self):
        pygame.init()
        pygame.joystick.init()

        # Initialize a joystick object: grabs the first joystick
        self.max_fps = 60
        self.clock = pygame.time.Clock()
        self.right_stick = numpy.array(numpy.zeros(2), float)
        self.left_stick = numpy.array(numpy.zeros(2), float)
        #self.memos_stick = numpy.array(numpy.zeros(4), float)
        PLATFORM = platform.uname()[0].upper()
        WINDOWS_PLATFORM = PLATFORM == 'WINDOWS'
        self.WINDOWS_XBOX_360 = False
        JOYSTICK_NAME = ''
        joysticks = xinput.XInputJoystick.enumerate_devices()
        device_numbers = list(map(attrgetter('device_number'), joysticks))
        self.joystick = None
        if device_numbers:
            self.joystick = pygame.joystick.Joystick(device_numbers[0])
            JOYSTICK_NAME = self.joystick.get_name().upper()
            print('Joystick: {} using "{}" device'.format(PLATFORM, JOYSTICK_NAME))
            if 'XBOX 360' in JOYSTICK_NAME and WINDOWS_PLATFORM:
                self.WINDOWS_XBOX_360 = True
                self.joystick = xinput.XInputJoystick(device_numbers[0])
                print('Using xinput.XInputJoystick')
            else:
                # put other logic here for handling platform + device type in the event loop
                print('Using pygame joystick')
                self.joystick.init()
        else:
            print('Try default pygame joystick')
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            JOYSTICK_NAME = self.joystick.get_name()
            print('Joystick: {} using "{}" device'.format(PLATFORM, JOYSTICK_NAME))
                
    def stick_center_snap(self, value, snap=0.2):
    # Feeble attempt to compensate for calibration and loose stick.
        if value >= snap or value <= -snap:
            return value
        else:
            return 0.0
                
    def DetectAction(self):
        self.clock.tick(self.max_fps)
        if self.WINDOWS_XBOX_360:
            self.joystick.dispatch_events()                 
            for e in pygame.event.get():
                #print('event: {}'.format(pygame.event.event_name(e.type)))
                if e.type == JOYAXISMOTION:
                    #print('JOYAXISMOTION: axis {}, value {}'.format(e.axis, e.value))
                    if e.axis == 3:
                        self.right_stick[0] = self.stick_center_snap(e.value * -1)
                        #return self.right_stick 
                    elif e.axis == 4:
                        self.right_stick[1] = self.stick_center_snap(e.value * -1)
                        #return self.right_stick
                    elif e.axis == 0:
                        self.left_stick[1] = self.stick_center_snap(e.value)
                    elif e.axis == 1:
                        self.left_stick[0] = self.stick_center_snap(e.value) 
            return numpy.concatenate((self.right_stick,self.left_stick))
        else:
            for e in pygame.event.get():
                #print('event: {}'.format(pygame.event.event_name(e.type)))
                if e.type == JOYAXISMOTION:
                    #print('JOYAXISMOTION: axis {}, value {}'.format(e.axis, e.value))
                    if e.axis == 3:
                        self.right_stick[0] = self.stick_center_snap(e.value * -1)
                        #return self.right_stick 
                    elif e.axis == 2:
                        self.right_stick[1] = self.stick_center_snap(e.value * -1)
                        #return self.right_stick
                    elif e.axis == 0:
                        self.left_stick[1] = self.stick_center_snap(e.value)
                    elif e.axis == 1:
                        self.left_stick[0] = self.stick_center_snap(e.value) 
            return numpy.concatenate((self.right_stick,self.left_stick))
    def Destroyer(self):
        pygame.quit()