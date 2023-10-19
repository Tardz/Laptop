#!/bin/bash

# Run Rofi in "run" mode with the temporary script
chosen_option=$(rofi -show run -modi run:/home/jonalm/scripts/udev/rofi_custom_options.sh -theme /home/jonalm/.config/rofi/files/launchers/type-1/style-3-automation.rasi)

if [ -n "$chosen_option" ]; then
    echo "You chose: $chosen_option"
    exit 0
else
    echo $chosen_option
    echo "No choice was made."
fi