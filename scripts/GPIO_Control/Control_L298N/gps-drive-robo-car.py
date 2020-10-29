#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    2020-02.02
# Version:  2.1
# Language:	English
# Homepage: http://custom-build-robots.com

# With this program the robot car can independently approach 
# GPS coordinates.

import time, smbus, os

# Subprocess is imported to start the GPS daemon automatically
import subprocess
from subprocess import Popen

# Importing the Python math library
from math import *

# Importing the Python gps library
from gps import *

# Importing the Python thread library
from threading import Thread

# The program L298NHBridge.py is loaded as a module.
# import L298NHBridge as HBridge

# The program L298NHBridgePCA9685.py is loaded as a module.
import L298NHBridgePCA9685 as HBridge

# The python class SenseHat is imported.
from sense_hat import SenseHat

# A "sense" object is created by the class SenseHat() to access  
# the sensors of the Sense HAT.
sense = SenseHat()

# The Python class gpscalculatemodule is imported.
import gpscalculatemodule as GPSCalc

# The Python class ledmatrix is imported.
import ledmatrix as matrix

# Definition of the globalen stop variables
global stopp_gps
global stopp_print
global stopp_bearing
global time_stopp

# Definition of the globalen coordinate variables
global act_latitude
global act_longitude
global start_latitude
global start_longitude
global last_pos_latitude
global last_pos_longitude

# target coordinate variables
global target_lat
global target_lon

# Here the variable of the z axes is defined
global z

# global variables to store some information during the 
# processing of the program
global h_bearing
global distance

# global message variable
global msg

# global variable for the correction of the north orientation 
# of the Sense HAT on the robot car
global s_h_direction
s_h_direction = 180

# global process variable to start the GPS-daemon
global process
process = None

# Initial assignment of variables
act_latitude = 0
act_longitude = 0
start_latitude = 0
start_longitude = 0
last_pos_latitude = 0
last_pos_longitude = 0
z = 0
h_bearing = 0
distance = 0
msg = "start"


# The GPSD daemon is started in the background
print("The GPSD daemon is started with the USB device /dev/ttyACM0.")
process = subprocess.Popen(["sudo", "gpsd", "-b", "/dev/ttyACM0", "-F", "/var/run/gpsd.sock", "–G"]) 
print("GPSD PID: ", process.pid)

print("The GPSD daemon was started.")
time.sleep(1)

# With this function the GPS coordinates are read.
def readgps():
   # global stopp variable for the program
   global stopp_gps
   global time_stopp

   # Variables for the temporary storage of the current GPS coordinates of the 
   # robot car position
   global act_latitude
   global act_longitude

   # start position
   global start_latitude
   global start_longitude

   # variable for the last known GPS position
   global last_pos_latitude
   global last_pos_longitude

   # Variable for the course angle
   global h_bearing

   # Variable for the distance to the target
   global distance

   # Initialize variables
   start_latitude = 0
   start_longitude = 0

   # Create the GPS session so that the GPS receiver can be read out.
   session = gps(mode=WATCH_ENABLE)

   # If stop_gps has the value 1, the While loop is terminated, and 
   # thus the thread and the program end.
   stopp_gps = 0

   # count is an auxiliary variable to temporarily store the current 
   # GPS coordinates every second in the two variables 
   # last_pos_latitude and last_pos_longitude.
   count = 0

   while stopp_gps == 0:
      if time_stopp < time.time():
         stopp_gps = 1
      # Gets the current GPS information in the variable session
      session.next()

      # Only when a GPS fix is available does the program continue. 
      # Until then the program searches for a valid GPS position.
      if session.fix.latitude != 0.0 and session.fix.longitude:
         # The start GPS coordinates of the robot car are assigned
         if start_latitude == 0:
            start_latitude = session.fix.latitude
            start_longitude = session.fix.longitude
            # Initial assignment of the variables for the last known 
            # position
            last_pos_latitude = session.fix.latitude
            last_pos_longitude = session.fix.longitude
         # Save current position of the robot car
         act_latitude = session.fix.latitude
         act_longitude = session.fix.longitude

      # Every second count%10 is true.
      if count%10 == 0:
         if session.fix.latitude != 0.0 and \
         session.fix.longitude != 0.0:
            # Every 10 passes or every second the variable is updated
            #  with the last GPS position.
            last_pos_latitude = session.fix.latitude
            last_pos_longitude = session.fix.longitude
         count = 0
      count += 1
      time.sleep(0.1)

