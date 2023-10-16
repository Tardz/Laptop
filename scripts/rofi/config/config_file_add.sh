#!/bin/bash

while [ -z "$Name" ]; do
    Name=$(rofi -config ~/.config/rofi/files/config.rasi -theme "$HOME/.config/rofi/files/launchers/type-1/style-7-config-add-name.rasi" -dmenu -i -l 2 -p '') || exit
done

while [ -z "$Filepath" ]; do
    Filepath=$(rofi -config ~/.config/rofi/files/config.rasi -theme "$HOME/.config/rofi/files/launchers/type-1/style-7-config-add-filepath.rasi" -dmenu -i -l 2 -p '') || exit
done

option="$Name - $Filepath"
current_time="Time:$(date +'%T')"

if [[ "$Name" && "$Filepath" ]]; then
    python3 "/home/jonalm/scripts/rofi/config/config_file_add.py" "$option"
    python_exit_code=$?
    if [ $python_exit_code -eq 0 ]; then
        notify-send -a $current_time -u low -t 3000 "Config option added" "Option: <span foreground='#a3be8c' size='medium'>$Name</span>"
    else
        notify-send -a $current_time -u critical -t 3000 "Config option add failed" "Error: <span foreground='#bf616a' size='medium'>$python_exit_code</span>"
    fi
fi