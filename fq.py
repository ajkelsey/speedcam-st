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

from os.path import exists

class FileQueue():
    def __init__(self, filename, maxlength):
        self.filename = filename
        self.maxlength = maxlength

        if exists(filename) == False:
            with open(filename, 'a') as file:
                pass
        else:
            self.trim_queue()

    def trim_queue(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
        num_lines = len(lines)
        if num_lines > self.maxlength:
            self.pop(num_lines - self.maxlength)

    def push(self, string):
        with open(self.filename, 'a') as file:
            file.write(string)
        self.trim_queue()

    def pop(self, n):
        with open(self.filename, 'r+') as file:
            lines = file.readlines()
            # Moves file pointer to beginning
            file.seek(0)
            file.writelines(lines[n:])
            # Removes any existing data after the new lines.
            file.truncate()