# Reading the gyroscope of the Sense HAT 
def gyroscope():
# define the variables as global
   global z
   global stopp_gyroscope
   stopp_gyroscope = 0

   # Activating the gyroscope
   sense.set_imu_config(False, True, False)

   # As long as stop = 0, this thread works in an endless loop.
   while stopp_gyroscope == 0:
      if time_stopp < time.time():
         stopp_gyroscope = 1
         sense.set_imu_config(False, False, False)

      # Reading the horizontal position of the robot car
      z = sense.get_orientation()['yaw']
      time.sleep(0.01)   

# Rotate by a certain degree
def turn_robot(value):
   global z
   global stopp_turn
   global turn
   global turn_delta
   global speed
   global stopp_gyroscope
   global msg

   # This variable determines by how many degrees the north direction of 
   # the Sense HAT deviates from the front of the robot car.
   global s_h_direction

   # The variable new_degree is initially passed the value degree. It 
   # is used to store the new calculated north direction of the robot car
   # in case of a possible deviation from s_h_direction.
   global new_degree
   new_degree = 0

   # initial rotation speed
   speed = 1

   # Presetting of variables
   turn = value
   stopp_gyroscope = 0
   stopp_turn = 0

   # Wait a short time so that the thread is also started and the gyroscope 
   # values are available.
   time.sleep(0.5)

   for i in range(5):
      # Activating and reading the values from the magnetometer.
      sense.set_imu_config(True, False, False) 
      north = sense.get_compass()
      degree = float(north)

      # Depending on the orientation of the Sense HAT on the robot car, 
      # the north direction must be corrected. In this example, the north 
      # direction of the Sense HAT points to the rear of the robot car.
      new_degree = degree
      if degree <= s_h_direction and s_h_direction != 0:
          new_degree = degree + s_h_direction
      else:
          new_degree = degree - s_h_direction

      msg = "Compass calibration in ", 5 - i, "s act. angle: "\
      ,round(new_degree,0)
      time.sleep(1)

   # Starting the thread that reads the gyroscope
   t_gyroscope = Thread(target=gyroscope)
   t_gyroscope.start()

   # As long as stop = 0, this thread works in an endless loop and
   # aligns the robot car.
   msg = "Start rotation of the robot car: "
   time.sleep(4)
   while stopp_turn == 0:
      if time_stopp < time.time():
         stopp_turn = 1      

      msg = "Current gyroscope value: ",round(z,0)

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

      # If the deviation from the target is only 
      # +/-15 degrees, the engines slow down. 
      if z - 15 < turn < z + 15:
         speed = 0.8         

      # If the deviation from the target is only 
      #  +/-2 degrees, the engines stop. 
      if z - 2 < turn < z + 2:
         matrix.display_pixels("finish")
         stopp_gyroscope = 1
         stopp_turn = 1
         HBridge.setMotorLeft(0)
         HBridge.setMotorRight(0)
         sense.set_imu_config(False, False, False)

      time.sleep(0.04)
   msg = "Rotation completed: ",round(turn_delta,0)
   time.sleep(3)   

