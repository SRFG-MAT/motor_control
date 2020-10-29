#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    2020-02.02
# Version:  2.1
# Language:	English
# Homepage: http://custom-build-robots.com

# This Python program enables the display of information on 
# the LED matrix of the Raspberry Pi Sense HAT.

import time, os

# Import Sense HAT library.
from sense_hat import SenseHat

# Creater an SenseHat object sense
sense = SenseHat()

# Set the colors for the symbols on the LED display
g = [0, 255, 0]
r = [255, 0, 0]
e = [0, 0, 0]   

# Definition of the end symbol for the display on the 
# LED-Matrix
icon_finish = [
e,e,e,r,r,e,e,e,
e,e,r,e,e,r,e,e,
e,r,e,e,e,e,r,e,
r,e,e,r,r,e,e,r,
r,e,e,r,r,e,e,r,
e,r,e,e,e,e,r,e,
e,e,r,e,e,r,e,e,
e,e,e,r,r,e,e,e
]

# Definition of an arrow symbol for the display on the LED-Matrix
icon_arrow = [
e,e,e,g,g,e,e,e,
e,e,g,g,g,g,e,e,
e,g,e,g,g,e,g,e,
g,e,e,g,g,e,e,g,
e,e,e,g,g,e,e,e,
e,e,e,g,g,e,e,e,
e,e,e,g,g,e,e,e,
e,e,e,g,g,e,e,e
]   

# This functions displayes letters on the LED-Matrix
def display_letter(text,txt_colour,bg_color):
   if bg_color =="":
      bg_color = [255,255,255]
   if txt_colour =="":
      txt_colour = [0,0,0]
   # The content of the variable "text" is explicitly converted into
   # a string to avoid display errors.
   text = str(text)
   # Display of the text on the LED-Matrix
   sense.show_letter(text,text_colour=txt_colour,\
   back_colour=bg_color)
   return -1

# This functions displayes messages on the LED-Matrix
def display_message(text,txt_colour,bg_color, speed):
   if bg_color =="":
      bg_color = [255,255,255]
   if txt_colour =="":
      txt_colour = [0,0,0]
   # The content of the variable "text" is explicitly converted into
   # a string to avoid display errors.
   text = str(text)
   # Display of the messages on the LED-Matrix
   sense.show_message(text,scroll_speed=speed,\
   text_colour=txt_colour,back_colour=bg_color)
   return -1

# This functions displayes pixels on the LED-Matrix   
def display_pixels(icon):
   if icon == "arrow":
      sense.set_pixels(icon_arrow)   
   elif icon == "finish":
      sense.set_pixels(icon_finish)
   return -1

# This functions rotates the messages on the LED-Matrix   
def display_rotate(value):
   # The Sense-HAT-API only accepts angles of 0, 90, 180 and 270 
   # degrees around which the display can be rotated. 
   if value == 0:
      sense.set_rotation(value)      
   elif value == 90:
      sense.set_rotation(value)      
   elif value == 180:
      sense.set_rotation(value)   
   elif value == 270:
      sense.set_rotation(value)   
   return -1

# This functions displayes an image on the LED-Matrix   
def display_image(file_path):
   # Check if the file exists at all
   if os.path.isfile(file_path)== True:
      sense.load_image(file_path,redraw=True)      
   return -1

# This functions clears the LED-Matrix   
def display_clear():
   sense.clear(255, 255, 255)
   return -1

# Mirrors the current display on the LED Matrix vertically and 
# horizontally.  
def display_flip(flip):
   # flip vertically
   if flip == "v":
      sense.flip_v()
   # flip horizontally
   elif flip =="h":
      sense.flip_h()
   return -1       
# End of the program
