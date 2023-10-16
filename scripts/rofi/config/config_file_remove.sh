#!/bin/bash

source /home/jonalm/scripts/rofi/config/config_options.sh

while [ -z "$engine" ]; do
    displayname=$(printf '%s\n' "${display_options[@]}" | rofi -config ~/.config/rofi/files/config.rasi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-3-config-remove'.rasi -dmenu -i -l 6 -p '') || exit
    engine=$(echo "$options" | cut -d' ' -f1-1)
done

displayname=$(echo "$displayname" | sed 's/ //g')
current_time="Time:$(date +'%T')"

if [ "$displayname" ]; then
    python3 "/home/jonalm/scripts/rofi/config/config_file_remove.py" "$displayname"
    python_exit_code=$?
    if [ $python_exit_code -eq 0 ]; then
        notify-send -a $current_time -u low -t 3000 "Config option removed" "Option: <span foreground='#bf616a' size='medium'>$displayname</span>"
    else
        notify-send -a $current_time -u critical -t 3000 "Config option remove failed" "Error: <span foreground='#bf616a' size='medium'>$python_exit_code</span>"
    fi
fi