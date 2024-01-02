#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
excludeListPath="$HOME/scripts/rofi/automation/exclude-in-scripts.txt"

~/scripts/other/check_internet.sh
internet_status=$?

if [ $internet_status -eq 1 ]; then
  exit 1
fi

git_path="~/laptopgit/Laptop"
json_file="~/scripts/rofi/automation/save_files_data.json"
current_date_time=$(date "+%Y-%m-%d %H:%M:%S")
old_date=$(date "+%Y-%m-%d %H:%M:%S")