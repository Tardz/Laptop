#!/bin/bash

source /home/jonalm/scripts/rofi/config/config_options.sh

while [ -z "$engine" ]; do
    displayname=$(printf '%s\n' "${display_options[@]}" | rofi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-3-config-remove'.rasi -dmenu -i -l 6 -p '') || exit
    engine=$(echo "$options" | cut -d' ' -f1-1)
done

if [ "$displayname" ]; then
    python3 "/home/jonalm/scripts/rofi/config/config_file_remove.py" "$displayname"
    python_exit_code=$?
    if [ $python_exit_code -eq 0 ]; then
        notify-send -u low -t 3000 "Config option removed" "Option: <span foreground='#bf616a' size='medium'>$displayname</span>"
        /home/jonalm/scripts/drive/bisync_drive.sh
    else
        notify-send -u critical -t 3000 "Config option remove failed" "Error: <span foreground='#bf616a' size='medium'>$python_exit_code</span>"
    fi
fi