declare -a options=(
'SDDM config - /etc/sddm.conf.d/'
'SDDM themes - /usr/share/sddm/themes/'
"Dunstrc - $HOME/.config/dunst"
'Udev rules - /etc/udev/rules.d/'
"Qtile config - $HOME/.config/qtile/"
"Qtile source code - /usr/lib/python3.11/site-packages/libqtile/"
"Qtile extras source code - /usr/lib/python3.11/site-packages/qtile_extras/"
"Neofetch config - $HOME/.config/neofetch/config.conf"
"Alacritty all - $HOME/.config/alacritty/"
"Alacritty config - $HOME/.config/alacritty/alacritty.toml"
"Picom config all - $HOME/.config/picom/"
"Picom config - $HOME/.config/picom/picom.conf"
"Rofi config - $HOME/.config/rofi/"
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
"Bar menus - $HOME/scripts/qtile/bar_menus/"
"Settings menu - $HOME/scripts/qtile/settings_menu/"
"Wifi menu - $HOME/scripts/qtile/bar_menus/wifi/"
"Bluetooth menu - $HOME/scripts/qtile/bar_menus/bluetooth/"
"Volume menu - $HOME/scripts/qtile/bar_menus/volume/"
"Power menu - $HOME/scripts/qtile/bar_menus/power/"
"Cpu menu - $HOME/scripts/qtile/bar_menus/cpu/"
)

display_options=$(printf '%s\n' "${options[@]}" | cut -d'-' -f1-1)
