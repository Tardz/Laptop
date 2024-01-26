#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
excludeListPath="$HOME/scripts/rofi/automation/exclude-in-scripts.txt"

$HOME/scripts/other/check_internet.sh
internet_status=$?

if [ $internet_status -eq 1 ]; then
  exit 1
fi

git_path="$HOME/laptopgit/Laptop"
json_file="$HOME/scripts/rofi/automation/laptop_version/save_files_data.json"
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

sudo rsync -av --delete $HOME/laptopgit/Laptop/ $HOME/laptopgit/LaptopBackup/
sudo rsync -av --delete $HOME/scripts "$git_path"

sudo rsync -av --delete $HOME/.config/qtile/settings.py "$git_path"/qtile/settings.py
sudo rsync -av --delete $HOME/.config/qtile/config "$git_path"/qtile/config.py
sudo rsync -av --delete $HOME/.config/qtile/functions.py "$git_path"/qtile/functions.py
sudo rsync -av --delete $HOME/.config/qtile/keybindings.py "$git_path"/qtile/keybindings.py
sudo rsync -av --delete $HOME/.config/qtile/groups.py "$git_path"/qtile/groups.py
sudo rsync -av --delete $HOME/.config/qtile/widgets.py "$git_path"/qtile/widgets.py
sudo rsync -av --delete $HOME/.config/qtile/bars.py "$git_path"/qtile/bars.py
sudo rsync -av --delete $HOME/.config/qtile/layouts.py "$git_path"/qtile/layouts.py
sudo rsync -av --delete $HOME/.config/fish/config.fish "$git_path"/fish/config.fish

sudo rsync -av --delete $HOME/.config/rofi "$git_path"
sudo rsync -av --delete $HOME/.config/alacritty "$git_path"
sudo rsync -av --delete $HOME/.config/picom "$git_path"
sudo rsync -av --delete $HOME/.config/fusuma "$git_path"
sudo rsync -av --delete $HOME/.config/dunst "$git_path"
sudo rsync -av --delete $HOME/.config/redshift "$git_path"
sudo rsync -av --delete $HOME/.config/fish "$git_path"
sudo rsync -av --delete $HOME/.imwheelrc "$git_path"
sudo rsync -av --delete $HOME/.inputrc "$git_path"
# sudo rsync -av --delete /usr/share/backgrounds/ "$git_path"

cd $HOME/laptopgit/Laptop/
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
