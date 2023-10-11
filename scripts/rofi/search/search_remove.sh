#!/bin/bash

source /home/jonalm/googleDrive/search_options.sh

while [ -z "$engine" ]; do
    displayname=$(printf '%s\n' "${display_options[@]}" | rofi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-7-search-remove'.rasi -dmenu -i -l 6 -p '') || exit
    engine=$(echo "$options" | cut -d' ' -f1-1)
done

if [ "$displayname" ]; then
    python3 "/home/jonalm/scripts/rofi/search/search_remove.py" "$displayname"
    python_exit_code=$?
    if [ $python_exit_code -eq 0 ]; then
        echo "Python script completed successfully."
        /home/jonalm/scripts/drive/bisync_drive.sh
    else
        echo "Python script encountered an error (Exit code: $python_exit_code)."
    fi
fi