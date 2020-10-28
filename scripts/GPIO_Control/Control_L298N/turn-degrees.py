#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    2020-01-26
# Version:  2.1
# Language:	English
# Homepage: http://custom-build-robots.com

# The program rotates the robot car by an angle entered
# by the user.

import time, smbus, os

# Import threads library
from threading import Thread

# The python class SenseHat is imported.
from sense_hat import SenseHat

# The program L298NHBridgePCA9685.py is loaded as a module.
import L298NHBridgePCA9685 as HBridge

# The Python class ledmatrix is imported.
import ledmatrix as matrix

# Here the variable of the z axes of the gyroscope is set to 0. 
# This avoids a possible error in the output, if the variable  
# should be empty or initial. The variables turn is also set to 0
z = 0
turn = 0

# With speed the constant motor speed is defined
speed = 0.7

# turn_delta stores the number of degrees by which the robot car
# must still turn until the entered value is reached.
turn_delta = 0

# The stop variable sets the condition for the While loop.
stopp = 0

# Reading the orientation of the robot car via the  gyroscope
def gyroscope():
    # Define variables as global
    global z
    global stopp

    # A "sense" object is created by the class SenseHat() to access  
    # the sensors of the Sense HAT.
    sense = SenseHat()
    
    # Activating the gyroscope
    sense.set_imu_config(False, True, False)

   # As long as the variable value stop = 0, this thread works in an 
   # endless loop.
    while stopp == 0:   
        # Here the value for the z-axis is determined from the array.
        z = sense.get_orientation()['yaw']
        time.sleep(0.03)


# Rotate the robot car by a certain degree 
def turn_robot(value):
   global z
   global stopp
   global turn
   global turn_delta
   global speed

   # Value assigned to the variable turn which angle the robot car 
   # should turn.
   turn = value
   # Set the initial moving speed of the robot car
   speed = 0.7

   # As long as the variable value stop = 0, this thread works in an 
   # endless loop.
   while stopp == 0:
      #When the car is turned to the right, z starts at 0 and counts up 
      # to 360. When the car is turned to the left, z starts at 360 and 
      # counts down to 0.

      # Check in which direction the robot car should turn to reach the 
      # entered value the fastest.
      if turn <= 180:
         if turn - z > 0:
            # Display of the green arrow rotated by 180
            matrix.display_pixels("arrow")
            matrix.display_rotate(0)
            # If speed is positive, the motors rotate forward.
            # If speed is positive, the motors rotate backwards.
            HBridge.setMotorLeft(speed)
            HBridge.setMotorRight(-speed)
         elif turn - z < 0:
            # Display the green arrow
            matrix.display_pixels("arrow")
            matrix.display_rotate(180)
            HBridge.setMotorLeft(-speed)
            HBridge.setMotorRight(speed)      
      elif turn > 180:
         if z - turn > 0:
            # Display the green arrow 
            matrix.display_pixels("arrow")
            matrix.display_rotate(180)         
            HBridge.setMotorLeft(-speed)
            HBridge.setMotorRight(speed)
         elif z - turn < 0:
            # Display of the green arrow rotated by 180
            matrix.display_pixels("arrow")
            matrix.display_rotate(0)         
            HBridge.setMotorLeft(speed)
            HBridge.setMotorRight(-speed)         
      # Calculation of the current deviation in degrees
      turn_delta = turn - z   

      # If the deviation from the target is only +/-15 degrees, 
      # the engines slow down.
      if z - 15 < turn < z + 15:
        speed = 0.5         
      # If the deviation from the target angle is only +/-2 
      # degrees, the motors stop and the program is terminated.
      if z - 2 < turn < z + 2:
        # Display the red stopp symbol
        matrix.display_pixels("finish")
        stopp = 1
        HBridge.setMotorLeft(0)
        HBridge.setMotorRight(-0)  
      print_all()
      time.sleep(0.04)

# On the console the measured values are output, which are determined 
# per thread. 
def print_all():
   global z 
   global turn   
   global turn_delta
   global speed
   os.system('clear')

   print "############################################"
   print "######         Thread turn            ######"
   print "######   Update every 0.04 seconds    ######"   
   print "############################################"
   print "--------------------------------------------"
   print "Current number of degrees (z): ",round(z,2)
   print "Entered degree number:         ",turn
   print "Current degree number:         ",round(turn_delta,2)
   print "Current speed:                 ",speed
   print "--------------------------------------------"

# Einlesen der Gradzahl, die der Anwender eingibt
gradzahl=input("Input degrees for the rotation of the robot car: ")   

# Pruefen, ob die eingegebene Gradzahl Sinn macht. 
if gradzahl <= 0 or gradzahl >= 360:
   print "------------------------------------------------"
   print "Please enter a degree value between >0 and <360."
   print "------------------------------------------------"   
else: 
   # The threads gyroscope and compass will initialize 
   t_gyroscope = Thread(target=gyroscope)
   t_turn_robot = Thread(target=turn_robot, args=(gradzahl,))
   
   # The threads gyroscope and compass will be started 
   t_gyroscope.start()
   t_turn_robot.start()

   t_gyroscope.join()
   t_turn_robot.join()
# End of the program 
