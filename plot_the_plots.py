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


import argparse
from argparse import RawTextHelpFormatter
from datetime import datetime, timedelta
from dateutil.parser import *
import matplotlib.dates as mpl
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
import os
import pandas as pd
from rich.console import Console
from rich.progress import Progress

def parse_the_args():
    # desc = "-+= Plot the Plots =+-\n\nThis script creates graphs based on\n" + \
    #        "collected data from the speed camera.\n"
    desc = """

    ██████╗ ██╗      ██████╗ ████████╗    ████████╗██╗  ██╗███████╗    ██████╗ ██╗      ██████╗ ████████╗███████╗
    ██╔══██╗██║     ██╔═══██╗╚══██╔══╝    ╚══██╔══╝██║  ██║██╔════╝    ██╔══██╗██║     ██╔═══██╗╚══██╔══╝██╔════╝
    ██████╔╝██║     ██║   ██║   ██║          ██║   ███████║█████╗      ██████╔╝██║     ██║   ██║   ██║   ███████╗
    ██╔═══╝ ██║     ██║   ██║   ██║          ██║   ██╔══██║██╔══╝      ██╔═══╝ ██║     ██║   ██║   ██║   ╚════██║
    ██║     ███████╗╚██████╔╝   ██║          ██║   ██║  ██║███████╗    ██║     ███████╗╚██████╔╝   ██║   ███████║
    ╚═╝     ╚══════╝ ╚═════╝    ╚═╝          ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═╝     ╚══════╝ ╚═════╝    ╚═╝   ╚══════╝

                      This script creates graphs based on collected data from the speed camera.
    """
    parser = argparse.ArgumentParser(description=desc, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-g', '--graph', help='Specify graph type: \n\t' + \
                        'bar\tBar graph.\n\t' + \
                        'line\tLine graph.', required=True)
    parser.add_argument('-tl', '--trend', help='Add a trend line to the graph.', action='store_true', default=False)
    parser.add_argument('-t', '--type', help='Specify desired data type: \n\t' + \
                        'carsperday\tGraphs the number of cars per day.\n\t' + \
                        'carsperhour\tGraphs the number of cars per hour.\n\t' + \
                        'speedbin\tNumbers of cars per speed category. [default=0 26 31 36 41 46 51]\n', required=True)
    parser.add_argument('-sb', '--speedbin', help='Enter space separated values to override the default speedbins.', 
                        nargs='*', default=[0, 26, 31, 36, 41, 46, 51])
    parser.add_argument('-p', '--period', help='Specify time period: \n\t' + \
                        'currentmonth\tSets the time period for the current month.\n\t'
                        'prevmonth\tSets time period to previous month.\n\t' + \
                        'currentyear\tSets time period to current year.\n\t' + \
                        'prevyear\tSets time period to previous year.\n\t' + \
                        'YYYY-MM-DD\tEnter a specific date.',required=True)
    parser.add_argument('-s', '--speed', help='Speeds above threshold will be graphed. [default=0]\n ', default=0)
    args = parser.parse_args()
    progress.start_task(task)
    if args.period == 'prevmonth':
        data_df, period = determine_prev_month()
    elif args.period == 'prevyear':
        data_df, period = determine_prev_year()
    elif args.period == 'currentmonth':
        data_df, period = determine_current_month()
    elif args.period == 'currentyear':
        data_df, period = determine_current_year()
    else:
        period = args.period
        data_df = get_period_file_list(period)
    if args.type == 'carsperday':
        plot_cars_per_day(data_df, period, args)
    elif args.type == 'carsperhour':
        plot_cars_per_hour(data_df, period, args)
    elif args.type == 'speedbin':
        plot_speed_bins(data_df, period, args)

def determine_prev_month():
    today = datetime.today()
    # Brings date to the first of the month.
    first = today.replace(day=1)
    prv_month = str(first - timedelta(days=1))
    period = prv_month[:7]
    data_df = get_period_file_list(period)
    return data_df, period

def determine_prev_year():
    today = datetime.today()
    # Brings date to the first day of the year.
    first = today.replace(month=1, day=1)
    prv_year = str(first - timedelta(days=1))
    period = prv_year[:4]
    data_df = get_period_file_list(period)
    return data_df, period

def determine_current_month():
    today = datetime.today()
    period = str(today.now())[:7]
    data_df = get_period_file_list(period)
    return data_df, period

def determine_current_year():
    current_year = str(datetime.today())
    period = current_year[:4]
    data_df = get_period_file_list(period)
    return data_df, period

def get_period_file_list(period):
    last_period_list = []
    files = os.listdir(path)   
    # Filters for files only.
    files = [f for f in files if os.path.isfile(path + f)]
    for file in files:
        if file.__contains__(period) == True:
            last_period_list.append(file)
    data_df = ingest_data(last_period_list)
    return data_df

# Loads appropriate data files.
def ingest_data(file_list):
    # progress.update(task, description='Ingesting data...')
    data_df = pd.DataFrame()
    # Joins CSV files into one dataframe.
    for file in file_list:
        df = pd.read_csv(path + file)
        data_df = pd.concat([df, data_df], ignore_index=True)
    return data_df

def plot_cars_per_day(data_df, period, args):
    progress.update(task, description='Crunching data...')
    filename = period + '_cars_per_day.jpg'
    title = 'Daily Vehicle Totals for ' + period
    xlabel = ''
    ylabel = 'Number of Cars'
    cars_per_day = {}
    # Iterate dataframe, pull dates and associated speeds.
    for i in range(len(data_df)):
        date = data_df.loc[i, 'Date']
        speed = data_df.loc[i, 'Speed']
        if float(speed) >= float(args.speed):
            if date in cars_per_day.keys():
                # Adds speeds to date entry.
                cars_per_day.setdefault(date, []).append(speed)
            else:
                # Creates date entry if it doesn't exist.
                cars_per_day[date] = [speed]
            if float(args.speed) > 0:
                title = 'Daily Speeders for ' + period
                filename = period[:7] + '_speeders_per_day.jpg'
    # Creates plot data dictionary.
    carspday_plot_data = {}
    for key in cars_per_day.keys():
        carspday_plot_data.setdefault(key, len(cars_per_day[key]))
    # Convert dict to list for sorting.
    carspday_plot_list = []
    for key, val in carspday_plot_data.items():
        carspday_plot_list.append([key, val])
    # Sort list by date ascending.
    carspday_plot_list.sort()
    # Create parameters to send to method.
    xdata = []
    ydata = []
    for list in carspday_plot_list:
        xdata.append(list[0])
        ydata.append(list[1])
    
    plot_the_plot(period, xdata, ydata, title, xlabel, ylabel, filename, args)
    
### Number of cars in speed bins ###
def plot_speed_bins(data_df, period, args):
    progress.update(task, description='Crunching data...')
    # Create nested bin list.
    speed_bins = []
    # Creates labels in dict.
    for i in range(len(args.speedbin)):
        if i == (len(args.speedbin) - 1):
            speed_bins.append([f'{str(args.speedbin[i])}+', 0])
        else:
            speed_bins.append([f'{str(args.speedbin[i])}-{str(int(args.speedbin[i + 1]) - 1)}', 0])
    # Iterate dataframe, add count to correct speed bin.
    for j in range(len(data_df)):
        speed = data_df.loc[j, 'Speed']
        # Determine correct speed bin.
        for k in range(len(speed_bins)):
            # Checks for last index to avoid out of bounds.
            if (k == (len(speed_bins) - 1)) and (speed >= int(args.speedbin[-1])).all():
                speed_bins[k][1] = speed_bins[k][1] + 1
            # Adds to correct bin.
            elif speed >= int(args.speedbin[k]) and speed < int(args.speedbin[k + 1]):
                speed_bins[k][1] = speed_bins[k][1] + 1
    # Create parameters to send to method.
    xdata = []
    ydata = []
    for l in range(len(speed_bins)):
        xdata.append(speed_bins[l][0])
        ydata.append(speed_bins[l][1])
    filename = f'{period}.jpg'
    title = datetime.strptime(period, '%Y-%m-%d').strftime('%A %B %d, %Y')
    xlabel = 'MPH'
    ylabel = 'Number of Cars'
    plot_the_plot(period, xdata, ydata, title, xlabel, ylabel, filename, args)

### Number of cars in hourly bins ###
def plot_cars_per_hour(data_df, period, args):
    progress.update(task, description='Crunching data...')
    # Create nested bin list.
    hour_bins = [
                ['00:00', 0], ['01:00', 0], ['02:00', 0], ['03:00', 0],
                ['04:00', 0], ['05:00', 0], ['06:00', 0], ['07:00', 0],
                ['08:00', 0], ['09:00', 0], ['10:00', 0], ['11:00', 0],
                ['12:00', 0], ['13:00', 0], ['14:00', 0], ['15:00', 0],
                ['16:00', 0], ['17:00', 0], ['18:00', 0], ['19:00', 0],
                ['20:00', 0], ['21:00', 0], ['22:00', 0], ['23:00', 0],
                ]
    # Iterate dataframe, add count to correct hour bin.
    for j in range(len(data_df)):
        hour = data_df.loc[j, 'Time']
        speed = data_df.loc[j, 'Speed']
        # Determine correct speed bin.
        if float(speed) >= float(args.speed):
            for k in range(len(hour_bins)):
                # Checks for last index to avoid out of bounds.
                # if (k == (len(hour_bins) - 1)):
                #     hour_bins[k][1] = hour_bins[k][1] + 1
                # Adds to correct bin.
                if str(hour)[:2] == str(hour_bins[k][0])[:2]:
                    hour_bins[k][1] = hour_bins[k][1] + 1
                    # hour_bins[k][1].append
    # Create parameters to send to method.
    xdata = []
    ydata = []
    for l in range(len(hour_bins)):
        xdata.append(hour_bins[l][0])
        ydata.append(hour_bins[l][1])
    filename = period + '_hour_bins.jpg'
    title = 'Total Vehicles Per Hour ' + period
    xlabel = 'Time of Day'
    ylabel = 'Number of Cars'
    plot_the_plot(period, xdata, ydata, title, xlabel, ylabel, filename, args)

### Top speeders based on plate. ###
def top_speeders():
    pass

def plot_the_plot(period, xdata, ydata, title, xlabel, ylabel, filename, args):
    global message
    progress.update(task, description='Plotting the plot...')
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_title(title, fontsize=18)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if args.graph == 'bar':
        ax.bar(xdata, ydata)
        # Applies bar totals to top of bar.
        for bar in ax.patches:
            # Avoids labeling 0 values.
            if bar.get_height() > 0:
                ax.annotate(format(bar.get_height()),
                            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                            ha='center', va='center', size=12, xytext=(0,8), textcoords='offset points')
    if args.graph == 'line':
        ax.plot(xdata, ydata)
    # Trend line.
    if args.trend is True:
        # Use index instead of xdata for trend input.
        x = []
        for index in range(len(xdata)):
            x.append(index)
        # Convert data to np array
        x = np.asarray(x, dtype=np.float64)
        y = np.asarray(ydata, dtype=np.float64)
        # Calculate trend line
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        # Plot trend line.
        ax.plot(x, p(x), color='red', linewidth=2)
    # Rotates and aligns x-axis labels.
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    plt.savefig(filename)
    message = f'Done! Saved as {filename}'
    

if __name__ == '__main__':
    message = ''
    with Progress() as progress:
        console = Console()
        task = progress.add_task(start=False, description='Parsing the args...', total=None)
        path = '/opt/speedcam/data/'
        parse_the_args()
    print(message)