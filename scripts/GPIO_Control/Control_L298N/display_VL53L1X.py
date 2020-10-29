#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    2020-02-02
# Version:  2.1
# Language:	English
# Homepage: http://custom-build-robots.com

# This program outputs the measured distance of a VL53L1X ToF 
# sensor on the console.

# The Python library time is imported
import time

# The program read_VL53L1X is loaded as a module and provides 
# the functions to read the distance from a ToF VL53L1X sensor.
import read_VL53L1X as dist

# The selected ToF Sensor at GPIO pin 23 is activated.
dist.start_sensor(23)

# The For loop takes 30 measurements with the addressed ToF Sensor
for x in range(30):
    # Here you can access the active ToF Sensor
    dist_mm = dist.get_distance()
    print("ToF sensor front - GPIO Pin 23:")
    print("Distance: {}mm".format(dist_mm))

# The selected ToF Sensor at GPIO pin 23 is switched inactive.
dist.stop_sensor(23)

time.sleep(0.5)
# The selected ToF Sensor at GPIO pin 24 is activated.
dist.start_sensor(24)

# The For loop takes 30 measurements with the addressed ToF Sensor
for x in range(30):
    # Here you can access the active ToF Sensor
    dist_mm = dist.get_distance()
    print("ToF sensor back - GPIO Pin 24:")
    print("Distance: {}mm".format(dist_mm))

# The selected ToF Sensor at GPIO pin 24 is switched inactive.
dist.stop_sensor(24)
# Program end