files_last_update=$(jq -r '.date' "/home/jonalm/scripts/rofi/automation/save_files_data.json")

declare -a options=(
"Floating - Add | $HOME/scripts/qtile/update_floating.py"
"Floating - Remove | $HOME/scripts/qtile/remove_floating.py"
"Group Match - Add | $HOME/scripts/qtile/update_group_match.py"
"Group Match - Remove | $HOME/scripts/qtile/remove_group_match.py"
"Search - Add | $HOME/scripts/rofi/search/search_add.sh"
"Search - Remove | $HOME/scripts/rofi/search/search_remove.sh"
"Config - Add | $HOME/scripts/rofi/config/config_file_add.sh"
"Config - Remove | $HOME/scripts/rofi/config/config_file_remove.sh"
"Push - Add | $HOME/scripts/rofi/config_file_remove.sh"
"Push - Remove | $HOME/scripts/rofi/config_file_remove.sh"
"Files - Save [$files_last_update] | $HOME/scripts/rofi/automation/save_files.sh"
"Files - Revert | $HOME/scripts/rofi/config_file_remove.sh"
"Push - TDDD78 | $HOME/scripts/rofi/config_file_remove.sh"
)

display_options=$(printf '%s\n' "${options[@]}" | cut -d'|' -f1-1)

export options, files_last_update, display_options