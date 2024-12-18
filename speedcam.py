#!/bin/python

import alpr
from apscheduler.schedulers.background import BackgroundScheduler
import camera
import data
import facebook
import json
import ir_filter
import logging
from logging.handlers import RotatingFileHandler
import os
from os.path import exists
import radar
import subprocess
import sys
from threading import Thread

def get_config():
    logger.info('Intializing...')
    try:
        with open('/opt/speedcam/speedcam-config.json', mode='r') as config_file:
            config = json.load(config_file)
            logger.info('Configuration loaded.')
            logger.setLevel(config['logging_level'].upper())
    except Exception:
        logging.exception('Configuration load exception has occured.')
    return config

def init_scheduler():

    def restart():
            logger.info('Daily restart...')
            subprocess.run('sudo systemctl reboot -i', capture_output=True, shell=True, text=True)
                         
    daily_reboot_scheduler = BackgroundScheduler()
    daily_reboot_scheduler.add_job(restart, 'cron', hour=3, misfire_grace_time=None)
    daily_reboot_scheduler.start()

def start_logger():
    logger = logging.getLogger('speedlog')
    # Logging level set to a default of DEBUG on start. Updated when config file is loaded.
    logger.setLevel("DEBUG")
    logformat = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
    log_handler = RotatingFileHandler('/opt/speedcam/log/speedcam.log', maxBytes=500000, backupCount=5)
    log_handler.setFormatter(logformat)
    logger.addHandler(log_handler)
    return logger

####################################################################################################

if __name__ == '__main__':
    
    print('Initializing...')
    logger = start_logger()
    config = get_config()
    init_scheduler()

    camera.init(config)
    radar.init(config)
    ir_filter.init()
    videoq, imageq = alpr.init()

    if config['post_to_facebook'] == '1':
        facebook.init(config)
        facebook.init_scheduler(config, imageq)

    # Starts vehicle detection loop
    alpr_thread = Thread(target=alpr.detect_vehicle, args=(videoq, imageq), daemon=True)
    alpr_thread.start()
        
    print('Ready.')
    logger.info('Ready.')

    while True:
        try:
            # Checks if daylight, actuates ir cut filter, sets day flag
            if camera.is_day(config):
                is_day_flag = True
                ir_filter.on()
            else:
                is_day_flag = False
                ir_filter.off()

            vehicle, filename = radar.get_speed(config)
            
            if vehicle.speed > int(config['min_speed_report']):
                
                # States video saved for vehicles above threshold.
                logger.debug(f"{filename} saved.")

                # Logs car data in csv file.
                csv_file = data.process(vehicle)

                # Generates Facebook post if measured speed is above min_speed_report.
                if (vehicle.speed > float(config['min_speed_post'])):

                    # Loads alpr file queue with video filename.
                    if filename != 'unknown':
                        videoq.put(vehicle)
                        videoq.put(filename)
                        videoq.task_done()
                else:
                    # Removes video for vehicles below fb post threshold.
                    if exists(filename):
                        os.remove(filename)
                        logger.debug(f'{filename} removed. Speed is below min_speed_report.')
            else:
                # Removes video for vehicles below report threshold.
                if exists(filename):
                    os.remove(filename)
                    logger.debug(f'{filename} removed. Speed is below min_speed_report.')
        except KeyboardInterrupt:
            print('\nClosing...')
            logger.info('Closing...')
            radar.shutdown()
            logger.info('Radar closed.')
            camera.shutdown()
            logger.info('Camera closed.')
            logger.info('Exiting...')
            sys.exit()