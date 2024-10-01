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

from apscheduler.schedulers.background import BackgroundScheduler
import json
import logging
import os
from os.path import exists
import requests
import stats
import subprocess

API_VERSION = 'v20.0'
DEFAULT_IMAGE = '/opt/speedcam/default_image.jpg'

def init(config):
    global facebook_logger
    global page_token
    facebook_logger = logging.getLogger('speedlog.facebook')
    facebook_logger.addHandler
    try:

        # Retrieves page access token. Requires integration userid, user access token.
        usr_id = config['facebook']['userid']
        usr_token = config['facebook']['user_token']
        pg_token_url = 'https://graph.facebook.com/{}/accounts?access_token={}'.format(usr_id, usr_token)
        response_dict = requests.get(pg_token_url).json()
        page_token = response_dict['data'][0]['access_token']

        if 'error' in response_dict:
            error_msg = response_dict['error']['message']
            error_code = response_dict['error']['code']
            facebook_logger.warning('Facebook initialization error has occured. Facebook Reponse: ' + 
                            '[Code: {}\tMessage: {}.]'.format(error_code, error_msg))
        else:
            facebook_logger.info('Facebook intialized.')
    except KeyError:
        facebook_logger.warning(response_dict)
    except Exception:
        facebook_logger.exception('A Facebook initialization exception has occured.')
    return 

def init_scheduler(config, imageq):
    try:

        # Schedules post of speeding vehicles every hour.
        fb_hourly_scheduler = BackgroundScheduler()
        fb_hourly_scheduler.add_job(post_images, 'interval', 
                                    args=(config, imageq), hours=1, misfire_grace_time=None)
        fb_hourly_scheduler.start()

        # Schedules speeder of the day post
        fb_speeder_of_day_scheduler = BackgroundScheduler()
        fb_speeder_of_day_scheduler.add_job(speeder_of_the_day, 'cron',
                                            args=(config['facebook']['pageid'], 
                                                  config['facebook']['page_token']), hour=1, 
                                                  misfire_grace_time=None)
        fb_speeder_of_day_scheduler.start()

        # Schedules daily speeders post
        fb_daily_speeders_scheduler = BackgroundScheduler()
        fb_daily_speeders_scheduler.add_job(daily_speeders, 'cron',
                                            args=(config['facebook']['pageid'], config['facebook']['page_token'], 
                                                  config['street_name']), hour=2, misfire_grace_time=None)
        fb_daily_speeders_scheduler.start()

    except Exception:
        facebook_logger.exception('A scheduler exception has occured.')

def post_images(config, imageq):
    
    try:
        facebook_logger.debug('Attempting to post to Facebook...')
            
        count = 0
        street = config['street_name']

        # Upload images
        PAGE_ID = config['facebook']['pageid']
        ACCESS_TOKEN = config['facebook']['page_token']
        image_ids = []
        image_url = f'https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/photos'
        image_payload = {'access_token': ACCESS_TOKEN,
                        'published': 'false',}
        
        while not imageq.empty():
            try:
                count += 1
                image_file = imageq.get()
                file = {'media': open(image_file, 'rb')}

                image_response_dict = requests.post(image_url, data=image_payload, files=file).json()
                image_ids.append(image_response_dict['id'])
            
                if 'error' in image_response_dict:
                    error_msg = image_response_dict['error']['message']
                    error_code = image_response_dict['error']['code']
                    facebook_logger.warning(f'Facebook image upload error has occured. \
                                            Facebook Response: [Code: {error_code}\tMessage: {error_msg}.]')
                else:
                    # Removes filenames from queue only if the upload is successful.
                    imageq.task_done()

            except FileNotFoundError:
                facebook_logger.warning(f'Facebook: While uploading images, {image_file} was not found.')
                continue
            except ValueError as e:
                facebook_logger.warning(f'{e}')
                continue
            except requests.exceptions.ConnectionError as e:
                facebook_logger.warning(f'Facebook connection error: {e}')
            except requests.exceptions.HTTPError as e:
                facebook_logger.warning(f'Facebook HTTP: {e}.')
            except requests.exceptions.RequestException as e:
                facebook_logger.warning(f'Facebook connection error: {e}')

        # Create POST.
        if count > 0:
            post_url = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/feed"
            payload = {'access_token': ACCESS_TOKEN, 
                    'message': f'Street: {street}\nNumber of vehicles: {count}',
                    'published': 'true',}

            for image_id in image_ids:
                payload[f'attached_media[{image_id}]'] = f'{{"media_fbid": "{image_id}"}}'
            
            # Send POST
            try:
                response_dict = requests.post(post_url, data=payload, json=payload).json()
                if 'error' in response_dict:
                    error_msg = response_dict['error']['message']
                    error_code = response_dict['error']['code']
                    facebook_logger.warning(f'Facebook post error has occured. \
                                            Facebook Response: [Code: {error_code}\tMessage: {error_msg}.]')

                facebook_logger.debug(f'Facebook post completed.')
            except requests.exceptions.ConnectionError as e:
                facebook_logger.warning(f'Facebook connection error: {e}')
            except requests.exceptions.HTTPError as e:
                facebook_logger.warning(f'Facebook HTTP: {e}.')
            except requests.exceptions.RequestException as e:
                facebook_logger.warning(f'Facebook connection error: {e}')
        else:
            facebook_logger.debug(f'Facebook: There was nothing to post.')
        
    except Exception:
        facebook_logger.exception('Facebook post exception has occured.')

