import csv
import logging
from os.path import exists

data_logger = logging.getLogger('speedlog.data')
data_logger.addHandler

def process(vehicle):
    # Checks for daily file. Creates and adds field names if it doesn't exist.
    global filename
    filename = '/opt/speedcam/data/' + vehicle.sheet_date + '.csv'
    if exists(filename) == False:
        write_csv('Date', 'Time', 'Travel Direction', 'Speed', 'Plate', 'Image Path')
        data_logger.debug(f'CSV file \"{filename}\" created.')
    write_csv(vehicle.sheet_date, vehicle.sheet_time, vehicle.direction, str(vehicle.speed), 
              vehicle.plate, vehicle.file_date)
    data_logger.debug(f"Vehicle {vehicle.file_date} logged.")
    return filename

def write_csv(*args):
    try:
        with open(filename, 'a') as data_csv:
                csv.writer(data_csv).writerow(args)
    except FileNotFoundError:
        data_logger.warning('CSV file not found error.')
    except Exception:
        data_logger.exception('CSV write exception occured.')
