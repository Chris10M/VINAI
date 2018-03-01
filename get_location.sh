#!usr/bin/bash

xdg-open geo_location.html
sleep 8
xdotool windowactivate --sync $(eval xdotool search "Chromium" | tail -1) key Tab Tab Return ctrl+s
sleep 2 
xdotool windowactivate --sync $(eval xdotool search "Save File" | head -1) Return
sleep 2
xdotool windowactivate --sync $SAVE_WINDOW Return
cp $HOME/Downloads/geo_location.html location.html
kill $(ps -A | grep "chromium.*" | cut -d " " -f 1)
cat location.html | grep "Latitude" | head -1 | tr "<br>" " " | cut -d " " -f 5,10 | tr " " "," > current_location.txt
