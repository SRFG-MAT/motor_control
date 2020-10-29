#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    2020-01-26
# Version:  2.1
# Language:	English
# Homepage: http://custom-build-robots.com

# This program accesses the magnetometer of the Raspberry Pi Sense HAT
# and displays the north deviation in degrees.

import sys, tty, termios, os, time

# The Python class "SenseHat" is imported.
from sense_hat import SenseHat

# Here the variable degree is set initial to avoid an error in the 
# output of the variable if it is empty.
degree = 0

# A "sense" object is created by the class "SenseHat()" to access 
# the sensors of the Sense HAT.
sense = SenseHat()

# Now the sensor magnetometer is activated.
sense.set_imu_config(True, False, False)  

# This variable determines by how many degrees the north direction 
# of the Sense HAT deviates from the front of the robot car.
s_h_direction = 180

# The variable new_degree is initially passed the value degree.
# It is used to store the new calculated north direction of the 
# robot car in case of a possible deviation from s_h_direction.
new_degree = 0

# The endless loop reads the Magenetometer until the user types 
# Ctrl+C in the terminal window.
try:
   while True:
        # The number of degrees to the north is read out.
        north = sense.get_compass()

        # The degree number should be displayed as a float value.
        degree = float(north)

        # Depending on the orientation of the Sense HAT on the robot 
        # car, the north direction must be corrected. In this example, 
        # the north direction of the Sense HAT points to the rear of 
        # the robot car.
        new_degree = degree
        if degree <= s_h_direction and s_h_direction != 0:
            new_degree = degree + s_h_direction
        else:
            new_degree = degree - s_h_direction

        # The screen content is deleted per loop pass.
        os.system('clear')

        # The measured values are displayed in the terminal window.
        print("Orientation with the compass:")
        print("North direction: %s" % round(new_degree,1))

        # A sleep phase of 0.1 seconds is inserted so that the loop 
        # runs in a controlled manner.
        time.sleep(0.1)

# If the user presses Ctrl+C in the terminal window, the program is 
# terminated and the magnetometer sensor is released.
except KeyboardInterrupt:
   sense.set_imu_config(False, False, False)
# End of the program