#!/bin/bash

git_path="/home/jonalm/laptopgit/Laptop"
json_file="/home/jonalm/scripts/rofi/automation/save_files_data.json"
current_date_time=$(date "+%Y-%m-%d %H:%M:%S")

echo "$current_date_time"
if test -f "$json_file"; then
  old_number=$(jq '.number' "$json_file")
  new_number=$((old_number + 1))
else
  new_number=1
  echo "{ \"number\": $new_number, \"date\": \"$current_date_time\" }" | jq . > "$json_file"
fiawdawd

sudo cp -rf /home/jonalm/laptopgit/Laptop/ /home/jonalm/laptopgit/LaptopBackup/
sudo cp -rf /home/jonalm/scripts "$git_path"
sudo cp -rf /home/jonalm/.config/qtile "$git_path"
sudo cp -rf /home/jonalm/.config/rofi "$git_path"
sudo cp -rf /home/jonalm/.config/alacritty "$git_path"
sudo cp -rf /home/jonalm/.config/picom.conf "$git_path"
sudo cp -rf /home/jonalm/.imwheelrc "$git_path"
sudo cp -rf /home/jonalm/.inputrc "$git_path"
sudo cp -rf /home/jonalm/.doom.d "$git_path"

cd /home/jonalm/laptopgit/Laptop/
git add --all
git commit -m "commit ${new_number}"
git push -f origin main


if [ $? -eq 0 ]; then
  echo "{ \"number\": $new_number, \"date\": \"$current_date_time\" }" | jq . > "$json_file"
  echo "Commit successful!"
else
  echo "Commit failed!"
fi