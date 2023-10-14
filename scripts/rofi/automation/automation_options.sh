files_last_update=$(jq -r '.date' "/home/jonalm/scripts/rofi/automation/save_files_data.json")
files_prev_update=$(jq -r '.old_date' "/home/jonalm/scripts/rofi/automation/save_files_data.json")

declare -a root_options=(
"  Drive"
"  Floating"
"  Groups"
"  Search"
"  Config"
"  Push"
"  Files"
)

declare -a drive_options=(
"  Sync | $HOME/scripts/drive/sync_drive.sh"
"  Bisync | $HOME/scripts/drive/bisync_drive.sh"
)

declare -a floating_options=(
"+ Add | $HOME/scripts/qtile/floating/update_floating.sh"
"- Remove | $HOME/scripts/qtile/floating/remove_floating.sh"
)

declare -a group_options=(
"+ Add | $HOME/scripts/qtile/groups/update_group_match.sh"
"- Remove | $HOME/scripts/qtile/groups/remove_group_match.sh"
)

declare -a search_options=(
"+ Add | $HOME/scripts/rofi/search/search_add.sh"
"- Remove | $HOME/scripts/rofi/search/search_remove.sh"
)

declare -a config_options=(
"+ Add | $HOME/scripts/rofi/config/config_file_add.sh"
"- Remove | $HOME/scripts/rofi/config/config_file_remove.sh"
)

declare -a push_options=(
"+ Add | $HOME/scripts/rofi/config_file_remove.sh"
"- Remove | $HOME/scripts/rofi/config_file_remove.sh"
)

declare -a github_files_options=(
"  Save [$files_last_update] | $HOME/scripts/rofi/automation/save_files.sh"
"  Revert [$files_prev_update] | $HOME/scripts/rofi/config_file_remove.sh"
)