#!/bin/bash

script_info=$(python3 "/home/jonalm/scripts/qtile/remove_group_match.py")
python_exit_code=$?

if [ $python_exit_code -eq 0 ]; then
    notify-send -t 3000 "Group match removed" "Option: <span foreground='#bf616a' size='medium'>$script_info</span>"
elif [ $python_exit_code -eq 1 ]; then 
    notify-send -u normal -t 3000 "Group match remove stopped" "Error: WM class <span foreground='#bf616a' size='medium'>empty</span>"
elif [ $python_exit_code -eq 2 ]; then 
    notify-send -u normal -t 3000 "Group match remove stopped" "Error: <span foreground='#bf616a' size='medium'>$script_info</span> not in group"
fi