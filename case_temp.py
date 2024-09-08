#! /bin/python

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


import matplotlib.pyplot as plt
import plotext as plt

def load_data(filename):
    with open(filename, 'r') as file:
        data = []
        x = []
        y = []
        for line in file:
            data.append(line.split(' '))

    for row in data:
        x.append(str(row[0]))
        y.append(int(row[1].strip()))
    return x, y

def create_plot(x, y):
    plt.clear_terminal()
    plt.clear_data()

    xsize = (plt.terminal_width() * .75)
    ysize = (plt.terminal_height() * .75)
    current_temp =  y[-1]

    plt.plot(y, color='default', marker='braille')
    
    plt.theme('clear')
    plt.title('Case Temperature')
    plt.plot_size(xsize, ysize)
    plt.text(f'Current Temperature: {current_temp}C', x=54, y=-20, alignment='center')

    plt.xlabel('Hours')
    plt.xticks(ticks=[1, 72, 144, 216, 288, 360, 432, 504, 576],
               labels=[48, 42, 36, 30, 24, 18, 12, 6, 0])
    
    plt.vline(144, 'gray+')
    plt.vline(288, 'gray+')
    plt.vline(432, 'gray+')
    
    plt.ylim(-20, 50)
    plt.yfrequency(15)
    
    plt.hline(0, 'gray+')
    plt.hline(38, 'gray+')
    
    plt.show()
    print('Ctrl-C to quit.\n')
    plt.sleep(300)
    


if __name__ == '__main__':
    try:
        while True:
            x, y = load_data('/opt/speedcam/case_temp.q')
            create_plot(x, y)
    except KeyboardInterrupt:
        print('\n')
        quit()
