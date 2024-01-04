#!/bin/bash

BROWSER="firefox"

source /home/jonalm/googleDrive/search_options.sh

while [ -z "$engine" ]; do
    displayname=$(printf '%s\n' "${display_options[@]}" | rofi -config ~/.config/rofi/files/config.rasi \-theme "$HOME/.config/rofi/files/launchers/search"/'search'.rasi -dmenu -i -l 5 -p '') || exit
    engine=$(echo "$options" | cut -d' ' -f1-1)
done

/home/jonalm/scripts/other/check_internet.sh
internet_status=$?
current_screen=$(/home/jonalm/scripts/other/get_current_screen.py)

if [ $internet_status -eq 1 ]; then
    exit 1
fi

for option in "${options[@]}"; do
    option_formated=$(echo "$option" | cut -d'-' -f1-1)
    if [[ "$displayname" == "$option_formated" ]]; then
        url=$(echo "$option" | cut -d'-' -f2- )
        search=$(echo "$option" | cut -d' ' -f2)
        if [[ "$search" == "Search" ]]; then
            while [ -z "$query" ]; do
                query=$(rofi -config ~/.config/rofi/files/config.rasi \-theme "$HOME/.config/rofi/files/launchers/search"/'search'.rasi -dmenu -i -l 2 -p '') || exit
            done
            $BROWSER "$url""$query"
            notify-send -u low -t 2400 '-h' "int:transient:1" "Search finished" "Website: <span foreground='#81a1c1' size='medium'>$displayname</span>"
            exit 1
        fi
    fi
done

if [ $current_screen -eq 1 ]; then
    qtile cmd-obj -o cmd -f next_screen
    qtile cmd-obj -o group c -f toscreen
    xdotool mousemove 4300 900
elif [ $current_screen -eq 0 ]; then 
    qtile cmd-obj -o group c -f toscreen
fi

notify-send -u low -t 2400 '-h' "int:transient:1" "Search finished" "Website: <span foreground='#81a1c1' size='medium'>$displayname</span>"

$BROWSER "$url"
exit 1

