#!/bin/bash
xrandr --output DP-1 --off
xrandr --output DVI-D-1 --off
xrandr --output DVI-D-1 --mode 1920x1080 --rate 144 --left-of HDMI-1
xrandr --output HDMI-1 --mode 1920x1080 --rate 144
