#!/bin/bash

script_info=$(python3 "/home/jonalm/scripts/qtile/update_group_match.py")
python_exit_code=$?

if [ $python_exit_code -eq 0 ]; then
    notify-send -t 3000 "Group match added" "<span foreground='#a3be8c' size='medium'>$script_info</span> added"
elif [ $python_exit_code -eq 1 ]; then 
    notify-send -u normal -t 3000 "Group match add stopped" "Error: WM class <span foreground='#bf616a' size='medium'>empty</span>"
elif [ $python_exit_code -eq 2 ]; then 
    notify-send -u critical -t 3000 "Group match add faild" "Error: group <span foreground='#bf616a' size='medium'>not found</span>"
elif [ $python_exit_code -eq 3 ]; then 
    notify-send -u normal -t 3000 "Group match add stopped" "Error: <span foreground='#bf616a' size='medium'>$script_info</span> already in group"
fi