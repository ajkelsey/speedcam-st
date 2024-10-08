from datetime import datetime, timedelta
import os
import pandas as pd

path = '/opt/speedcam/data/'
speed_limit = 25
min_fine_speed = 30 # The minimum speed to be considered for fine calculation
speed_brackets = [[1, 9], [10, 14], [15, 19], [20, 24], [25, 29], [30, 34], [35, 39]]
speed_fines = [85, 95, 105, 200, 220, 240, 269]

def previous_day():
    # Get previous day.
    today = datetime.today()
    prv_day = today - timedelta(days=1)
    period = str(prv_day)[:10]
    yesterday = prv_day.strftime('%A %B %d, %Y')
    return yesterday, period

def get_file_list(period):
    # Get list of files.
    last_period_list = []
    files = os.listdir(path)   
    # Filters for files only.
    files = [f for f in files if os.path.isfile(path + f)]
    for file in files:
        if file.__contains__(period) == True:
            last_period_list.append(file)
    return last_period_list

def ingest_data(file_list):
    data_df = pd.DataFrame()
    # Joins CSV files into one dataframe.
    for file in file_list:
        df = pd.read_csv(path + file)
        data_df = pd.concat([df, data_df], ignore_index=True)
    return data_df

def top_speeder(min_speed_post, data_df):
    # Extract fastest car.
    image_path = '/opt/speedcam/images'
    speeder = 0
    speeder_filename = ''
    for i in range(len(data_df)):
        speed = float(data_df.loc[i, 'Speed'])
        filename = data_df.loc[i, 'Image Path']
        if speed > min_speed_post:
            if speed > speeder:
                speeder = speed
                speeder_filename = f'{image_path}/{filename}.jpg'
    return speeder, speeder_filename

def daily_revenue():
    daily_fines = 0
    speed_count = [0, 0, 0, 0, 0, 0, 0]
    yesterday, period = previous_day()
    file_list = get_file_list(period)
    data_df = ingest_data(file_list)
    for i in range(len(data_df)):
        vehicle_speed = float(data_df.loc[i, 'Speed'])
        for j in range(len(speed_brackets)):
            if vehicle_speed > min_fine_speed:
                if vehicle_speed >= (speed_brackets[j][0] + speed_limit) and vehicle_speed <= (speed_brackets[j][1] + speed_limit):
                    speed_count[j] = speed_count[j] + 1
                    continue
    print(speed_count)
    for k in range(len(speed_count)):
        daily_fines = daily_fines + (speed_count[k] * speed_fines[k])
    daily_fines = f'Total potential fines: ${daily_fines:,}'
    return yesterday, daily_fines

if __name__ == '__main__':
    pass