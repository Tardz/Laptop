#!/bin/bash

source /home/jonalm/scripts/rofi/config/config_options.sh 

DMEDITOR="alacritty -e code -n"

choice=$(printf '%s\n' "${display_options[@]}" | rofi -config ~/.config/rofi/files/config.rasi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-3-config'.rasi -dmenu -i -l 5 -p '' )

if [ "$choice" ]; then 
    for option in "${options[@]}"; do
        option_formated=$(echo "$option" | cut -d'-' -f1-1)
        if [[ "$option_formated" == "$choice"* ]]; then
            cfg=$(echo "${option}" | cut -d'-' -f2- )
            # Attempt to open the editor
            if $DMEDITOR "$cfg"; then
                # Editor was opened successfully
                notify-send -u low -t 3000 '-h' "int:transient:1" "Open config" "<span foreground='#a3be8c' size='medium'>$choice</span>opened in vscode"
                qtile cmd-obj -o group v -f toscreen
            else
                notify-send -u critical -t 3000 '-h' "int:transient:1" "Open config failed" "Error for: <span foreground='#bf616a' size='medium'>$choice</span>"
                # Editor failed to open
            fi
        fi
    done
else
    echo "Program terminated." && exit 1
fi

