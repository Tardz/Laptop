declare -a options=(
'SDDM config - /etc/sddm.conf.d/'
'SDDM themes - /usr/share/sddm/themes/'
"Dunstrc - $HOME/.config/dunst"
'Udev rules - /etc/udev/rules.d/'
"Qtile config all - $HOME/.config/qtile/"
"Qtile config - $HOME/.config/qtile/config.py"
"Qtile autostart - $HOME/.config/qtile/autostart.sh"
"Neofetch config - $HOME/.config/neofetch/config.conf"
"Alacritty config - $HOME/.config/alacritty/alacritty.yml"
"Picom config - $HOME/.config/picom.conf"
"Doom init config - $HOME/.doom.d/init.el"
"Synth shell config - $HOME/.config/synth-shell/synth-shell-prompt.config"
"Bashrc - $HOME/.bashrc"
"Xinitrc - $HOME/.xinitrc"
"Xauthority - $HOME/.Xauthority"
"Show keys script - $HOME/scripts/term/show_keys.sh"
"Rofi scripts - $HOME/scripts/rofi/"
"Qtile scripts - $HOME/scripts/qtile/"
"Term scripts - $HOME/scripts/term/"
"Generall scripts - $HOME/scripts/"
"Rofi config - $HOME/.config/rofi/"
)

display_options=$(printf '%s\n' "${options[@]}" | cut -d'-' -f1-1)
