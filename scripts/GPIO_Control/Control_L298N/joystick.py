# Released by rdb under the Unlicense (unlicense.org)
# Based on information from:
# https://www.kernel.org/doc/Documentatio ... ck-api.txt

# 20181231 modified by Ingmar Stapel, changes released under 
# the Unlicense.

import os, struct, array
from fcntl import ioctl

# The program L298NHBridge.py is loaded as a module. It provides
# the functions for the control of the H-bridge.
import L298NHBridge as HBridge

# The program L298NHBridgePCA9685 is loaded as module. It 
# provides the functions to control the H-Bridge via a PCA9685 
# servo controller. 
# import L298NHBridgePCA9685 as HBridge

# Variable definition for the speed of the left and right motors 
# of the robot car.
speedleft = 0
speedright = 0

# We'll store the states here.
axis_states = {}
button_states = {}

# These constants were borrowed from linux/input.h
axis_names = {
    0x00 : 'x',
    0x01 : 'y',
    0x02 : 'z',
    0x03 : 'rx',
    0x04 : 'ry',
    0x05 : 'rz',
    0x06 : 'trottle',
    0x07 : 'rudder',
    0x08 : 'wheel',
    0x09 : 'gas',
    0x0a : 'brake',
    0x10 : 'hat0x',
    0x11 : 'hat0y',
    0x12 : 'hat1x',
    0x13 : 'hat1y',
    0x14 : 'hat2x',
    0x15 : 'hat2y',
    0x16 : 'hat3x',
    0x17 : 'hat3y',
    0x18 : 'pressure',
    0x19 : 'distance',
    0x1a : 'tilt_x',
    0x1b : 'tilt_y',
    0x1c : 'tool_width',
    0x20 : 'volume',
    0x28 : 'misc',
}

button_names = {
    0x120 : 'trigger',
    0x121 : 'thumb',
    0x122 : 'thumb2',
    0x123 : 'top',
    0x124 : 'top2',
    0x125 : 'pinkie',
    0x126 : 'base',
    0x127 : 'base2',
    0x128 : 'base3',
    0x129 : 'base4',
    0x12a : 'base5',
    0x12b : 'base6',
    0x12f : 'dead',
    0x130 : 'a',
    0x131 : 'b',
    0x132 : 'c',
    0x133 : 'x',
    0x134 : 'y',
    0x135 : 'z',
    0x136 : 'tl',
    0x137 : 'tr',
    0x138 : 'tl2',
    0x139 : 'tr2',
    0x13a : 'select',
    0x13b : 'start',
    0x13c : 'mode',
    0x13d : 'thumbl',
    0x13e : 'thumbr',

    0x220 : 'dpad_up',
    0x221 : 'dpad_down',
    0x222 : 'dpad_left',
    0x223 : 'dpad_right',

    # XBox 360 controller uses these codes.
    0x2c0 : 'dpad_left',
    0x2c1 : 'dpad_right',
    0x2c2 : 'dpad_up',
    0x2c3 : 'dpad_down',
}

axis_map = []
button_map = []

# The menu for the user when running the program.
# The menu explains which buttons are used to control the car.
def printscreen():
    # The call os.system('clear') clears the screen.
    os.system('clear')
    buf = array.array('c', ['\0'] * 64)
    ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)    
    js_name = buf.tostring()   
    print("======= Joystick Robot control program ========")
    print('Joystick name: %s' % js_name) 
    print("===============================================")     
    print("==========           Menue           ==========")  
    print("===============================================")       
    print("Button O:   motor stop")
    print("Button X:   Exit program")
    print("===============================================")      
    print("=============    Speed display    =============")
    print("speed left motor:  ", speedleft)
    print("speed right motor: ", speedright)
    print("===============================================")      


# Open the joystick as a device.
fn = '/dev/input/js0'
jsdev = open(fn, 'rb')

# Get the name of the used joystick.
buf = array.array('c', ['\0'] * 64)
ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
js_name = buf.tostring()

# Read the numer of axes and buttons.
buf = array.array('B', [0])
ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES
num_axes = buf[0]

buf = array.array('B', [0])
ioctl(jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
num_buttons = buf[0]

# read the mapping of each axis.
buf = array.array('B', [0] * 0x40)
ioctl(jsdev, 0x80406a32, buf) # JSIOCGAXMAP

for axis in buf[:num_axes]:
    axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
    axis_map.append(axis_name)
    axis_states[axis_name] = 0.0

# Read the mapping of each button.
buf = array.array('H', [0] * 200)
ioctl(jsdev, 0x80406a34, buf) # JSIOCGBTNMAP

for btn in buf[:num_buttons]:
    btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
    button_map.append(btn_name)
    button_states[btn_name] = 0

# In the main loop the inputs on the joystick are read in as 
# well as the values for controlling the motors.
while True:
    evbuf = jsdev.read(8)
    if evbuf:
        time, value, type, number = struct.unpack('IhBB', evbuf)

# Here the buttons that were pressed are read out. For example, 
# the two buttons X and O are used to end the program or set the 
# values for the motors to zero. Here you can also read different 
# buttons to execute functions.
        if type & 0x01:
            button = button_map[number]
            if button:
                button_states[button] = value
                if button == "a" and value == 1:
                    print("The program was terminated")
                    speedleft = 0
                    speedright = 0
                    HBridge.setMotorLeft(speedleft)
                    HBridge.setMotorRight(speedright)                   
                    break
                elif button == "b" and value == 1:
                    speedleft = 0
                    speedright = 0
                    HBridge.setMotorLeft(speedleft)
                    HBridge.setMotorRight(speedright)       
                    printscreen()                  
# In the IF-queries the axes of the joystick are read out to be 
# able to set the speed of the left and right motors.
        if type & 0x02:
            axis = axis_map[number]
            if axis == "y":
                fvalue = value / 32767.0
                speedleft = round(value / 32767.0, 2) *-1
                axis_states[axis] = fvalue
                #print "%s: %.3f" % (axis, fvalue)
            elif axis == "ry":
                fvalue = value / 32767.0
                speedright = round(value / 32767.0, 2) *-1
                axis_states[axis] = fvalue
                #print "%s: %.3f" % (axis, fvalue)
            HBridge.setMotorLeft(speedleft)
            HBridge.setMotorRight(speedright)
            printscreen()
 # End of the program          