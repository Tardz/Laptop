#!/bin/sh

export DISPLAY=:0
export XAUTHORITY=/home/jonalm/.Xauthority

if [ "$1" = "connected" ]; then
    previous_state=$(cat /home/jonalm/scripts/other/previous_state.txt)
    if [ "$previous_state" != "connected" ]; then
        xrandr --output eDP --mode 2560x1440_120.00
        current_hour=$(date +'%H')
        if [ "$current_hour" -ge "20" ] || [ "$current_hour" -le "06" ]; then
            brillo -S 30
            echo $current_hour >> /home/jonalm/scripts/other/previous_state.txt
        else
            brillo -S 60
        fi
        echo connected >> /home/jonalm/scripts/other/previous_state.txt
    fi
elif [ "$1" = "disconnected" ]; then
    xrandr --output eDP --mode 2560x1440_60.00
    brillo -S 10
    rm "/home/jonalm/scripts/other/previous_state.txt"
fi
