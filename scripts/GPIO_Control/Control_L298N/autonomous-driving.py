#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    2020-01-26
# Version:  2.1
# Language:	English
# Homepage: http://custom-build-robots.com

# With this program the robot car can drive autonomously.

import smbus, time, os, random

# Import threads library
from threading import Thread

# The python class SenseHat is imported.
from sense_hat import SenseHat

# The program L298NHBridge.py is loaded as a module.
# import L298NHBridge as HBridge

# The program L298NHBridgePCA9685.py is loaded as a module.
import L298NHBridgePCA9685 as HBridge

# The program read_VL53L1X is loaded as a module and reads 
# out a ToF VL53L1X sensor.
import read_VL53L1X as dist_tof

# The Python class ledmatrix is imported.
import ledmatrix as matrix

# activatin the SMBus device
dev = smbus.SMBus(1)

# initiating some variables to control the program
global dist
dist = 20
global speed
speed = 0
global stopp_turn
global time_stopp

# Here the variable of the z axes of the gyroscope is set to 0. 
# This avoids a possible error in the output, if the variable  
# should be empty or initial.
z = 0            

# Rotate by a certain degree
def turn_robot(value):
   global z
   global stopp_turn
   global time_stopp
   global speed
   stopp_turn = 0
   turn_delta = 0
   turn = value
   speed = 1

   # A "sense" object is created by the class SenseHat() to access  
   # the sensors of the Sense HAT.
   sense = SenseHat()

   # Activate gyroscope sensor
   sense.set_imu_config(False, True, False)

   # As long as the variable value stop = 0, this thread works in an 
   # endless loop.
   while stopp_turn == 0:
      # Here the value for the z-axis is determined from the array.
      z = sense.get_orientation()['yaw']

      # Check in which direction the car should turn to reach the 
      # entered value the fastest. Next, the display of an arrow on 
      # the LED matrix is set according to the respective direction.
      if turn <= 180:
         if turn - z > 0:
            matrix.display_pixels("arrow")
            matrix.display_rotate(0)
            HBridge.setMotorLeft(speed)
            HBridge.setMotorRight(-speed)
         elif turn - z < 0:
            matrix.display_pixels("arrow")
            matrix.display_rotate(180)
            HBridge.setMotorLeft(-speed)
            HBridge.setMotorRight(speed)      
      elif turn > 180:
         if z - turn > 0:
            matrix.display_pixels("arrow")
            matrix.display_rotate(180)         
            HBridge.setMotorLeft(-speed)
            HBridge.setMotorRight(speed)
         elif z - turn < 0:
            matrix.display_pixels("arrow")
            matrix.display_rotate(0)         
            HBridge.setMotorLeft(speed)
            HBridge.setMotorRight(-speed)   

      # Calculation of the current deviation
      turn_delta = turn - z   

      # If the deviation from the target is only 5 degrees, the 
      # engines
      # slow down. 
      if z - 5 < turn < z + 5:
         speed = 0.8      

      # If the deviation from the target is only +-2 degrees, the 
      # motors stop 
      if z - 2 < turn < z + 2:
         stopp_turn = 1
         sense.set_imu_config(False, False, False)
         t_control = Thread(target=control)
         t_control.start()

      # The measured values are displayed in the terminal window.
      os.system('clear')      
      print("################# Turning ################")
      print("Current number of degrees of rotation: ", z)
      print("Remaining degrees to the destination:  ", turn_delta)

      print("Program shutdown in: ", time_stopp - time.time(), " sec.")
      print("Speed:               ", speed)
      time.sleep(0.02)

      # The time is calculated that the program may still be active 
      # until the robot car is stopped.
      if time_stopp < time.time():
         # Displays the program end symbol on the LED matrix
         matrix.display_pixels("finish")

         # stopping the geared motors.
         HBridge.setMotorLeft(0)
         HBridge.setMotorRight(0)

         # The endless loop is also stopped.
         stopp_turn = 1
# Main program for the control
def control():
   global stopp_control
   global z
   global time_stopp
   global dist
   global speed
   stopp_control = 0
   turn_degree = 0

   # The selected ToF Sensor at GPIO pin 23 is activated.
   dist_tof.start_sensor(23) 

   while stopp_control == 0:   
      # Here you can access the active ToF Sensor
      act_dist = dist_tof.get_distance()
      while act_dist == 0:
          act_dist = dist_tof.get_distance()    

      # convert the measured distance in mm into cm
      act_dist = act_dist / 10

      # Minimal plausibility check whether the measured 
      # distance is realistic.
      if act_dist != 0 and act_dist <= 2000:
         dist = act_dist

      if min_dist + 20 <= dist <= min_dist + 35:
         speed = 0.6
      elif min_dist + 15 <= dist <= min_dist + 20:
         speed = 0.5
      elif min_dist <= dist <= min_dist + 15:
         speed = 0.4
      elif 0 <= dist <= min_dist:
         speed = 0
         turn_degree = random.randint(90,270)

         # Stopping the geared motors
         HBridge.setMotorLeft(0)
         HBridge.setMotorRight(0)

         # Call the thread that makes the robot car turn to avoid 
         # the obstacle
         t_turn_robot = Thread(target=turn_robot, args=(turn_degree,))
         t_turn_robot.start()

         # The endless loop is also stopped.
         stopp_control = 1
      elif dist < 0:
         HBridge.setMotorLeft(0)
         HBridge.setMotorRight(0)           
      else:
         # In order for the car to start at a distance greater than 
         # 35cm + min_dist, this query sets the speed to 0.8.
         speed = 0.8

      # The speed of the motors is set.
      HBridge.setMotorLeft(speed)
      HBridge.setMotorRight(speed)      

      # The green arrow pointing forward is drawn on the LED matrix.
      matrix.display_pixels("arrow")
      matrix.display_rotate(270)   

      # Output of current information such as distance, speed and 
      # remaining program time
      os.system('clear')
      print("########### Driving ###########")
      print("Distance:          ", dist, " cm")
      print("Speed:  ", speed)
      print("Program duration: ",round(time_stopp - time.time(),1)," s")

      time.sleep(0.04)

      # The time is calculated that the program may still be active 
      # until the robot car is stopped.
      if time_stopp < time.time():
         # Displays the program end icon on the LED Matrix.
         matrix.display_pixels("finish")

         # Stopping the geared motors
         HBridge.setMotorLeft(0)
         HBridge.setMotorRight(0)

         # The endless loop is also stopped.
         stopp_control = 1

min_dist=input("Input minimum distance in cm (e.g. 10):")
laufzeit=input("Please enter the time in minutes that the robot car should drive: ")      
time_stopp = laufzeit*60 + time.time()

t_control = Thread(target=control)
t_control.start()

# End of the program