#!/bin/bash
  
files_last_update=$(jq -r '.date' "/home/jonalm/scripts/term/save_files_data.json")

declare -a options=(
"Floating - Add | $HOME/scripts/qtile/update_floating.py"
"Floating - Remove | $HOME/scripts/qtile/remove_floating.py"
"Group Match - Add | $HOME/scripts/qtile/update_group_match.py"
"Group Match - Remove | $HOME/scripts/qtile/remove_group_match.py"
"Search - Add | $HOME/scripts/rofi/search_add.sh"
"Search - Remove | $HOME/scripts/rofi/search_remove.sh"
"Config - Add | $HOME/scripts/rofi/config_file_add.sh"
"Config - Remove | $HOME/scripts/rofi/config_file_remove.sh"
"Push - Add | $HOME/scripts/rofi/config_file_remove.sh"
"Push - Remove | $HOME/scripts/rofi/config_file_remove.sh"
"Files - Save [$files_last_update] | $HOME/scripts/term/save_files.sh"
"Files - Revert | $HOME/scripts/rofi/config_file_remove.sh"
"Push - TDDD78 | $HOME/scripts/rofi/config_file_remove.sh"
)

display_options=$(printf '%s\n' "${options[@]}" | cut -d'|' -f1-1)
choice=$(printf '%s\n' "${display_options[@]}" | rofi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-3-automation'.rasi -dmenu -i -l 5 -p '' )

if [[ "$choice" == "Quit" ]]; then
    echo "Program terminated." && exit 1
elif [ "$choice" ]; then 
    for option in "${options[@]}"; do
        option_formated=$(echo "$option" | cut -d'|' -f1-1)
        file_format=$(echo "$option" | grep -oE '.py$')
        if [[ "$option_formated" == "$choice"* ]]; then
            file_path=$(echo "$option" | cut -d'|' -f2-)
            if [[ "$file_format" == ".py" ]]; then
                python $file_path
                break
            else
                bash $file_path
                break
            fi
        fi
    done
else
    echo "Program terminated." && exit 1
fi