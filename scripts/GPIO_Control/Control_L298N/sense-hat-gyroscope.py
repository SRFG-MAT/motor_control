#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    2020-01-28
# Version:  2.1
# Language:	English
# Homepage: http://custom-build-robots.com

# This program accesses the gyroscope of the Raspberry Pi Sense HAT 
# and displays the orientation of the robot car in degrees.

import sys, tty, termios, os, time

# The python class SenseHat is imported.
from sense_hat import SenseHat

# Here the variables of the three axes of the gyroscope are set to 0. 
# This avoids a possible error in the output, if the variables should 
# be empty or initial.
x = 0
y = 0
z = 0

# A "sense" object is created by the class SenseHat() to access the 
# sensors of the Sense HAT.
sense = SenseHat()

# Now the sensor gyroscope is activated.
sense.set_imu_config(False, True, False)
try:
   while True:
      # Here the values of the three axes x, y and z are read out.
      x, y, z = sense.get_orientation().values()
      
      # Clearing the terminal window.
      os.system('clear')
      
      # The measured values are displayed in the terminal window and 
      # rounded to one decimal place.
      print "Orientation with the gyroscope:"
      print "Pitch x: ",round(x,2)
      print "Roll y:  ",round(y,2)
      print "Yaw z:   ",round(z,2)
      
      # Wait to delay the while loop.
      time.sleep(0.1)
      
# If the user types Ctrl+c in the terminal window, the program will 
# be terminated and the GPSD daemon as well.
except KeyboardInterrupt:
   sense.set_imu_config(False, False, False)
   print'Program finished: '
# End of the program 
