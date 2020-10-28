#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    2020-01-26
# Version:  2.0
# Language:	English
# Homepage: http://custom-build-robots.com

# Program for the introduction to programming with several 
# threads. It reads different sensors of the Raspberry Pi 
# Sense HAT with two threads.

import time, smbus, os
from threading import Thread
from sense_hat import SenseHat

# Initialize variables
x = 0
y = 0
z = 0
pressure = 0
temp = 0
humidity = 0

# Stop time after which the program should end
global time_stopp

# This function reads the x, y and z values of the 
# gyroscope of the Sense HAT and transfers the measured 
# values to the global variables x, y and z of the same name.
def gyroscope():
# Definition of the variables x, y and z as global variables.
   global x
   global y
   global z

   # A "sense" object is created by the class "SenseHat()" to 
   # access the sensors of the Sense HAT.
   sense = SenseHat()

   # Activate the gyroscope sensor of the Sense HAT
   sense.set_imu_config(False, True, False)

   # This endless loop reads out the x, y and z values of the 
   # Sense HAT every 0.05 seconds. Since this function is started 
   # as a thread, the global variables x, y and z always contain 
   # the new measured values.
   while time_stopp > time.time():
      # Get the x,y and z axis from the array
      x = sense.get_orientation()['pitch']
      y = sense.get_orientation()['roll']
      z = sense.get_orientation()['yaw']

      # a short pause of 0.05 seconds
      time.sleep(0.05)

      # Calls the function print_all(), which updates the display
      # of the values.
      print_all()

# Reading the compass of the Sense HAT
def environment():
   # Definition of the Variablen pressure, temp und humidity
   # as globale variables
   global pressure
   global temp
   global humidity

   sense = SenseHat()

   # This endless loop reads the pressure, temp and humidity values
   # every 0.5 seconds. Since this function is started as a thread, 
   # the global variables pressure, temp and humidity always contain 
   # the new measured values.
   while time_stopp > time.time():
      humidity = sense.get_humidity()
      temp = sense.get_temperature()
      pressure = sense.get_pressure()

      # a short pause of 0.05 seconds
      time.sleep(0.5)

      # Calls the function print_all(), which updates the display
      # of the values.
      print_all()

# Output the values in the terminal window with the function 
# print_all(), which is called every 0.05 seconds or 0.5 seconds
# per thread. So you can clearly see the different running times 
# of the threads and that they are executed in parallel.
def print_all():
   global x
   global y
   global z  
   global pressure
   global temp
   global humidity
   global time_stopp
   os.system('clear')
   
   print "############################################"
   print "############# Thread 1 #####################"
   print "#####     Update every 0.5 seconds     #####"
   print "############################################"
   print "--------------------------------------------"
   print("Temperatur:   %s C" % round(temp,2))      
   print("Air pressure: %s Millibar" % round(pressure,2))
   print("Air humidity: %s %%rH" % round(humidity,2))
   print "--------------------------------------------"
   print "############################################"
   print "############# Thread 2 #####################"
   print "#####     Update every 0.05 seconds     ####"
   print "############################################"
   print "--------------------------------------------"
   print "Pitch: ",x
   print "Roll:  ",y
   print "Yaw:   ",z
   print "--------------------------------------------"
   print "############################################"
   print "###########   remaining runtime   ##########"
   print "############################################"
   print "--------------------------------------------"
   print "Time: ",round(time_stopp - time.time(),1)," s"
   print "--------------------------------------------"

# Querying the program runtime from the user
laufzeit=input("Enter time in minutes until emergency stop active: ")
time_stopp = laufzeit*60 + time.time()

# Initialize the threads gyroscope and compass.  With e.g. 
# target=gyroscope the function gyroscope is executed by the 
# thread t_ gyroscope.
t_gyroscope = Thread(target=gyroscope)
t_environment = Thread(target=environment)

# Starting the two threads gyroscope and compass. Calling the
# method start() calls the method run() again.
t_gyroscope.start()
t_environment.start()

# With the method join() the main program waits until all threads are 
# finished. Because of the endless loops in the two functions, however, 
# the threads never come to an end - and thus the main program does not.
t_gyroscope.join()
t_environment.join()
# End of the program