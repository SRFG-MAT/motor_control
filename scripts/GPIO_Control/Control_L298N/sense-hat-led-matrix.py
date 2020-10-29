#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    2020-01-26
# Version:  2.1
# Language:	English
# Homepage: http://custom-build-robots.com

# This program accesses the sensors for air pressure, temperature
#  and humidity of the Raspberry Pi Sense HAT and displays the values
#  on the LED matrix of the Raspberry Pi Sense HAT.

import sys, tty, termios, os, time

# The python class SenseHat is imported.
from sense_hat import SenseHat

# The Python class ledmatrix is imported.
import ledmatrix as matrix

# A "sense" object is created by the class "SenseHat()" to access 
# the sensors of the Sense HAT.
sense = SenseHat()

try:
   while True:
      # The values for temperature, air pressure and humidity are 
      # read out of the sensor.
      temp = sense.get_temperature()
      pres = sense.get_pressure()
      humi = sense.get_humidity()

      # The values read out are rounded to one decimal place.
      temp = round(temp, 1)
      pres = round(pres, 1)
      humi = round(humi, 1)

      # The LED matrix turns green or red, depending on whether 
      # the measured temperature is within the defined valid interval.
      if temp > 20 and temp < 27:
         bg = [0, 100, 0]  # green
      else:
         bg = [100, 0, 0]  # red

      # Here in the variable "msg" the text to be displayed on the 
      # LED Matrix is composed.
      msg = "Temp=%s, Press=%s, Humi=%s"%(temp, pres, humi)

      # The individual measured values temperature, air pressure and 
      # humidity are displayed on the LED matrix in the form of a ticker.
      matrix.display_message(msg,[250,250,50],bg,0.06)
      
# If the user types Ctrl+c in the terminal window, the program is terminated 
# and the magnetometer sensor is released.
except KeyboardInterrupt:
    sense.set_imu_config(False, False, False)
# End of the program
