#!/bin/sh

/home/jonalm/scripts/other/check_internet.sh
internet_status=$?

if [ $internet_status -eq 0 ]; then
    rclone sync googleDrive/ GoogleDrive:Arch-delat

    sync_exit_status=$?

    if [ $sync_exit_status -eq 0 ]; then
        notify-send -t 3000 "Drive bisync" "<span foreground='#a3be8c' size='medium'>Successful</span>"
    else
        notify-send -u critical -t 3000 "Drive bisync" "<span foreground='#bf616a' size='medium'>Failed</span>"
    fi
else
    exit 1
fi