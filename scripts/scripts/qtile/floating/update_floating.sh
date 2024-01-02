#!/bin/bash

wm_class=$(python3 "/home/jonalm/scripts/qtile/floating/update_floating.py")
python_exit_code=$?
current_time="Time:$(date +'%T')"

if [ $python_exit_code -eq 0 ]; then
    notify-send -a $current_time -u low -t 3000 "Floating added" "Option: <span foreground='#a3be8c' size='medium'>$wm_class</span>"
elif [ $python_exit_code -eq 1 ]; then
    notify-send -a $current_time -u normal -t 3000 "Floating add stopped" "Error: WM class <span foreground='#bf616a' size='medium'>is empty</span>"
elif [ $python_exit_code -eq 2 ]; then
    notify-send -a $current_time -u normal -t 3000 "Floating add stopped" "Error: <span foreground='#bf616a' size='medium'>$wm_class</span> already floats"
fi