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
if ! git pull; then
    notify-send -a $current_time -u low -t 3000 "Files sync from laptop" "<span foreground='#d08770' size='medium'>Local and remote already synced</span>"
    exit 1
fi

sudo rsync -av --delete "$git_path/" "$HOME/laptopgit/LaptopBackup/"
sudo rsync -av --delete "$git_path/scripts/" "$HOME/scripts/"
sudo rsync -av --delete "$git_path"/qtile/settings.py $HOME/.config/qtile/settings.py
sudo rsync -av --delete "$git_path"/qtile/config.py $HOME/.config/qtile/config.py
sudo rsync -av --delete "$git_path"/qtile/functions.py $HOME/.config/qtile/functions.py
sudo rsync -av --delete "$git_path"/qtile/keybindings.py $HOME/.config/qtile/keybindings.py
sudo rsync -av --delete "$git_path"/qtile/groups.py $HOME/.config/qtile/groups.py
sudo rsync -av --delete "$git_path"/qtile/widgets.py $HOME/.config/qtile/widgets.py
sudo rsync -av --delete "$git_path"/qtile/bars.py $HOME/.config/qtile/bars.py
sudo rsync -av --delete "$git_path"/qtile/layouts.py $HOME/.config/qtile/layouts.py
sudo rsync -av --delete "$git_path"/fish/config.fish $HOME/.config/fish/config.fish
sudo rsync -av --delete "$git_path"/sddm/theme.conf /usr/share/sddm/themes/sugar-candy/

current_time="Time:$(date +'%T')"

if [ $? -eq 0 ]; then
    notify-send -a $current_time -u low -t 3000 "Files sync from laptop" "<span foreground='#a3be8c' size='medium'>Successful</span>"
  else
    notify-send -a $current_time -u critical -t 3000 "Files sync from laptop" "<span foreground='#bf616a' size='medium'>Faild</span>"
fi
