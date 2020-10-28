#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    2020-01-26
# Version:  2.1
# Language:	English
# Homepage: http://custom-build-robots.com

# Program for distance measurement with one Time of Flight sensor 
# in front of the robot car and one in the back of the robot car.

import smbus
import time
import subprocess
import os
import sys
import signal

# The program read_VL53L1X is loaded as a module and reads 
# out a ToF VL53L1X sensor.
import read_VL53L1X as dist_tof

# Import threads library
from threading import Thread

# The program L298NHBridge.py is loaded as a module.
# import L298NHBridge as HBridge

# The program L298NHBridgePCA9685.py is loaded as a module.
import L298NHBridgePCA9685 as HBridge

# The Python class ledmatrix is imported.
import ledmatrix as matrix

# activatin the SMBus device
dev = smbus.SMBus(1)

# initiating some variables to control the program
stopp = 0
global set_speed
set_speed = 0.0

# The letters f, r and s define the direction in which
# the robot car should move. The variable direction get
# those letters assigned.
# f = forward
# r = reverse
# s = stopp
global direction
direction = "f"

global dist
global time_stopp

# This function controls the robot car until just before the obstacle.
def move_robot():
   global stopp
   global set_speed
   
   # As long as stop = 0 this thread works in an endless loop.
   while stopp == 0:
      HBridge.setMotorLeft(set_speed)
      HBridge.setMotorRight(set_speed)
      time.sleep(0.01)            

def control():
   global stopp
   global set_speed
   global direction
   set_speed = 0

   try:
      min_dist=input("Input minimum distance in cm (z. B. 10):")
      laufzeit=input("Running time of the program in minutes: (z. B. 0.5):")   
   except ValueError: 
      sys.exit()

   # Calculate the runtime entered by the user in seconds.
   time_stopp = laufzeit*60 + time.time()

   # Shows the arrow for driving forward.
   matrix.display_pixels("arrow")
   matrix.display_rotate(90)   
      
   # This thread works in an endless loop until stop is set to 1.
   while stopp == 0:
      
   # When the runtime of the program entered by the user has expired,
   # the program is automatically terminated.
      if time_stopp < time.time():
        stopp = 1
        # stopping the geared motors
        set_speed = 0     

        # Displays the program end symbol on the LED Matrix.
        matrix.display_pixels("finish")
      
      # Reading the ToF sensor to get the last measured distance.
      
      if direction == "r":
        # The selected ToF Sensor at GPIO pin 24 is activated.
        dist_tof.start_sensor(24)  
        # Here you can access the active ToF Sensor
        act_dist = dist_tof.get_distance()
        while act_dist == 0:
            act_dist = dist_tof.get_distance()    
        # convert the measured distance in mm into cm
        act_dist = act_dist / 10        
      else:
        # The selected ToF Sensor at GPIO pin 23 is activated.
        dist_tof.start_sensor(23)  
        # HHere you can access the active ToF Sensor
        act_dist = dist_tof.get_distance()
        while act_dist == 0:
            act_dist = dist_tof.get_distance()    

        # convert the measured distance in mm into cm
        act_dist = act_dist / 10

      # Minimal plausibility check whether the measured distance is 
      # realistic.
      if act_dist != 0 and act_dist <= 2000:
         dist = act_dist

      # Control of the speed up to the obstacle in three steps. The 
      # last step directly in front of the rear obstacle stops the 
      # robot car and lets it continue driving backwards.
      if min_dist + 40 <= dist <= min_dist + 100:
         speed = 0.5
      elif min_dist + 25 <= dist <= min_dist + 40:
         speed = 0.4
      elif min_dist <= dist <= min_dist + 25:
         speed = 0.35
      elif 0 <= dist <= min_dist:
         speed = 0
         if direction == "f":
            direction = "r"

            # Stop the sensor at GPIO pin 23 (front)
            dist_tof.stop_sensor(23)

            # Shows the arrow for driving backwards.
            matrix.display_pixels("arrow")
            matrix.display_rotate(90)   
         elif direction == "r":
            direction = "f"
            # Stop the sensor at GPIO pin 24 (back)
            dist_tof.stop_sensor(24)

            # Shows the arrow for driving forward.
            matrix.display_pixels("arrow")
            matrix.display_rotate(270)               
      else:
         # This query is needed for the car to start at a distance 
         # greater than 100cm + min_dist.
         speed = 0.5
    
      # set the direction of travel for forward and backward.
      if direction == "r":
         set_speed = speed * -1
      else:
         set_speed = speed
   
      # Output of the current information.
      os.system('clear')
      if direction == "r":         
        print("rear spacing:      ", dist, " cm")
      else:
         print("Distance in front:   ", dist, " cm")
      print("Direction of travel: ", direction)
      print("Speed:               ", set_speed)
      print("Program run time:    ",round(time_stopp - time.time(),1)," s")
      time.sleep(0.04)
      
# Starting the thread that controls the motor driver.
t_move_robot = Thread(target=move_robot)
t_move_robot.start()

# Starting the main thread that determines the distance measurement and 
# control of the direction and speed of the motors.
t_control = Thread(target=control)
t_control.start()

# Both threads are merged with the function join() so that they are 
# terminated simultaneously on termination.
t_move_robot.join()
t_control.join()
# End of the program