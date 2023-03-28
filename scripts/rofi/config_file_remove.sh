#!/bin/bash

source /home/jonalm/scripts/rofi/config_file_options.sh

while [ -z "$engine" ]; do
    displayname=$(printf '%s\n' "${display_options[@]}" | rofi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-7-config-remove'.rasi -dmenu -i -l 6 -p '') || exit
    engine=$(echo "$options" | cut -d' ' -f1-1)
done

if [ "$displayname" ]; then
    python3 "/home/jonalm/scripts/rofi/config_file_remove.py" "$displayname"
fi