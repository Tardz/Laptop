#!/bin/bash

git_path="/home/jonalm/laptopgit/Laptop"

json_file="/home/jonalm/scripts/term/commit_number.json"

if test -f "$json_file"; then
  current_number=$(jq '.number' "$json_file")
  new_number=$((current_number + 1))
else
  new_number=1
  echo "{ \"number\": $new_number }" | jq . > "$json_file"
fi

sudo cp -r /home/jonalm/laptopgit/Laptop/ /home/jonalm/laptopgit/LaptopBackup/
sudo cp -r /home/jonalm/scripts "$git_path"
sudo cp -r /home/jonalm/.config/qtile "$git_path"
sudo cp -r /home/jonalm/.config/rofi "$git_path"
sudo cp -r /home/jonalm/.config/alacritty "$git_path"
sudo cp -r /home/jonalm/.config/picom.conf "$git_path"
sudo cp -r /home/jonalm/.imwheelrc "$git_path"
sudo cp -r /home/jonalm/.inputrc "$git_path"
sudo cp -r /home/jonalm/.Xauthority "$git_path"
sudo cp -r /home/jonalm/.inputrc "$git_path"
sudo cp -r /home/jonalm/.doom.d "$git_path"

cd /home/jonalm/laptopgit/Laptop/
git add --all
git commit -m "commit ${new_number}"
git push -u -f origin main

if [ $? -eq 0 ]; then
  echo "{ \"number\": $new_number }" | jq . > "$json_file"
  echo "Commit successful!"
else
  echo "Commit failed!"
fi
