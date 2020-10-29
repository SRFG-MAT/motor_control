#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    2020-02-02
# Version:  1.0
# Language:	English
# Homepage: http://custom-build-robots.com

# This program imports the gpscalculatemodule.py and 
# tests the module for function.

# The program gps-calculate-module.py is loaded as a module.
import gpscalculatemodule as GPSCalc

# Initialization of the variables for the calculated distance 
# and for the calculated course angle
distance = 0
angle = 0

# In this section you can store your own GPS coordinates.
# START GPS Coordinates (S)
lat1 = 49.43214701785448
lon1 = 11.12244073993263

# Target GPS Coordinates (S
lat2 = 49.43029201382965
lon2 = 11.12692215680694

# Call of the module gps-calculate-module with the GPS coordinates
distance, angle = GPSCalc.calc(lat1, lon1, lat2, lon2)

print "Calculated distance:     ", round(distance,1), " m"
print "Calculated course angle: ", round(angle,1)

# End of the program