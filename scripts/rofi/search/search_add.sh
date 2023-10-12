#!/bin/bash

while [ -z "$WebName" ]; do
    WebName=$(rofi -theme "$HOME/.config/rofi/files/launchers/type-1/style-7-search-add-name.rasi" -dmenu -i -l 2 -p '') || exit
done

while [ -z "$Url" ]; do
    Url=$(rofi -theme "$HOME/.config/rofi/files/launchers/type-1/style-7-search-add-url.rasi" -dmenu -i -l 2 -p '') || exit
done

option="$WebName - $Url"

if [[ "$Url" && "$WebName" ]]; then
    python3 "/home/jonalm/scripts/rofi/search/search_add.py" "$option"
    python_exit_code=$?
    if [ $python_exit_code -eq 0 ]; then
        notify-send -t 3000 "Search option added" "Option: <span foreground='#a3be8c' size='medium'>$WebName</span>"
        /home/jonalm/scripts/drive/bisync_drive.sh
    else
        notify-send -u critical -t 3000 "Search option add failed" "Error: <span foreground='#bf616a' size='medium'>$python_exit_code</span>"
    fi
fi