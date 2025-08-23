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

import camera
from datetime import datetime
import json
import logging
import serial
import time
from threading import Thread
from vehicle import Vehicle

radar_logger = logging.getLogger('speedlog.radar')
radar_logger.addHandler

def get_datetime():
    dt = datetime.now()
    p_date = dt.strftime('%A %B %d, %Y at %H:%M')
    f_date = dt.strftime("%Y%m%d-%H%M%S")
    s_date = dt.strftime('%Y-%m-%d')
    s_time = dt.strftime('%H:%M:%S')
    return p_date, f_date, s_date, s_time
    
def get_milli_time():
    milli_time = int(time.time() * 1000)
    return milli_time

def init(config):
    global radar
    try:
        radar = serial.Serial(config['radar']['device_path'],9600, timeout=1)
    except Exception:
        radar_logger.exception('Serial connection exception has occured.')
    radar.write("AX\n".encode('utf-8'))
    time.sleep(1)
    for key in config['radar']['settings']:
        radar.write(config['radar']['settings'][key].encode('utf-8') + "\n".encode('utf-8'))
    radar_logger.info('Radar configured.')
    # Flushes read buffer.
    radar.reset_input_buffer()
    radar.write("??".encode('utf-8'))
    radar_logger.debug('Radar settings:')
    for line in radar.readlines():
        radar_logger.debug(line.decode('utf-8')[:-2])
    radar_logger.info("Radar connection initialized.")

def read_buffer():
    if radar.in_waiting > 0:
        buffer = radar.readline().decode('utf-8')[:-2]
        json_buffer = json.loads(buffer)
        return json_buffer

def get_speed(config):
    
    p_flag = False

    vehicle = Vehicle()
    vehicle.speed_units = config['speed_units']
    vehicle.street_name = config['street_name']
    vehicle.post_date, vehicle.file_date, vehicle.sheet_date, vehicle.sheet_time = get_datetime()

    vehicle_speed = 0
    spd = [get_milli_time()]
    avg_speed = []
    filename = 'unknown'
    
    # Stays in loop while the time delta of the last measurement is < 1 second.
    while (int(get_milli_time()) - spd[0]) < 750:
        
        # Stays in loop until the serial buffer is empty.
        while radar.in_waiting > 0:
            
            # Begins video record.
            if camera.is_day(config):
                if p_flag == False:
                    filename = camera.start_video(config, vehicle.file_date)
                    p_flag = True
            
            spd = []
            spd = [None, None]
            spd[0] = get_milli_time()
            buffer = read_buffer()
            
            if "speed" in buffer:
                spd[1] = buffer['speed']
            
            # Appends spd to accumulator.
            if (spd[1] != None):
                avg_speed.append(spd)
    
    # Stop recording video
    if camera.is_day(config):
        cam_thread = Thread(target=camera.stop_video(config, filename), daemon=True)
        cam_thread.start()

    # Determines average speed.
    if len(avg_speed) > 0 and (p_flag == True):
        
        for index in range(len(avg_speed)):
            vehicle_speed += float(avg_speed[index][1])

        vehicle.speed = vehicle_speed / len(avg_speed)
        
        # Determines direction of travel and converts negative speed to positive.

        if vehicle.speed > 0:
            vehicle.direction = config['inbound']
            # Applies inbound speed correction.
            vehicle.speed = vehicle.speed + float(config['inbound_correction'])
        else:
            vehicle.direction = config['outbound']
            # Applies outbound speed correction.
            vehicle.speed = vehicle.speed - float(config['outbound_correction'])
        vehicle.speed = round(abs(vehicle.speed), 1)
        radar_logger.debug(f'Average speed: {vehicle.speed}')

    return vehicle, filename
        
def shutdown():
    radar.close()