#!/bin/bash

git_path="$HOME/laptopgit/Laptop"
json_file="$HOME/scripts/rofi/automation/save_files_data.json"
current_date_time=$(date "+%Y-%m-%d %H:%M:%S")

echo "$current_date_time"
if test -f "$json_file"; then
  old_number=$(jq '.number' "$json_file")
  new_number=$((old_number + 1))
else
  new_number=1
  echo "{ \"number\": $new_number, \"date\": \"$current_date_time\" }" | jq . > "$json_file"

sudo cp -rf $HOME/laptopgit/Laptop/ $HOME/laptopgit/LaptopBackup/
sudo cp -rf $HOME/scripts "$git_path"
sudo cp -rf $HOME/.config/qtile "$git_path"
sudo cp -rf $HOME/.config/rofi "$git_path"
sudo cp -rf $HOME/.config/alacritty "$git_path"
sudo cp -rf $HOME/.config/picom.conf "$git_path"
sudo cp -rf $HOME/.imwheelrc "$git_path"
sudo cp -rf $HOME/.inputrc "$git_path"
sudo cp -rf $HOME/.doom.d "$git_path"

cd $HOME/laptopgit/Laptop/
git add --all
git commit -m "commit ${new_number}"
git push -f origin main


if [ $? -eq 0 ]; then
  echo "{ \"number\": $new_number, \"date\": \"$current_date_time\" }" | jq . > "$json_file"
  echo "Commit successful!"
else
  echo "Commit failed!"
fi