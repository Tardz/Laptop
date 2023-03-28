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
fi