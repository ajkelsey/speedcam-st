#! /bin/python

'''
    SpeedcamST: A do-it-yourself speed camera.
    Copyright (C) 2024  Andrew Kelsey [ajkelsey@grandroyal.org]

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''


from gpiozero import DigitalOutputDevice
import os
import time

def init():
    global pin22
    global pin27
    pin27 = DigitalOutputDevice(27, active_high=True, initial_value=False)
    pin22 = DigitalOutputDevice(22, active_high=True, initial_value=False)
    os.system('modprobe w1-gpio')

# IR filter
def on():
    pin27.off()
    pin22.on()
    time.sleep(1)

# No IR filter
def off():
    pin22.off()
    pin27.on()
    time.sleep(1)

if __name__ == '__main__':
    init()
    while True:
        choice = input('Enter choice: ')
        if choice == '0':
            off()
        elif choice == '1':
            on()
    