def speeder_of_the_day(PAGE_ID, ACCESS_TOKEN):
    
    try:

        facebook_logger.debug(f'Attempting Speeder Of The Day post...')

        # Get stats
        yesterday, period = stats.previous_day()
        file_list = stats.get_file_list(period)
        data_df = stats.ingest_data(file_list)
        speeder, speeder_filename = stats.top_speeder(data_df)
        
        # Create post
        if exists(speeder_filename):
            post_url = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/photos"
            payload = {'access_token': ACCESS_TOKEN, 
                    'message': f'\U0001f6a8\U0001f6a8\U0001f6a8 SPEEDER OF THE DAY \U0001f6a8\U0001f6a8\U0001f6a8\n\nThe loser for {yesterday} drove {speeder} mph!',
                    'published': 'true',}
            file = {'media': open(speeder_filename, 'rb')}
        else:
            facebook_logger.debug('Attempting to post speeder of the day without image...')
            post_url = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/photos"
            payload = {'access_token': ACCESS_TOKEN, 
                    'message': f'\U0001f6a8\U0001f6a8\U0001f6a8 SPEEDER OF THE DAY \U0001f6a8\U0001f6a8\U0001f6a8\n' + 
                               f'The loser for {yesterday} drove {speeder} mph!\n\n[Photo unavailable]',
                    'published': 'true',}
            file = {'media': open(DEFAULT_IMAGE, 'rb')}
        
        # Send POST
        response_dict = requests.post(post_url, data=payload, files=file).json()

        facebook_logger.debug('Sent POST...')
        if 'error' in response_dict:
            error_msg = response_dict['error']['message']
            error_code = response_dict['error']['code']
            facebook_logger.warning(f'Speeder Of The Day post error has occured. \
                                    Facebook Response: [Code: {error_code}\tMessage: {error_msg}.]')
        print(response_dict.json())
        facebook_logger.debug(f'Speeder Of The Day post completed.')
    except requests.exceptions.ConnectionError as e:
        facebook_logger.warning(f'Speeder Of The Day connection error: {e}')
    except requests.exceptions.HTTPError as e:
        print(f'Speeder Of The Day HTTP: {e}.')
        facebook_logger.warning(f'Speeder Of The Day HTTP: {e}.')
    except requests.exceptions.RequestException as e:
        print(f'Speeder Of The Day connection error: {e}')
        facebook_logger.warning(f'Speeder Of The Day connection error: {e}')
    except FileNotFoundError:
        facebook_logger.warning(f'Speeder of the day {speeder_filename} was not found.')

def daily_speeders(PAGE_ID, ACCESS_TOKEN, street_name):
    try:

        facebook_logger.debug(f'Attempting Daily Speeders post...')

        # Create graph
        yesterday, period = stats.previous_day()
        daily_filename = f'/opt/speedcam/{period}.jpg'
        subprocess.run(f'/opt/speedcam/plot_the_plots.py -g bar -t speedbin -sb 31 36 41 46 51 -p {period}',
                        capture_output=True, shell=True, text=True)

        # Create post
        _, daily_fines = stats.daily_revenue()
        if exists(daily_filename):
            post_url = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/photos"
            payload = {'access_token': ACCESS_TOKEN, 
                    'message': f'Number of speeders on {street_name} for {yesterday}.\n\n' +
                    f'{daily_fines}',
                    'published': 'true',}
            file = {'media': open(daily_filename, 'rb')}
        else:
            return
        
        # Send POST
        response_dict = requests.post(post_url, data=payload, files=file)

        facebook_logger.debug('Sent POST...')
        if 'error' in response_dict:
            error_msg = response_dict['error']['message']
            error_code = response_dict['error']['code']
            facebook_logger.warning(f'Daily Speeders post error has occured. \
                                    Facebook Response: [Code: {error_code}\tMessage: {error_msg}.]')
        print(response_dict.json())
        facebook_logger.debug(f'Daily Speeders post completed.')

        os.remove(daily_filename)

    except requests.exceptions.ConnectionError as e:
        print(f'Daily Speeders connection error: {e}')
        facebook_logger.warning(f'Daily Speeders connection error: {e}')
    except requests.exceptions.HTTPError as e:
        print(f'Daily Speeders HTTP: {e}.')
        facebook_logger.warning(f'Daily Speeders HTTP: {e}.')
    except requests.exceptions.RequestException as e:
        print(f'Daily Speeders connection error: {e}')
        facebook_logger.warning(f'Daily Speeders connection error: {e}')
    except FileNotFoundError:
        facebook_logger.warning(f'Daily Speeders {daily_filename} was not found.')

if __name__ == '__main__':
    with open('/opt/speedcam/speedcam-config.json', mode='r') as config_file:
        config = json.load(config_file)
    init(config)
    daily_speeders(config['facebook']['pageid'], page_token)