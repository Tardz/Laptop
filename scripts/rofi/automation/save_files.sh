#!/bin/bash

git_path="/home/jonalm/laptopgit/Laptop"
json_file="/home/jonalm/scripts/rofi/automation/save_files_data.json"

echo "$current_date_time"
if test -f "$json_file"; then
  old_date=$(jq '.date' "$json_file")
  old_number=$(jq '.number' "$json_file")
  new_number=$((old_number + 1))
  echo "$old_date"
  echo "$old_number"
else
  old_date=$(date "+%Y-%m-%d %H:%M:%S")
  new_number=1
  echo "{ \"number\": $new_number, \"date\": \"$current_date_time\", \"old_date\": \"$old_date\" }" | jq . > "$json_file"
fi

current_date_time=$(date "+%Y-%m-%d %H:%M:%S")

sudo cp -r /home/jonalm/laptopgit/Laptop/ /home/jonalm/laptopgit/LaptopBackup/
sudo cp -r /home/jonalm/scripts "$git_path"
sudo cp -r /home/jonalm/.config/qtile "$git_path"
sudo cp -r /home/jonalm/.config/rofi "$git_path"
sudo cp -r /home/jonalm/.config/alacritty "$git_path"
sudo cp -r /home/jonalm/.config/picom.conf "$git_path"
sudo cp -r /home/jonalm/.imwheelrc "$git_path"
sudo cp -r /home/jonalm/.inputrc "$git_path"

cd /home/jonalm/laptopgit/Laptop/
git add --all
git commit -m "commit ${new_number}"
git push -u -f origin main

if [ $? -eq 0 ]; then
  echo "{ \"number\": $new_number, \"date\": \"$current_date_time\", \"old_date\": \"$old_date\" }" | jq . > "$json_file"
  echo "Commit successful!"
else
  echo "Commit failed!"
fi
