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


from fq import FileQueue
import glob
from gpiozero import DigitalOutputDevice
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from threading import Thread, Lock
import os
from systemd.journal import JournalHandler
import time

# Temperature in C
ON_TEMP = 27
OFF_TEMP = 21
fan_logger = logging.getLogger('fans')
fan_logger.addHandler(JournalHandler())
fan_logger.setLevel(logging.INFO)

def init_fans():
    global fans
    global flag
    global fq
    flag = False
    lock = Lock()
    fq = FileQueue('/opt/speedcam/case_temp.q', 576)
    fans = DigitalOutputDevice(17, active_high=True, initial_value=False)
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    return lock

def run_fans(lock):
    try:
        global flag
        lock.acquire()
        with open(glob.glob('/sys/bus/w1/devices/28*')[0] + '/temperature', 'r') as file:
            temp = file.readline()
        lock.release()
        if len(temp) > 0:
            temp = float(temp) / 1000
            if temp is None:
                print('Case fan temp value was None.')
            if temp > ON_TEMP and flag == False:
                fans.on()
                flag = True
                fan_logger.info(f'Fans: ON ({int(temp)}C)')
            elif temp < OFF_TEMP and flag == True:
                fans.off()
                flag = False
                fan_logger.info(f'Fans: OFF({int(temp)}C)')
    except ValueError as e:
        fan_logger.warning(f'{e}')
    except Exception:
        fan_logger.warning('Case fan exception.')

def on():
    global flag
    fans.on()
    flag = True

def off():
    global flag
    fans.off()
    flag = False

def get_temp(lock):
    while True:
        try:
            lock.acquire()
            with open(glob.glob('/sys/bus/w1/devices/28*')[0] + '/temperature', 'r') as file:
                    t = file.readline()
            lock.release()
            t = float(t) / 1000
            fan_logger.info(f'Current temperature: {int(t)}')

            with open('/opt/speedcam/case_temp.q', 'a') as file:
                current_time = datetime.now().strftime('%H:%M')
                fq.push(f'{current_time} {int(t)}\n')

            time.sleep(300)
        except ValueError as e:
            fan_logger.warning(f'{e}')
            continue

if __name__ == "__main__":
        fq = FileQueue('/opt/speedcam/case_temp.q', 576)
        lock = init_fans()
        get_temp_thread = Thread(target=get_temp, args=(lock,), daemon=True)
        get_temp_thread.start()
        while True:
            try:
                run_fans(lock)
                time.sleep(60)
            except Exception:
                fan_logger.exception(f'General exception has occured in the main loop.')
                continue
        
