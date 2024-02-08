#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
excludeListPath="$HOME/scripts/rofi/automation/exclude-in-scripts.txt"

$HOME/scripts/other/check_internet.sh
internet_status=$?

if [ $internet_status -eq 1 ]; then
  exit 1
fi

git_path="$HOME/laptopgit/Laptop"

sudo rsync -av --delete "$git_path" $HOME/laptopgit/LaptopBackup/
sudo rsync --exclude-from="$excludeListPath" -av --delete $HOME/scripts "$git_path"

sudo rsync -av --delete $HOME/.config/qtile/settings.py "$git_path"/qtile/settings.py
sudo rsync -av --delete $HOME/.config/qtile/config.py "$git_path"/qtile/config.py
sudo rsync -av --delete $HOME/.config/qtile/functions.py "$git_path"/qtile/functions.py
sudo rsync -av --delete $HOME/.config/qtile/keybindings.py "$git_path"/qtile/keybindings.py
sudo rsync -av --delete $HOME/.config/qtile/groups.py "$git_path"/qtile/groups.py
sudo rsync -av --delete $HOME/.config/qtile/widgets.py "$git_path"/qtile/widgets.py
sudo rsync -av --delete $HOME/.config/qtile/bars.py "$git_path"/qtile/bars.py
sudo rsync -av --delete $HOME/.config/qtile/layouts.py "$git_path"/qtile/layouts.py
sudo rsync -av --delete /usr/share/sddm/themes/sugar-candy/theme.conf "$git_path"/sddm/

cd "$git_path"
git add --all
git commit -m "Bisync from desktop"
git push -u --force origin main

current_time="Time:$(date +'%T')"

if [ $? -eq 0 ]; then
    notify-send -a $current_time -u low -t 3000 "Files bisync to laptop" "<span foreground='#a3be8c' size='medium'>Successful</span>"
  else
    notify-send -a $current_time -u critical -t 3000 "Files bisync to laptop" "<span foreground='#bf616a' size='medium'>Faild</span>"
fi
