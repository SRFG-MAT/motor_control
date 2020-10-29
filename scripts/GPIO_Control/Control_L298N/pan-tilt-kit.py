#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    2020-02-02
# Version:  2.1
# Language:	English
# Homepage: http://custom-build-robots.com

# This Python program makes it possible to control a pan-tilt 
# kit with two servo motors. 

# Various Python libraries are imported whose functions are 
# needed in the program.
import sys, tty, termios, os, readchar

# Import the Adafruit PCA9685 library to drive the servo controller.
import Adafruit_PCA9685

# Initialization of the servo controller object pwm
pwm = Adafruit_PCA9685.PCA9685()

# With a frequency of 60 HZ the RC model servo motors I use work 
# very well.
pwm.set_pwm_freq(60)

# Here the starting positions for the two servo motors are defined
servo1_pwm = 480
servo2_pwm = 350

# The Min and Max values of the two servo motors are defined here.
servo1_min = 260
servo1_max = 640

servo2_min = 160
servo2_max = 640

# The variable interval defines the step size for the servo motors.
intervall = 5

# The menu that the user sees after starting the program explains 
# to him with which keys he has to control the Pan-Tilt-Kit.
print("w/s: turn up / down")
print("a/d: turn left / right")
print("x:   Exit program")

# The function getch() accepts the user's keyboard input. The 
# pressed letters are read in. They are needed to set the  
# direction and speed of the robot car.
def getch():
   ch = readchar.readchar()
   return ch

# The menu for the user when running the program.
# The menu explains which buttons are used to control the 
# Pan-Tilt-Kit and shows the PWM value of each servo motor.
def printscreen():
   # The call os.system('clear') clears the screen.
   os.system('clear')
   print("w/s: turn up / down")
   print("a/d: turn left / right")
   print("x:   Exit program")
   print("=== PWM value of the servo motors ===")
   print("PWM value servo motor 1: ", servo1_pwm)
   print("PWM value servo motor 2: ", servo2_pwm)

# This endless loop is only ended when the user presses the 
# X key. As long as the program is running, the keyboard input
# is read in via this loop.
while True:
   # The getch() functions reads the pressed key by the user and
   # stores the value in the variable char for futher processing
   char = getch()
   
   # The Pan-Tilt-Kit turns up.
   if(char == "w"):
      if servo1_max >= servo1_pwm:
         servo1_pwm = servo1_pwm + intervall
         pwm.set_pwm(3, 0, servo1_pwm)
      printscreen()

   # The Pan-Tilt-Kit turns down.
   if(char == "s"):
      if servo1_pwm >= servo1_min:
         servo1_pwm = servo1_pwm - intervall
         pwm.set_pwm(3, 0, servo1_pwm)
      printscreen()

   # The Pan-Tilt-Kit turns to the right.
   if(char == "d"):
      if servo2_pwm > servo2_min:
         servo2_pwm = servo2_pwm - intervall      
         pwm.set_pwm(2, 0, servo2_pwm)
      printscreen()
      
   # The Pan-Tilt-Kit turns to the left.
   if(char == "a"):
      if servo2_max > servo2_pwm:
         servo2_pwm = servo2_pwm + intervall          
         pwm.set_pwm(2, 0, servo2_pwm)
      printscreen()
      
   # By pressing the key "x" the endless loop for reading the 
   # keyboard inputs stopps and the program ends.
   if(char == "x"):
      print("Exit program")
      break
   
   # The variable char is cleared after each loop run to be able to 
   # read the next key pressed by the user.
   char = ""
   
# End of the program 
