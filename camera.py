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

import logging
import os
from os.path import exists
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
import subprocess
import time

def init(config):
    try:
        global output
        global picam
        global camera_logger

        camera_logger = logging.getLogger('speedlog.camera')
        camera_logger.addHandler        

        picam = Picamera2()
        width = int(config['resolution_x'])
        height = int(config['resolution_y'])
        cam_config = picam.create_video_configuration(main={'size': (width, height)}, buffer_count=12)
        picam.configure(cam_config)
        encdr = H264Encoder()
        output = CircularOutput(buffersize=int(config['cam_pre_record']) * 30)
        picam.start_recording(encdr, output)
        camera_logger.info("Camera initialized.")

    except Exception:
        camera_logger.exception('Camera exception has occured.')

def start_video(config, file_date):
    if config['camera_facility'] == '1':
        filename = f'/opt/speedcam/video/{file_date}.h264'
        try:
            if exists(filename) == False:
                output.fileoutput = filename
                output.start()
        except Exception:
            camera_logger.exception('Image capture exception.')
    else:
        filename = 'unknown'
    return filename

def stop_video(config, filename):

    if config['camera_facility'] == '1':
        time.sleep(int(config['cam_post_record']))
        output.stop()

    if exists(filename):
        if os.path.getsize(filename) == 0:
            print('Video file size is 0.')
            camera_logger.warning('Video file size is 0.')
            camera_logger.warning('Restarting daemon...')
            subprocess.run('sudo systemctl reboot -i', capture_output=True, shell=True, text=True)

def shutdown():
    picam.stop_recording()