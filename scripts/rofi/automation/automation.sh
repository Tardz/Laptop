#!/bin/bash
  
source /home/jonalm/scripts/rofi/automation/automation_options.sh 

while true; do
    choice=$(printf '%s\n' "${root_options[@]}" | cut -d'|' -f1-1 | rofi -theme "$HOME/.config/rofi/files/launchers/type-1/style-3-automation.rasi" -dmenu -i -l 6 -p '')
    
    if [ "$choice" ]; then
        case "$choice" in
            "  Drive")
                section_options=("${drive_options[@]}")
                icon=""
                ;;
            "  Floating")
                section_options=("${floating_options[@]}")
                icon=""
                ;;
            "  Groups")
                section_options=("${group_options[@]}")
                icon=""
                ;;
            "  Search")
                section_options=("${search_options[@]}")
                icon=""
                ;;
            "  Config")
                section_options=("${config_options[@]}")
                icon=""
                ;;
            "  Push")
                section_options=("${push_options[@]}")
                icon=""
                ;;
            "  Files")
                section_options=("${github_files_options[@]}")
                icon=""
                ;;
            *)
                section_options=("${display_options[@]}")  # Default to root options
                ;;
        esac

        section_choice=$(printf '%s\n' "${section_options[@]}" | cut -d'|' -f1-1 | rofi -theme "$HOME/.config/rofi/files/launchers/type-1/style-3-automation.rasi" -dmenu -i -l 6 -p $icon)

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