#!/bin/bash

source /home/jonalm/scripts/rofi/config_options.sh 

DMEDITOR="alacritty -e code -n"

choice=$(printf '%s\n' "${display_options[@]}" | rofi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-3-config'.rasi -dmenu -i 20 -columns 25 -p '' )

if [[ "$choice" == "Quit" ]]; then
    echo "Program terminated." && exit 1
elif [ "$choice" ]; then 
    for option in "${options[@]}"; do
        option_formated=$(echo "$option" | cut -d'-' -f1-1)
        if [[ "$option_formated" == "$choice"* ]]; then
            cfg=$(echo "${option}" | cut -d'-' -f2- )
            $DMEDITOR "$cfg"
            qtile cmd-obj -o group 3 -f toscreen
            break
        fi
    done
else
    echo "Program terminated." && exit 1
fi

