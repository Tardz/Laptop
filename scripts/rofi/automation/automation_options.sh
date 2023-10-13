files_last_update=$(jq -r '.date' "/home/jonalm/scripts/rofi/automation/save_files_data.json")
files_prev_update=$(jq -r '.old_date' "/home/jonalm/scripts/rofi/automation/save_files_data.json")

declare -a options=(
"Drive - sync | $HOME/scripts/drive/sync_drive.sh"
"Drive - bisync | $HOME/scripts/drive/bisync_drive.sh"
"Floating - Add | $HOME/scripts/qtile/floating/update_floating.sh"
"Floating - Remove | $HOME/scripts/qtile/floating/remove_floating.sh"
"Group Match - Add | $HOME/scripts/qtile/groups/update_group_match.sh"
"Group Match - Remove | $HOME/scripts/qtile/groups/remove_group_match.sh"
"Search - Add | $HOME/scripts/rofi/search/search_add.sh"
"Search - Remove | $HOME/scripts/rofi/search/search_remove.sh"
"Config - Add | $HOME/scripts/rofi/config/config_file_add.sh"
"Config - Remove | $HOME/scripts/rofi/config/config_file_remove.sh"
"Push - Add | $HOME/scripts/rofi/config_file_remove.sh"
"Push - Remove | $HOME/scripts/rofi/config_file_remove.sh"
"Files - Save [$files_last_update] | $HOME/scripts/rofi/automation/save_files.sh"
"Files - Revert [$files_prev_update] | $HOME/scripts/rofi/config_file_remove.sh"
)

display_options=$(printf '%s\n' "${options[@]}" | cut -d'|' -f1-1)

export options, files_last_update, display_options