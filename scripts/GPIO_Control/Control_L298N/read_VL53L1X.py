#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    2020-01-26
# Version:  2.1
# Language:	English
# Homepage: http://custom-build-robots.com

# This program reads the distance values of a VL53L1X ToF sensor. 
# When calling the VL53L1X ToF sensor, the GPIO pin to which the 
# ToF sensor is connected with its XSHUT pin must always be passed.

# Various Python classes are imported, whose functions are needed 
# for program processing.
import time

import VL53L1X

# The class RPi.GPIO is imported, which enables the control of the
# GPIO pins of the Raspberry Pi.
import RPi.GPIO as io

io.setmode(io.BCM)
io.setwarnings(False)

# Here an object tof is created with which the access via I2C bus to
# the ToF Sensor takes place.
tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)

# The sensor is set active with this function. The GPIO pin number 
# must be passed on.
def start_sensor(number):
    # The XSHUT pin is set HIGH to activate the sensor.
    io.setup(number, io.OUT)
    io.output(number, True)
    time.sleep(0.2)

    # Here you can access the ToF Sensor
    tof.open() # Initialise the i2c bus and configure the sensor
    # The measurement at the selected sensor is started. There are
    # three modes for the measurement:
    # 1 = Short Range, 
    # 2 = Medium Range, 
    # 3 = Long Range    
    tof.start_ranging(1)

# This function stops the distance measurement. The GPIO Pin
# Number must be transferred to set the ToF Sensor inactive.
def stop_sensor(number):
    # The measurement at the selected sensor is stopped.    
    tof.stop_ranging() 
    # The XSHUT pin is set LOW to disable the sensor.   
    io.output(number, False)

# The function reads out the measured distance.
def get_distance():
    distance_in_mm = 0
    distance_in_mm = tof.get_distance()
    return distance_in_mm
# Program end