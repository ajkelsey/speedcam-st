from datetime import datetime, timedelta
import os
import pandas as pd

path = '/opt/speedcam/data/'

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

def top_speeder(data_df):
    # Extract fastest car.
    image_path = '/opt/speedcam/images'
    speeder = 0
    for i in range(len(data_df)):
        speed = float(data_df.loc[i, 'Speed'])
        filename = data_df.loc[i, 'Image Path']
        if speed > speeder:
            speeder = speed
            speeder_filename = f'{image_path}/{filename}.jpg'
    return speeder, speeder_filename

if __name__ == '__main__':
    yesterday, period = previous_day()
    print(yesterday)
    file_list = get_file_list(period)
    data_df = ingest_data(file_list)
    speeder, speeder_filename = top_speeder(data_df)
    print(f'{speeder}, {speeder_filename}')
