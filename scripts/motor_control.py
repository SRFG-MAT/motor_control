#!/usr/bin/env python

import ROS_Control.ROSAdapter
import RPi.GPIO as GPIO
import time
import cv2

# for 1st Motor on ENA
ENA = 33
IN1 = 35
IN2 = 37

ENB = 38
IN3 = 32
IN4 = 36


#----------------------------------------------------------
# init board, pins and signals A and B
#----------------------------------------------------------
def initBoard():

    # set pin numbers to the board's
    GPIO.setmode(GPIO.BOARD)

    # initialize EnA, In1 and In2
    GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)

    GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

#----------------------------------------------------------
# free board and cleanup
#----------------------------------------------------------
def cleanupBoard():
    GPIO.cleanup()

#----------------------------------------------------------
# enable signals A and B
#----------------------------------------------------------
def enableSignals():
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(ENB, GPIO.HIGH)

#----------------------------------------------------------
# disable signals A and B
#----------------------------------------------------------
def disableSignals():
    GPIO.output(ENA, GPIO.LOW)
    GPIO.output(ENB, GPIO.LOW)

#----------------------------------------------------------
# stop both motors
#----------------------------------------------------------
def stopAllMotors():

    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    #time.sleep(0.5) # wait min time to apply?

#----------------------------------------------------------
# drive forward
#----------------------------------------------------------
def driveForwards():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

#----------------------------------------------------------
# drive backwards
#----------------------------------------------------------
def driveBackwards():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

#----------------------------------------------------------
# drive right
#----------------------------------------------------------
def driveRight():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

#----------------------------------------------------------
# drive left
#----------------------------------------------------------
def driveLeft():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

#----------------------------------------------------------
# main function
#----------------------------------------------------------
def main():

    # enable board, signals and motors
    initBoard()
    enableSignals()
    stopAllMotors()

    while True:

	img = cv2.imread(r"/home/srfg-tank/ros_ws/src/motor_control/scripts/test_sample.jpg") # no camera stream yet
	cv2.imshow("SRFG Tank Video", img)   
        key = cv2.waitKey(1) & 0xFF     

	#----------------------------------------------------------
	# drive forwards until pressed again
	#----------------------------------------------------------
	if key == ord("w"):
            driveForwards()
	      
            while True:
		key = cv2.waitKey(1) & 0xFF 
    	        if key == ord("w"):
		    stopAllMotors()
	            break
            
	#----------------------------------------------------------
	# drive left until pressed again
	#----------------------------------------------------------
	if key == ord("a"):
            driveLeft()
            
	    while True:
		key = cv2.waitKey(1) & 0xFF 
    	        if key == ord("a"):
		    stopAllMotors()
	            break

	#----------------------------------------------------------
	# drive backwards until pressed again
	#----------------------------------------------------------
	if key == ord("s"):
            driveBackwards()
            
	    while True:
		key = cv2.waitKey(1) & 0xFF 
    	        if key == ord("s"):
		    stopAllMotors()
	            break

	#----------------------------------------------------------
	# drive right until pressed again
	#----------------------------------------------------------
	if key == ord("d"):
            driveRight()
            
	    while True:
		key = cv2.waitKey(1) & 0xFF 
    	        if key == ord("d"):
		    stopAllMotors()
	            break

	#----------------------------------------------------------
	# quit
	#----------------------------------------------------------
	if key == ord("q"):
	    break

    # disable board, signals and motors
    disableSignals()
    cleanupBoard()


#----------------------------------------------------------
# init with main
#----------------------------------------------------------
if __name__ == "__main__":
    main()



