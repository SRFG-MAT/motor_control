#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    2020-01-28
# Version:  2.1
# Language:	English
# Homepage: http://custom-build-robots.com

# The program reads the magnetometer and turns the robot car 
# in the direction entered by the user

import sys, tty, termios, os, time

# Import threads library
from threading import Thread

# The python class SenseHat is imported.
from sense_hat import SenseHat

# The program L298NHBridge.py is loaded as a module.
# import L298NHBridge as HBridge

# The program L298NHBridgePCA9685.py is loaded as a module.
import L298NHBridgePCA9685 as HBridge

# The Python class ledmatrix is imported.
import ledmatrix as matrix

# A "sense" object is created by the class SenseHat() to access  
# the sensors of the Sense HAT.
sense = SenseHat()

# Here the variable of the z axes of the gyroscope is set to 0. 
# This avoids a possible error in the output, if the variable  
# should be empty or initial. The variables turn and degree are 
# also set to 0
z = 0
turn = 0
degree = 0

# With speed the constant motor speed is defined
speed = 0.7

# turn_delta stores the number of degrees by which the robot car
# must still turn until the entered value is reached.
turn_delta = 0

# The stop variable sets the condition for the While loop.
stopp = 0

# Reading the orientation of the robot car to the north pole from 
# the magnetometer of the Raspberry Pi Sense HAT 
def readposition(value):
    # Define variables as global
    global degree
    degree_delta = 0
    #global x
    #global y
    global z
    global stopp
    global new_degree
    pol = value

    # This variable defines by how many degrees the north direction 
    # of the Sense HAT deviates from the front of the robot car. The 
    # value depends on the mounting of the Sense HAT on the robot car.
    s_h_direction = 180

    # The variable new_degree is initially passed the value degree. 
    # It is used to store the new calculated north direction of the 
    # robot car in case of a possible deviation from s_h_direction.
    new_degree = 0

    # For a maximum of 60 seconds or 60 times the value of the 
    # magnetometer is read out to obtain the exact orientation in the
    # direction of the north pole.    
    for i in range(60):
        # Activating the magnetometer
        sense.set_imu_config(True, False, False)  
        # The number of degrees to the north is read out.
        north = sense.get_compass()
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
            
        # Clearing the terminal window.
        os.system('clear')
        print "-----------------------------------------------"
        print "Current compass value in degrees to north: ",new_degree      
        print "Compass calibration finished in ", 60 - i, "s."
        print "-----------------------------------------------"

        # Measure the value of the magnetometer for 10 seconds. If the 
        # deviation is less than 1 after 10 seconds, the measurement is 
        # considered valid.
        if i > 10 and new_degree - new_degree < 1:
        	
        	  # Clearing the terminal window.
            os.system('clear')
            print "-------------------------------------------"
            print "Current compass value in degrees to north: ",new_degree      
            print "Calibration successful and finished."
            print "-------------------------------------------"      
            time.sleep(1)

            # Initialize the turn_robot thread to turn the robot car.
            t_turn_robot = Thread(target=turn_robot, args=(pol,))    
                 
            # Start the thread turn_robot to turn the robot car in the given
            # direction.
            t_turn_robot.start()
            break
        else:
            degree_delta = new_degree

        time.sleep(1)

# Rotate by a certain degree
def turn_robot(value):
   global z
   global stopp
   #global degree
   global turn
   global turn_delta
   global speed

   # This variable determines by how many degrees the north direction of 
   # the Sense HAT deviates from the front of the robot car.
   s_h_direction = 180

   # Point of the compass from the user input
   pol = value
   # initial rotation speed
   speed = 0.7

   # Specify the number of degrees to which the robot car must rotate to
   # point in the entered cardinal direction.
   if pol == "N":
      turn = 0
   elif pol == "E":
      turn = 90
   elif pol == "S":
      turn = 180
   elif pol == "W":
      turn = 270

   # As long as the variable value stop = 0, this thread works in an 
   # endless loop.
   while stopp == 0:
      # Activate gyroscope sensor
      sense.set_imu_config(False, True, False) 
           
      # Here the value for the z-axis is determined from the array.
      z = sense.get_orientation()['yaw']     

      # Depending on the orientation of the Sense HAT on the robot car, 
      # the north direction must be corrected. In this example, the north
      # direction of the Sense HAT points to the rear of the robot car.
      # This also has a direct effect on the yaw value of the Sense HAT,
      # which must also be corrected with 180°.
       
      if z <= s_h_direction:
          z = z + s_h_direction
      else:
          z = z - s_h_direction

      # When the robot car is turned to the right, z starts at 0 and counts
      # up to 360. When the car is turned to the left, z starts at 360 and
      # counts down to 0.

      # Check in which direction the car should turn to reach the entered 
      # value the fastest. Next, the display of an arrow on the LED matrix
      # is set according to the respective direction.
      if turn == 0:
         if z > 345:
            matrix.display_pixels("arrow")
            matrix.display_rotate(0)
            HBridge.setMotorLeft(speed)
            HBridge.setMotorRight(-speed)
         elif z <= 345:
            matrix.display_pixels("arrow")
            matrix.display_rotate(180)   
            HBridge.setMotorLeft(-speed)
            HBridge.setMotorRight(speed)
      elif turn <= 180:
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

      # If the deviation from the target is only 15 degrees, the engines
      # slow down. 
      if z - 15 < turn < z + 15:
         speed = 0.5         

      # If the deviation from the target is only +-2 degrees, the motors stop 
      if z - 2 < turn < z + 2:
         matrix.display_pixels("finish")  
         stopp = 1
         HBridge.setMotorLeft(0)
         HBridge.setMotorRight(0) 
      print_all(pol)

# Output of the measured values, which are determined per thread, on the console.
def print_all(value):
   global z 
   global turn   
   global turn_delta
   global speed
   #global degree
   global new_degree
   pol = value

   os.system('clear')

   print "############################################"
   print "############ Magnetometer ##################"
   print "#####     Update every 0.04     seconds ####"   
   print "############################################"
   print "--------------------------------------------"
   print "Entered cardinal point:    ",pol
   print "Degrees for turning (yaw): ",round(z,2)
   print "Start value in degrees:    ",round(new_degree,2)
   print "Deviation in degrees:      ",round(turn_delta,2)
   print "Current speed:             ",speed
   print "--------------------------------------------"

# Reading the compass direction entered by the user
pol=raw_input("Please enter the cardinal point N, E, S or W: ")   

# Check if the entered degree number makes sense.  
if pol=="N" or pol=="E" or pol=="S" or pol=="W":
   # Initializing the thread t_readposition with transfer of the 
   # cardinal point entered by the user 
   t_readposition = Thread(target=readposition, args=(pol,))
   
   # Starting the Thread
   t_readposition.start()
else: 
   # Error handling if N, E, S or W is not entered
   print "-----------------------------------------------------"
   print "Please enter only the cardinal point N, E, S or W:"
   print "-----------------------------------------------------"