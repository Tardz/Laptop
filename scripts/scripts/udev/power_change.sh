#!/bin/sh

export DISPLAY=:0
export XAUTHORITY=/home/jonalm/.Xauthority
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/1001/bus"

if [ "$1" = "connected" ]; then
    previous_state=$(cat /home/jonalm/scripts/udev/previous_state.txt)
    if [ "$previous_state" != "connected" ]; then
        asusctl profile --profile-set performance
        xrandr --output eDP --mode 2560x1440_120.00
        current_hour=$(date +'%H')
        if [ "$current_hour" -ge "22" ] || [ "$current_hour" -le "06" ]; then
            brillo -S 30
            redshift -P -O 4500
            dbus-launch dunstify -u low -t 3000 '-h' "int:transient:1" "Power connected" "Display set to 30%\nRedshift enabled\n<span foreground='#a3be8c' size='medium'>Charging</span>"
        else
            brillo -S 60
            dbus-launch dunstify -u low -t 3000 '-h' "int:transient:1" "Power connected" "Display set to 60%\n<span foreground='#a3be8c' size='medium'>Charging</span>"
        fi
        echo connected >> /home/jonalm/scripts/udev/previous_state.txt
    fi
elif [ "$1" = "disconnected" ]; then
    asusctl profile --profile-set balanced
    xrandr --output eDP --mode 2560x1440_60.00
    brillo -S 10
    dbus-launch dunstify -u low -t 3000 '-h' "int:transient:1" "Power disconnected" "Display set to 10%\n<span foreground='#bf616a' size='medium'>Discharging</span>"
    rm "/home/jonalm/scripts/udev/previous_state.txt"
fi
