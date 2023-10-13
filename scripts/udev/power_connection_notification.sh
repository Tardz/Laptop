#!/bin/bash

if [ "$1" = "true" ] || [ "$1" = "1" ]; then
    notify-send -u low -t 2300 "Power Connected" "Your laptop is now plugged in."
elif [ "$1" = "false" ] || [ "$1" = "0" ]; then
    notify-send -u low -t 2300 "Power disconnected" "Your laptop is now unplugged."
fi
