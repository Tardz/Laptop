#!/bin/bash

BROWSER="brave"

# source /home/jonalm/scripts/rofi/search/search_options.sh 
source /home/jonalm/googleDrive/search_options.sh

while [ -z "$engine" ]; do
    displayname=$(printf '%s\n' "${display_options[@]}" | rofi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-7-search'.rasi -dmenu -i -l 5 -p '') || exit
    engine=$(echo "$options" | cut -d' ' -f1-1)
done

/home/jonalm/scripts/other/check_internet.sh
internet_status=$?

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
                query=$(rofi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-7-search'.rasi -dmenu -i -l 2 -p '') || exit
            done
            qtile cmd-obj -o group 2 -f toscreen
            $BROWSER "$url""$query"
            notify-send -u low -t 2400 "Search finished" "Website: <span foreground='#81a1c1' size='medium'>$displayname</span>"
            exit 1
        fi
    fi
done

qtile cmd-obj -o group 2 -f toscreen
notify-send -u low -t 2400 "Search finished" "Website: <span foreground='#81a1c1' size='medium'>$displayname</span>"

$BROWSER "$url"
exit 1

