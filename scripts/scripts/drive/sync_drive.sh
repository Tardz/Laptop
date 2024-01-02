#!/bin/sh

/home/jonalm/scripts/other/check_internet.sh
internet_status=$?
current_time="Time:$(date +'%T')"

if [ $internet_status -eq 0 ]; then
    rclone sync GoogleDrive:Arch-delat /home/jonalm/googleDrive/

    sync_exit_status=$?

    if [ $sync_exit_status -eq 0 ]; then
        notify-send -a $current_time -u low -t 3000 "Drive sync" "<span foreground='#a3be8c' size='medium'>Successful</span>"
    else
        notify-send -a $current_time -u critical -t 3000 "Drive sync" "<span foreground='#bf616a' size='medium'>Failed</span>"
    fi
else
    exit 1
fi