#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    2020-02-02
# Version:  2.1
# Language:	English
# Homepage: http://custom-build-robots.com


# This program calculates the horizontal distance between 
# two given GPS coordinates and the course angle. To test 
# this program, you have to integrate it into another program, 
# which addresses it as a module with its functions and outputs 
# the calculated values.

from math import *

# The function calc needs the start and the target position as
# latitude and longitude coordinates. Then the distance and course
#  angle are calculated.
def calc(lat1, lon1, lat2, lon2):

   lat1 = lat1 # Start length degree 1
   lon1 = lon1 # Starting latitude 1
   lat2 = lat2 # Start length degree 2
   lon2 = lon2 # Starting latitude 2


   # First interim calculation:
   # The degree values of the start and destination coordinates are 
   # converted to radians using the Python function radians() and the 
   # call map(radians).
   lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

   # Second interim calculation:
   # According to the Haversine formula and for easier programming, an
   # intermediate calculation is carried out here in a separate step. 
   # The length- and width- radian values of the points Z and S are 
   # subtracted from each other.
   hav_lat = lat2 - lat1
   hav_lon = lon2 - lon1

   # Third interim calculation:
   # In preparation for the root calculation, the radical ra of the 
   # root is calculated separately.
   ra = sin(hav_lat/2)**2 + cos(lat1) * cos(lat2) * sin(hav_lon/2)**2

   # Fourth interim calculation:
   # The vertical angle and the root are calculated.
   v_angle = asin(sqrt(ra)) 

   # Calculation of the distance:
   # The actual distance between points S and Z is calculated in meters.
   h_distance = 2 * 6361 * v_angle * 1000

   # In the following formula the course angle is calculated.
   angle = atan2(sin(hav_lon) * cos(lat2), cos(lat1) \
   * sin(lat2) - sin(lat1) * cos(lat2) * cos(hav_lon))

   # The calculated angle is converted from radians to a degree value.
   angle = degrees(angle)

   # The two values distance and course angle are returned.
   return h_distance, angle
# Program end