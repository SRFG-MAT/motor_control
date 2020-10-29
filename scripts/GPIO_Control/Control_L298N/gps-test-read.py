#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    2020-01-26
# Version:  2.1
# Language:	English
# Homepage: http://custom-build-robots.com

# With this program the GPS receiver can be read out.
# The read gpd koordinates will be displayed.

import os
from gps import *
import time
import subprocess
from subprocess import Popen

global process
process = None

# The counter shows the user how often an attempt was made to 
# read the coordinates.
count = 0

# The GPSD daemon is started in the background
print("Starting the gps receiver /dev/ttyACM0")
process = subprocess.Popen(["sudo", "gpsd", "-b", "/dev/ttyACM0", "-F", "/var/run/gpsd.sock", "–G"]) 
print("GPSD PID: ", process.pid)

print("The GPSD daemon was started.")
time.sleep(2)

# Create the session for accessing the receiver.
session = gps(mode=WATCH_ENABLE)

try:
   while True:
      # Wait to delay the while loop.
      time.sleep(0.5)

      # Clearing the terminal window.
      os.system('clear')

      # Output of the status line that the program is running.
      print'Reading the GPS coordinates'

      # The counter how often the gps information was read is 
      # incremented.
      count = count + 1

      # The user is informed about the read access.
      print'Counter:', count ,' read access.'
      session.next()

      # If the GPS receiver cannot find a fixed point, the user is 
      # informed.
      if session.fix.latitude == 0.0:
         print"-------------------------------------------"
         print"No GPS information was received"
         print"Has the gpsd daemon been started yet?"
         print"-------------------------------------------"
      # If GPS coordinates are received, they are output in the 
      # terminal window.
      else:
         print'------------------ GPS-Information --------------'
         print'Latitude: ' , session.fix.latitude
         print'Longitude:' , session.fix.longitude
         print'time utc: ' , session.utc
         print'fix time: ' , session.fix.time
         print'-------------------------------------------------'
# If the user types Ctrl+c in the terminal window, the program will 
# be terminated and the GPSD daemon as well.
except KeyboardInterrupt:
    print'Program finished: '

# End of the program 