#!/bin/bash

/home/jonalm/scripts/other/check_internet.sh
internet_status=$?

if [ $internet_status -eq 1 ]; then
  exit 1
fi

git_path="/home/jonalm/laptopgit/Laptop"
json_file="/home/jonalm/scripts/rofi/automation/save_files_data.json"
current_date_time=$(date "+%Y-%m-%d %H:%M:%S")
old_date=$(date "+%Y-%m-%d %H:%M:%S")

if test -f "$json_file"; then
  old_date=$(jq -r '.date' "$json_file")
  old_number=$(jq '.number' "$json_file")
  new_number=$((old_number + 1))
else
  new_number=1
  echo "{ \"number\": $new_number, \"date\": \"$current_date_time\", \"old_date\": \"$old_date\" }" | jq . > "$json_file"
fi

sudo rsync -av --delete /home/jonalm/laptopgit/Laptop/ /home/jonalm/laptopgit/LaptopBackup/
sudo rsync -av --delete /home/jonalm/scripts "$git_path"
sudo rsync -av --delete /home/jonalm/.config/qtile "$git_path"
sudo rsync -av --delete /home/jonalm/.config/rofi "$git_path"
sudo rsync -av --delete /home/jonalm/.config/alacritty "$git_path"
sudo rsync -av --delete /home/jonalm/.config/picom.conf "$git_path"
sudo rsync -av --delete /home/jonalm/.config/fusuma "$git_path"
sudo rsync -av --delete /home/jonalm/.config/gtk-3.0 "$git_path"
sudo rsync -av --delete /home/jonalm/.config/tmux "$git_path"
sudo rsync -av --delete /home/jonalm/.config/dunst "$git_path"
sudo rsync -av --delete /home/jonalm/.config/eww "$git_path"
sudo rsync -av --delete /home/jonalm/.imwheelrc "$git_path"
sudo rsync -av --delete /home/jonalm/.inputrc "$git_path"

cd /home/jonalm/laptopgit/Laptop/
git add --all
git commit -m "commit ${new_number}"
git push -u --force origin main

current_time="Time:$(date +'%T')"

if [ $? -eq 0 ]; then
    echo "{ \"number\": $new_number, \"date\": \"$current_date_time\", \"old_date\": \"$old_date\" }" | jq . > "$json_file"
    notify-send -a $current_time -u low -t 3000 "Files upload" "<span foreground='#a3be8c' size='medium'>Successful</span>"
  else
    notify-send -a $current_time -u critical -t 3000 "Files upload" "<span foreground='#bf616a' size='medium'>Faild</span>"
fi