# This function takes over the control of the robot car so 
# that it can follow GPS coordinates.
def drive_robot():
   global stopp_drive
   global act_latitude
   global act_longitude
   global start_latitude
   global start_longitude   
   global stopp_turn
   global target_lat
   global target_lon
   global msg
   global distance
   global h_bearing
   global s_h_direction
   # Initial driving speed
   speed = 1
   stopp_drive = 0
   stopp_ausrichten = 0
   distance = 0

   angle_b = 0
   angle_c = 0
   angle_d = 0

   # Here you have to store your own waypoints in the program. 
   # If you do not adjust the GPS coordinates, the robot car 
   # will drive to the Norisring in Nuremberg!

   # Here you can overwrite the target coordinate for tests. This 
   # has the advantage that when you are testing, you do not always 
   # have to enter the coordinates manually when calling the program.
   # target_lat = 48.24983124384924
   # target_lon = 11.65604102108043         

   stopp_ausrichten = 0   

   # Here the magnetometer of the Sense HAT is activated.
   sense.set_imu_config(True, False, False)        

   # Wait for the magnetometer to align itself.
   time.sleep(5)

   # The number of degrees to the north is read out.
   north = sense.get_compass()

   # Converting the degree number into a float value.
   angle_b = float(north)

   # Depending on the orientation of the Sense HAT on the robot car, 
   # the north direction must be corrected. In this example, the north 
   # direction of the Sense HAT points to the rear of the robot car.
   new_angle_b = angle_b
   if new_angle_b <= s_h_direction and s_h_direction != 0:
       new_angle_b = angle_b + s_h_direction
   else:
       new_angle_b = angle_b - s_h_direction
   angle_b = new_angle_b

   # Release all sense HAT sensors.
   sense.set_imu_config(False, False, False)
   msg = "Angle b of magnetometer:", round(angle_b,0)

   time.sleep(3)

   msg = "Next, calculate the angle to the target"
   time.sleep(3)   
   # It is calculated how large the angle to the target is. Therefore 
   # the current coordinates and the target coordinates are used for 
   # the calculation. 

   distance, angle_c = GPSCalc.calc(act_latitude, \
   act_longitude, target_lat, target_lon)
   h_bearing = round(angle_c,0)
   msg = "Angle c before calculation:", round(angle_c,0)
   time.sleep(5)   

   # Note the value range of the course angle. If it is negative, 
   # convert the angle so that the program can continue working 
   # with it.
   if angle_c < 0:
      angle_c += 360

   msg = "Angle c according to calculation:", round(angle_c,0)
   time.sleep(5)
   angle_d = angle_c

   # Transfer of the calculated angle to the print function.   
   msg = "Rotation angle of the robot car: ", round(angle_d,0)   
   time.sleep(5)

   # The robot car turns to the target coordinate.   
   turn_robot(angle_d)

   # Wait until the robot car has finished spinning. This is done
   # using the global variable stop_turn.
   while stopp_turn == 0:
      time.sleep(0.01)      

   # Transfer of the information to the print function that the 
   # robot car has finished turning 
   msg = "Fahre los zum Ziel..."
   time.sleep(2.5)   

   # From now on simply drive straight on without further checking 
   # the correct orientation of the robot car to the target until 
   # the distance to the target is < 4m.
   while stopp_ausrichten == 0:
      if time_stopp < time.time():
         stopp_ausrichten = 1
      if start_latitude != 0 and start_longitude != 0:
         distance, angle_c = GPSCalc.calc(act_latitude, \
         act_longitude, target_lat, target_lon)
         h_bearing = angle_c
         msg = "Drive to target - distance: ", round(distance,0)
      if distance < 4:
         HBridge.setMotorLeft(0)
         HBridge.setMotorRight(0)
         msg = "Distance < 4 m end of straight ahead. The target has \
            been reached: ", distance
         stopp_ausrichten = 1
      else:
         matrix.display_pixels("arrow")
         matrix.display_rotate(90)   
         HBridge.setMotorLeft(speed)
         HBridge.setMotorRight(speed)
      time.sleep(0.01)

# This function updates the text output in the terminal window 
def printdata():
   global time_stopp
   global stopp_print
   global act_latitude
   global act_longitude
   global start_latitude
   global start_longitude
   global h_bearing   
   global distance
   global msg

   stopp_print = 0
   laufzeit = 0
   while stopp_print == 0:   
      if time_stopp < time.time():
         stopp_print = 1
         HBridge.setMotorLeft(0)
         HBridge.setMotorRight(0)
      os.system('clear')
      laufzeit = time_stopp - time.time()
      print("---------------------------------------")
      print(":::::  Autonomous driving status  :::::")
      print("---------------------------------------" )  
      print("Start latitude:              ",start_latitude)
      print("Start longitude:             ",start_longitude)
      print("Actual latitude:             ",act_latitude)
      print("Actual longitude:            ",act_longitude)
      print("Horizontal angle:            ",round(h_bearing,1))
      print("Distance in m:               ",round(distance,1))
      print("Gyroscope angle z (turning): ",round(z,1))
      print("Program information:         ",msg)
      print("Programme runtime in sec:    ",round(laufzeit,1))
      time.sleep(0.5)   

# The user is prompted to select the target latitude and 
# the to enter the target longitude. 
try:
   laufzeit=input("Programmlaufzeit in Minuten eingeben: ") 
   target_lat=input("Target latitude:")
   target_lon=input("Target longitude:")
except ValueError: 
   sys.exit()

time_stopp = laufzeit*60 + time.time()
# Starting the threads that must be active for the program
t_readgps = Thread(target=readgps)
t_readgps.start()

t_print = Thread(target=printdata)
t_print.start()   

drive_robot()

# End of the program 
