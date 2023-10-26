#!/bin/bash

width=100
height=20

x_position=1880
y_position=50

# Create the yad dialog with the specified geometry and buttons
yad --geometry=${width}x${height}+${x_position}+${y_position} \
    --close-on-unfocus\
    --buttons-layout="edge"\
    --on-top\
    --button="Powersaver:0" --button="Balanced:1" --button="Performance:2"