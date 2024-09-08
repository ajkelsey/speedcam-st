#!/bin/python

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

import os
from picamera2.outputs import FfmpegOutput
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import subprocess


os.system('rm /opt/speedcam/http/*.m3u8')
os.system('rm /opt/speedcam/http/*.ts')
picam = Picamera2()
config = picam.create_video_configuration(main={"size": (1080, 720)})
picam.configure(config)
encoder = H264Encoder()
output = FfmpegOutput("-f hls -hls_time 5 -hls_list_size 40 -hls_flags delete_segments -hls_allow_cache 0 /opt/speedcam/http/stream.m3u8")
picam.start_recording(encoder, output)
subprocess.run('python -m {}'.format('http.server --directory /opt/speedcam/http'), capture_output=True, shell=True, text=True)

while True:
    if KeyboardInterrupt is True:
        break
