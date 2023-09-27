#!/bin/bash
### KEYBOARD CONF ###
setxkbmap se
### APPS ###
#alttab --restore
#xscreensaver &
#xss-lock -- xscreensaver-command --lock &
xss-lock --lock &
#polybar &
#powertop --auto-tune
nitrogen --restore &
picom -b &
fusuma &
xrandr --output eDP --mode 2560x1440 --rate 120
killall alttab
#alttab -bg '#2e3440' -fg '#d8dee9' -bc '#2e3440' -bw 18 -inact '#3b4252' -frame '#81a1c1' &
#emacs --daemon &
#imwheel -b 45 &
#nm-applet &
#blueman-applet &
