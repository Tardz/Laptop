#!/bin/bash

/home/jonalm/scripts/other/check_internet.sh
internet_status=$?

if [ $internet_status -eq 1 ]; then
    exit 1
fi

while [ -z "$WebName" ]; do
    WebName=$(rofi -config ~/.config/rofi/files/config.rasi -theme "$HOME/.config/rofi/files/launchers/search/search-add-name.rasi" -dmenu -i -l 2 -p '') || exit
done

while [ -z "$Url" ]; do
    Url=$(rofi -config ~/.config/rofi/files/config.rasi -theme "$HOME/.config/rofi/files/launchers/search/search-add-url.rasi" -dmenu -i -l 2 -p '') || exit
done

option="$WebName - $Url"
current_time="Time:$(date +'%T')"

if [[ "$Url" && "$WebName" ]]; then
    python3 "/home/jonalm/scripts/rofi/search/search_add.py" "$option"
    python_exit_code=$?
    if [ $python_exit_code -eq 0 ]; then
        notify-send -a $current_time -u low -t 3000 "Search option added" "Option: <span foreground='#a3be8c' size='medium'>$WebName</span>"
        /home/jonalm/scripts/drive/bisync_drive.sh
    else
        notify-send -a $current_time -u critical -t 3000 "Search option add failed" "Error: <span foreground='#bf616a' size='medium'>$python_exit_code</span>"
    fi
fi