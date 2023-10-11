#!/bin/bash

while [ -z "$Name" ]; do
    Name=$(rofi -theme "$HOME/.config/rofi/files/launchers/type-1/style-7-config-add-name.rasi" -dmenu -i -l 2 -p '') || exit
done

while [ -z "$Filepath" ]; do
    Filepath=$(rofi -theme "$HOME/.config/rofi/files/launchers/type-1/style-7-config-add-filepath.rasi" -dmenu -i -l 2 -p '') || exit
done

option="$Name - $Filepath"

if [[ "$Name" && "$Filepath" ]]; then
    python3 "/home/jonalm/scripts/rofi/config/config_file_add.py" "$option"
fi