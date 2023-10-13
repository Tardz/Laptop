#!/bin/bash

wm_class=$(python3 "/home/jonalm/scripts/qtile/update_floating.py")
python_exit_code=$?

if [ $python_exit_code -eq 0 ]; then
    notify-send -t 3000 "Floating added" "Option: <span foreground='#a3be8c' size='medium'>$wm_class</span>"
else
    notify-send -u critical -t 3000 "Floating add failed" "Error: <span foreground='#bf616a' size='medium'>$python_exit_code</span>"
fi