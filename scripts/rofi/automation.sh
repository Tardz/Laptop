#!/bin/bash
  
files_last_update=$(jq -r '.date' "/home/jonalm/scripts/term/save_files_data.json")
# files_last_update_formated="${current_date_time//\"/}"

declare -a options=(
"Floating - Add | $HOME/.config/qtile/qtile_scripts/update_floating.py"
"Floating - Remove | $HOME/.config/qtile/qtile_scripts/remove_floating.py"
"Files - Save [$files_last_update] | $HOME/scripts/term/save_files.sh"
)

display_options=$(printf '%s\n' "${options[@]}" | cut -d'|' -f1-1)

choice=$(printf '%s\n' "${display_options[@]}" | rofi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-3-automation'.rasi -dmenu -i -l 3 -p '' )

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