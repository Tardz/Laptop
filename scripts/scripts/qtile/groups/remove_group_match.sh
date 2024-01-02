#!/bin/bash

script_info=$(python3 "/home/jonalm/scripts/qtile/groups/remove_group_match.py")
python_exit_code=$?
current_time="Time:$(date +'%T')"

if [ $python_exit_code -eq 0 ]; then
    notify-send -a $current_time -u low -t 3000 "Group match removed" "Option: <span foreground='#bf616a' size='medium'>$script_info</span>"
elif [ $python_exit_code -eq 1 ]; then 
    notify-send -a $current_time -u normal -t 3000 "Group match remove stopped" "Error: WM class <span foreground='#bf616a' size='medium'>empty</span>"
elif [ $python_exit_code -eq 2 ]; then 
    notify-send -a $current_time -u normal -t 3000 "Group match remove stopped" "Error: <span foreground='#bf616a' size='medium'>$script_info</span> not in group"
fi