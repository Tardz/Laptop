from libqtile.layout.floating import Floating
from libqtile.layout.xmonad import MonadTall
from libqtile.layout.stack import Stack
from libqtile.config import Match
from settings import *

layouts = [
    MonadTall(
        border_normal       = layout_normal_color_monadtall,
        border_focus        = layout_focus_color_monadtall,
        margin              = monadtall_layout_margin,
        single_margin       = stack_layout_margin,
        border_width        = layout_border_width,
        single_border_width = layout_border_width,
    ),
    Stack(
        border_normal       = layout_normal_color_stack,
        border_focus        = layout_focus_color_stack,
        margin              = stack_layout_margin,
        num_stacks          = layout_num_stacks,
        border_width        = layout_border_width,
    ),
]

### FLOATING LAYOUT SETTINGS AND ASSIGNED APPS ###
floating_layout = Floating(
    border_normal = layout_normal_color_floating,
    border_focus  = layout_focus_color_floating,
    border_width  = floating_border_width,
    float_rules   = [
        *Floating.default_float_rules,
        Match(wm_class = "nitrogen"),
        Match(wm_class = "bluetooth_menu.py"),
        Match(wm_class = "volume_menu.py"),
        Match(wm_class = "wifi_menu.py"),
        Match(wm_class = "settings_menu.py"),
        Match(wm_class = "electron"),
        Match(wm_class = "PatternRecognition"),
        Match(wm_class = "patternrecognition"),
        Match(wm_class = "VirtualBox"),
        Match(wm_class = "gnuplot"),
        Match(wm_class = "yad"),
        Match(wm_class = "TSP"),
        Match(wm_class = "blueman-applet"),
        Match(wm_class = "blueman-manager"),
        Match(wm_class = "nitrogen"),
        Match(wm_class = "pavucontrol"),
        Match(wm_class = "se-liu-jonal155-tetris-Tester"),
        Match(wm_class = "ticktick"),
        Match(wm_class = "se-liu-davhe786_jonal155-pong-Main"),
        Match(wm_class = "qalculate-gtk"),
        ])
