#!/bin/bash

/home/jonalm/scripts/other/check_internet.sh
internet_status=$?

if [ $internet_status -eq 1 ]; then
    exit 1
fi

source /home/jonalm/googleDrive/search_options.sh

while [ -z "$engine" ]; do
    displayname=$(printf '%s\n' "${display_options[@]}" | rofi -config ~/.config/rofi/files/config.rasi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-7-search-remove'.rasi -dmenu -i -l 6 -p '') || exit
    engine=$(echo "$options" | cut -d' ' -f1-1)
done

current_time="Time:$(date +'%T')"
 

if [ "$displayname" ]; then
    python3 "/home/jonalm/scripts/rofi/search/search_remove.py" "$displayname"
    python_exit_code=$?
    if [ $python_exit_code -eq 0 ]; then
        notify-send -a $current_time -u low -t 3000 "Search option removed" "Option: <span foreground='#bf616a' size='medium'>$displayname</span>"
        /home/jonalm/scripts/drive/bisync_drive.sh
    else
        notify-send -a $current_time -u critical -t 3000 "Search option remove failed" "Error: <span foreground='#bf616a' size='medium'>$python_exit_code</span>"
    fi
fi