#!/bin/sh

rclone sync googleDrive/ GoogleDrive:Arch-delat

bisync_exit_status=$?

if [ $bisync_exit_status -eq 0 ]; then
    notify-send -t 3000 "Drive bisync" "<span foreground='#a3be8c' size='medium'>Successful</span>"
else
    notify-send -u critical -t 3000 "Drive bisync" "<span foreground='#bf616a' size='medium'>Failed</span>"
fi
