#!/bin/bash

sed -n '/START_KEYS/,/END_KEYS/p' ~/.config/qtile/keybindings_and_groups.py | \
    grep -v "#Key" |\
    grep -v "keys" |\
    grep -v "#-"   |\
    sed  -e "s/^[ \t]*//" -e "s/^[Key([]*//" -e "s/^[([]*//" -e "s/], / /" -e "s/"," / /" | \
    sed  -e "s/lazy.spawn(/ /" | \
    sed  -e "s/lazy.layout.down()/ /" | \
    sed  -e "s/lazy.layout.up() / /" | \
    yad --text-info --back=#282c34 --fore=#8FBCBB --geometry=800x800