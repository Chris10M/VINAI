#!usr/bin/bash

open geolocation.html
sleep 8
CHROME_WINDOW = 'xdotool search "Safari" | tail -1'
xdotool windowactivate --sync $CHROME_WINDOW key Tab Tab Return ctrl+s
sleep 2
SAVE_WINDOW = 'xdotool search "Save File" | head -1'
xdotool windowactivate --sync $SAVE_WINDOW Return
sleep 2
xdotool windowactivate --sync $SAVE_WINDOW Return
cp $HOME/Downloads/geo_location.html location.html
kill $(ps -A | grep "chromium.*" | cut -d " " -f 1)
cat location.html | grep "Latitude" | head -1 | tr "<br>" " " | cut -d " " -f 5,10 | tr " " "," > current_location.txt
