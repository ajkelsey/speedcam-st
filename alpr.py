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

import cv2
import logging
import os
from os.path import exists
from persistqueue import Queue
from ultralytics import YOLO
from vehicle import Vehicle

def init():
    global alpr_logger
    global model
    alpr_logger = logging.getLogger('speedlog.alpr')
    alpr_logger.addHandler
    
    # Queue for video filenames
    videoq = Queue('/opt/speedcam/videoq', maxsize=100, chunksize=100, autosave=False)

    # Queue for image filenames
    imageq = Queue('/opt/speedcam/imageq', maxsize=100, chunksize=100, autosave=False)

    # Load model
    model = YOLO('/opt/speedcam/yolov8n.pt', task='detect')

    return videoq, imageq

# def detect_vehicle(vehicle, filename, fb_image_list, fblist_lock):
def detect_vehicle(videoq, imageq):
    
    while True:
        try:

            vehicle = videoq.get()
            filename = videoq.get()

            root_path = '/opt/speedcam'
            video_filename = f'{root_path}/video/{filename[20:]}'
            filename = filename[20:]
            image_filename = f'{root_path}/images/{filename[:-5]}.jpg'
            moving_dict = {}

            alpr_logger.debug(f'Detecting vehicle {filename}...')

            video = cv2.VideoCapture(f'{root_path}/video/{filename}')
            
            while video.isOpened():
                
                success, frame = video.read()
                
                if success is True:

                    # ### Create and apply mask. ###
                    # mask = np.zeros(frame.shape[:2], dtype='uint8')
                    # # White area to unmask
                    # pts = np.array([[0, 432], [1920, 255], [1920, 553], [1430, 650], 
                    #                 [1430, 960], [998, 1080], [0, 1080]], np.int32)
                    # pts = pts.reshape((-1, 1, 2))
                    # cv2.polylines(mask, [pts], True, 255, 3)
                    # cv2.fillPoly(mask, [pts], 255)
                    # # Apply mask
                    # masked_image = cv2.bitwise_and(frame, frame, mask=mask)

                    ### Detection ###
                    # Tracks object between frames
                    # results = model.track(masked_image, persist=True, verbose=False)
                    results = model.track(frame, persist=True, verbose=False)
                    result = results[0]

                    ### Crop vehicle ###
                    # Gets size of original image
                    orig_h, orig_w = result.orig_shape

                    # Established detection zone
                    detect_zone_l = int(orig_w / 3.5)
                    detect_zone_r = (orig_w / 2) - 300
                    detect_zone_t = orig_h / 3
                    
                    # Checks if there is a detected obj
                    if result.boxes.id is not None:
                        
                        for i in range(len(result.boxes.id)):
                            
                            # Check if object is a vehicle
                            if is_vehicle(result.boxes.cls[i]):
                                
                                # Extract vehicle box coordinates
                                x1 = int(result.boxes.xyxy[i][0])
                                y1 = int(result.boxes.xyxy[i][1])
                                x2 = int(result.boxes.xyxy[i][2])
                                y2 = int(result.boxes.xyxy[i][3])
                                
                                # Find center of box
                                xw = int(result.boxes.xywh[i][2])
                                yh = int(result.boxes.xywh[i][3])
                                x_center = x1 + (xw / 2)
                                y_center = y1 + (yh / 2)

                                # Determine if vehicle is in detection zone
                                if x_center > detect_zone_l and x_center < detect_zone_r and y_center > detect_zone_t:
                                # if x_center > detect_zone_l and x_center < detect_zone_r:
                                    
                                    # Check if vehicle is moving
                                    moving_dict, moving_bool = is_moving(moving_dict, result.boxes.id[i].item(), x_center, y_center)

                                    # Crop vehicle
                                    if moving_bool is True:

                                        cropped = frame[y1:y2, x1:x2]
                                        
                                        # Normalize image
                                        norm_width = 1024
                                        size_ratio =  norm_width / xw
                                        resized = cv2.resize(cropped, (norm_width, int(yh * size_ratio)))
                                        
                                        confidence = abs(result.boxes.conf[i] * 100)

                                        overlay(vehicle, image_filename, resized)
                                        alpr_logger.debug(f'DETECTED: {image_filename}, Confidence: {confidence}%')
                                        clean_up(video_filename)

                                        # Add data to image queue for posting
                                        imageq.put(image_filename)
                                        imageq.task_done()

                                        break

                        # Checks if detected image file exists. Breaks to main while loop if true.
                        if exists(image_filename):
                            break
                else:
                    alpr_logger.debug(f'Vehicle not detected in {video_filename}.')
                    clean_up(video_filename)
                    break
                
            videoq.task_done()

        except FileNotFoundError:
            alpr_logger.warning(f'ALPR detection could not find {filename} on read.')
        except Exception:
            alpr_logger.exception('A vehicle detection error has occured.')

def is_vehicle(obj_class):
    if obj_class == 2 or obj_class == 3 or obj_class == 5 or obj_class == 7 or obj_class == 8:
        return True
    else:
        return False
    
def is_moving(moving_dict, id, x_center, y_center):
    
    if id in moving_dict.keys():
        moving_dict[id].append([x_center, y_center])
    else:
        moving_dict[id] = [[x_center, y_center]]
    
    if len(moving_dict[id]) > 1:
        x_shift = abs(moving_dict[id][0][0] - moving_dict[id][-1][0])
        y_shift = abs(moving_dict[id][0][1] - moving_dict[id][-1][1])
        
        if x_shift >= 50 or y_shift >= 50:
            return moving_dict, True
    
    return moving_dict, False

def overlay(vehicle, image_filename, resized):
    font_scale = 0.75
    try:
        # Add top border
        final_img = cv2.copyMakeBorder(resized, 75, 0, 0, 0, cv2.BORDER_CONSTANT, None, (255, 255, 255))

        # overlay_img = cv2.imread(image_filename, cv2.IMREAD_GRAYSCALE)
        overlay_txt1 = "[" + str(vehicle.sheet_date) + " " + str(vehicle.sheet_time) + "]" + \
                       "[" + vehicle.street_name + "]" + "[" + vehicle.direction + " bound]"
        overlay_txt2 = "[" + str(vehicle.speed) + " " + str(vehicle.speed_units) + "]"
                    #    "[" + str(vehicle.plate) + "]"
        # Font base size is 30 pixels. Origin y location is (scaler * 30) + 10.
        cv2.putText(final_img, overlay_txt1, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, font_scale, 
                    (0, 0, 0), 2, cv2.LINE_4)
        cv2.putText(final_img, overlay_txt2, (400, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                    (0, 0, 0), 2, cv2.LINE_4)
        cv2.imwrite(image_filename, final_img)
    except Exception:
        alpr_logger.exception('A picture overlay exception occured.')

def clean_up(video_filename):
    try:
        os.remove(video_filename)
    except FileNotFoundError:
        alpr_logger.warning('ALPR clean_up file was not found.')

if __name__ == '__main__':
    init()
    filename = ''
    vehicle = Vehicle()
    vehicle.sheet_date = ''
    vehicle.sheet_time = ''
    vehicle.street_name = ''
    vehicle.direction = ''
    vehicle.speed = ''
    vehicle.speed_units = ''
    detect_vehicle(vehicle, filename)