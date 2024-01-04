#!/bin/bash
### DISPLAY CONF ###
xrandr --output DisplayPort-0 --mode 1920x1080 --rate 144 --output DisplayPort-2 --mode 1920x1080 --rate 144 --output HDMI-A-0 --off

### KEYBOARD CONF ###
setxkbmap se

### APPS ###
nitrogen --restore &
picom &
openrazer-daemon
imwheel -b 45 &
polychromatic-cli --dpi 600 &
