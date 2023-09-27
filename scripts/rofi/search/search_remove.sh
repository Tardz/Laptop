#!/bin/bash

source Insync/johalm123@gmail.com/Google\ Drive/Arch_delat/search_options.sh

while [ -z "$engine" ]; do
    displayname=$(printf '%s\n' "${display_options[@]}" | rofi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-7-search-remove'.rasi -dmenu -i -l 6 -p '') || exit
    engine=$(echo "$options" | cut -d' ' -f1-1)
done

if [ "$displayname" ]; then
    python3 "/home/jonalm/scripts/rofi/search/search_remove.py" "$displayname"
fi