#!/bin/bash

# SpeedcamST: A do-it-yourself speed camera.
# Copyright (C) 2024  Andrew Kelsey [ajkelsey@grandroyal.org]

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

echo '  _________                        .___                      ____________________'
echo ' /   _____/_____   ____   ____   __| _/____ _____    _____  /   _____/\__    ___/'
echo ' \_____  \\____ \_/ __ \_/ __ \ / __ |/ ___\\__  \  /     \ \_____  \   |    |   '
echo ' /        \  |_> >  ___/\  ___// /_/ \  \___ / __ \|  Y Y  \/        \  |    |   '
echo '/_______  /   __/ \___  >\___  >____ |\___  >____  /__|_|  /_______  /  |____|   '
echo '        \/|__|        \/     \/     \/    \/     \/      \/        \/            '
echo ''
echo "SpeedcamST Copyright (C) 2024  Andrew Kelsey"
echo "This program comes with ABSOLUTELY NO WARRANTY."
echo "This is free software, and you are welcome to redistribute it"
echo "under certain conditions; type 'cat LICENSE' for details."

root='/opt/speedcam'
path_array=("${root}/data" "${root}/http" "${root}/imageq" "${root}/images" "${root}/log" \
            "${root}/video" "${root}/videoq")

# Create directory structure
for directory in "${path_array[@]}"; do
    if [ -d $directory ]; then
        echo "Found ${root)${directory}..."
        continue
    else 
        echo "Creating ${root)${directory}..."
        mkdir ${root}${directory}
    fi
done

url='https://raw.githubusercontent.com/ajkelsey/speedcam-st/main/'
file_array=("LICENSE" "README.md" "alpr.py" "camera.py" "case_fans.py" "data.py" \
            "default_image.jpg" "facebook.py" "ffmpeg_streamer.py" "fq.py" "ir_filter.py" \
            "plot_the_plots.py" "radar.py" "speedcam-config.json.sample" "stats.py" "vehicle.py"
            "http/index.html.sample" "systemd/case_fans.service" "systemd/speedcam.service")

# Download files from Github
for file in ${file_array[@]}; do
    echo "Downloading ${file}..."
    wget -O ${file} ${url}${file}
done

# Create symbolic links to .service files
echo "Creating symbolic links to service files..."
srv_path='/etc/systemd/system'
ln -s ${root}/systemd/speedcam.service ${srv_path}/speedcam.service
ln -s ${root}/systemd/case_fans.service ${srv_path}/case_fans.service

# Install python dependencies
echo 'Installing python dependencies...'
sudo apt update -y && sudo apt install python-apscheduler python3-matplotlib python3-matplotlib \
python3-pandas python3-persist-queue python3-rich
pip install ultralytics --break-system-packages

echo -e "\n\n
For new installations, edit speedcam-config.json.sample and save it to speedcam-config.json
"
