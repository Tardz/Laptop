#!/bin/bash

DMEDITOR="alacritty -e code -n"

declare -a options=(
"Qtile config all - $HOME/.config/qtile/"
"Qtile config - $HOME/.config/qtile/config.py"
"Qtile autostart - $HOME/.config/qtile/autostart.sh"
"Neofetch config - $HOME/.config/neofetch/config.conf"
"Alacritty config - $HOME/.config/alacritty/alacritty.yml"
"Picom config - $HOME/.config/picom.conf"
"Bashrc - $HOME/.bashrc"
"Xinitrc - $HOME/.xinitrc"
"Xauthority - $HOME/.Xauthority"
"Synth shell config - $HOME/.config/synth-shell/synth-shell-prompt.config"
"Show keys script - $HOME/scripts/term/show_keys.sh"
"Rofi scripts - $HOME/scripts/rofi/"
"Qtile scripts - $HOME/.config/qtile/qtile_scripts/"
"Term scripts - $HOME/scripts/term/"
"Rofi config - $HOME/.config/rofi/"
"Doom init config - $HOME/.doom.d/init.el"
"Quit"
)

display_options=$(printf '%s\n' "${options[@]}" | cut -d'-' -f1-1)

choice=$(printf '%s\n' "${display_options[@]}" | rofi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-3-config'.rasi -dmenu -i 20 -columns 25 -p '' )

if [[ "$choice" == "Quit" ]]; then
    echo "Program terminated." && exit 1
elif [ "$choice" ]; then 
    for option in "${options[@]}"; do
        option_formated=$(echo "$option" | cut -d'-' -f1-1)
        if [[ "$option_formated" == "$choice"* ]]; then
            cfg=$(echo "${option}" | cut -d'-' -f2- )
            $DMEDITOR "$cfg"
            qtile cmd-obj -o group 3 -f toscreen
            break
        fi
    done
else
    echo "Program terminated." && exit 1
fi

