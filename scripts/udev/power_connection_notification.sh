#!/bin/bash

# Redirect output and errors to a log file
exec >> /tmp/script_output.log 2>&1

if [ "$1" = "true" ]; then
    notify-send -u low -t 3000 "Power Connected" "<span foreground='#a3be8c' size='medium'>Charging</span>"
elif [ "$1" = "false" ]; then
    notify-send -u low -t 3000 "Power disconnected" "<span foreground='#bf616a' size='medium'Discharging</span>"
fi