#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    2020-02-02
# Version:  2.1
# Language:	English
# Homepage: http://custom-build-robots.com

# This program is used to log the temperature of the
# CPU into a csv file.

from gpiozero import CPUTemperature
from time import sleep, strftime, time

cpu = CPUTemperature()

def write_temp(temp):
    with open("/home/pi/cpu_temp.csv", "a") as log:
        log.write("{0}{1}\n".format(strftime("%Y-%m-%d;%H:%M:%S;"),str(temp)))

while True:
    temp = cpu.temperature
    write_temp(temp)
    sleep(1)