#!/bin/bash

wm_class=$(python3 "/home/jonalm/scripts/qtile/update_floating.py")
python_exit_code=$?

if [ $python_exit_code -eq 0 ]; then
    notify-send -t 3000 "Floating add" "<span foreground='#a3be8c' size='medium'>$wm_class</span> added"
else
    notify-send -u critical -t 3000 "Floating add" "Error: <span foreground='#bf616a' size='medium'>$python_exit_code</span>"
fi