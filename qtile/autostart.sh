#!/bin/bash
### KEYBOARD CONF ###
setxkbmap se
### APPS ###
xss-lock --lock &
powertop --auto-tune
nitrogen --restore &
picom -b &
fusuma &
killall alttab
background_path=$(awk -F'=' '/file=/{print $2}' ~/.config/nitrogen/bg-saved.cfg)
# sudo cp $background_path /usr/share/sddm/themes/sddm-slice-1.5.1/background.png
sudo cp $background_path /usr/share/sddm/themes/sugar-candy/background.png
alttab -bg '#2e3440' -fg '#d8dee9' -bc '#2e3440' -bw 18 -inact '#3b4252' -frame '#81a1c1' &
