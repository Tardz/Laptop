#!/bin/bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
excludeListPath="$script_dir/exclude-in-scripts.txt"

$HOME/scripts/other/check_internet.sh
internet_status=$?

if [ $internet_status -eq 1 ]; then
  exit 1
fi

git_path="$HOME/laptopgit/Laptop"
cd "$git_path"
git pull

sudo rsync -av --delete "$git_path" $HOME/laptopgit/LaptopBackup/
sudo rsync -av --delete scripts $HOME/scripts/
sudo rsync -av --delete qtile/settings.py $HOME/.config/qtile/
sudo rsync -av --delete qtile/config.py $HOME/.config/qtile/

current_time="Time:$(date +'%T')"

if [ $? -eq 0 ]; then
    notify-send -a $current_time -u low -t 3000 "Files upload" "<span foreground='#a3be8c' size='medium'>Successful</span>"
  else
    notify-send -a $current_time -u critical -t 3000 "Files upload" "<span foreground='#bf616a' size='medium'>Faild</span>"
fi
