#!/bin/bash
  
source /home/jonalm/scripts/rofi/automation/automation_options.sh 

while true; do
    choice=$(printf '%s\n' "${root_options[@]}" | cut -d'|' -f1-1 | rofi -config ~/.config/rofi/files/config.rasi -theme "$HOME/.config/rofi/files/launchers/type-1/style-3-automation.rasi" -dmenu -i -l 5 -p '')
    
    if [ "$choice" ]; then
        case "$choice" in
            "  Drive")
                section_options=("${drive_options[@]}")
                rofi_path="style-3-automation-drive.rasi"
                icon=""
                ;;
            "  Floating")
                section_options=("${floating_options[@]}")
                rofi_path="style-3-automation-floating.rasi"
                icon=""
                ;;
            "  Groups")
                section_options=("${group_options[@]}")
                rofi_path="style-3-automation-groups.rasi"
                icon=""
                ;;
            "  Search")
                section_options=("${search_options[@]}")
                rofi_path="style-3-automation-search.rasi"
                icon=""
                ;;
            "  Config")
                section_options=("${config_options[@]}")
                rofi_path="style-3-automation-config.rasi"
                icon=""
                ;;
            "  Push")
                section_options=("${push_options[@]}")
                rofi_path="style-3-automation-push.rasi"
                icon=""
                ;;
            "  Files")
                section_options=("${github_files_options[@]}")
                rofi_path="style-3-automation-files.rasi"
                icon=""
                ;;
            *)
                section_options=("${display_options[@]}")  # Default to root options
                ;;
        esac

        section_choice=$(printf '%s\n' "${section_options[@]}" | cut -d'|' -f1-1 | rofi -config ~/.config/rofi/files/config.rasi -theme "$HOME/.config/rofi/files/launchers/type-1/$rofi_path" -dmenu -i -l 5 -p $icon)

        if [ "$section_choice" ]; then 
            for option in "${section_options[@]}"; do
                option_formated=$(echo "$option" | cut -d'|' -f1-1)
                file_format=$(echo "$option" | grep -oE '.py$')
                if [[ "$option_formated" == "$section_choice"* ]]; then
                    file_path=$(echo "$option" | cut -d'|' -f2-)
                    if [[ "$file_format" == ".py" ]]; then
                        python $file_path
                        exit 0
                    else
                        bash $file_path
                        exit 0
                    fi
                fi
            done
        else
            echo "Returning to main menu."
        fi
    else
        echo "Program terminated." && exit 1
    fi
done