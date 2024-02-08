"""
Author: Jonathan Almstedt [Tardz]
Updated: 2023-12-29

Description: Reads values from json files contained in the settings app
specifically made for qtile, the app and the json files can be found in 
"$HOME/scripts/qtile/settings_menu". This settings file will use default 
values if no json file can be found. To be able to change the way qtile 
works and looks clone the scripts directory on https://github.com/Tardz/Laptop.git
and use the settings menu.
"""

import subprocess
import json
import os

### KEYBINDING VARIABLES ###
mod1           = "Alt"
mod            = "mod4"
myBrowser      = "brave"
myTerm         = "alacritty"
alttab_spawned = False
HOME           = os.path.expanduser("~")
active_window_name = ""

check_dict = {
    #[0] - app, [1] - command, [2] - screen
    "c": ["vivaldi", None, 0],
    "d": ["discord", None, 0],
    "v": [None, None, 1],
    "n": ["pcmanfm", None, 0],
    "m": ["thunderbird", None, 0],
    9  : []
}

### COLORS ###
colors = [
    #-Bar
    ["#2e3440", "#2e3440"],     # 0 background
    ["#d8dee9", "#d8dee9"],     # 1 foreground
    ["#3b4252", "#3b4252"],     # 2 background lighter
    ["#bf616a", "#bf616a"],     # 3 red
    ["#a3be8c", "#a3be8c"],     # 4 green
    ["#ebcb8b", "#ebcb8b"],     # 5 yellow
    ["#81a1c1", "#81a1c1"],     # 6 blue
    ["#b48ead", "#b48ead"],     # 7 magenta
    ["#88c0d0", "#88c0d0"],     # 8 cyan
    ["#e5e9f0", "#e5e9f0"],     # 9 white
    ["#4c566a", "#4c566a"],     # 10 grey
    ["#d08770", "#d08770"],     # 11 orange
    ["#8fbcbb", "#8fbcbb"],     # 12 super cyan
    ["#5e81ac", "#5e81ac"],     # 13 super blue
    ["#242831.95", "#242831.95"],     # 14 super dark background
    ["#434C5E", "#434C5E"],     # 15 darker grey
    #-Dark mode
    ["#00000000", "#00000000"], # 16 transp1
    ["#99000000", "#99000000"], # 17 transp2
    ["#ffffff", "#ffffff"],     # 18 text
    ["#000000", "#000000"],     # 19 text2
    ["#282828", "#282828"],     # 20 background
    ["#cc241d", "#cc241d"],     # 21 red
    ["#EA738DFF", "#EA738DFF"], # 22 red2
    ["#98971a", "#98971a"],     # 23 green
    ["#d79921", "#d79921"],     # 24 yellow
    ["#458588", "#458588"],     # 25 blue
    ["#89ABE3FF", "#89ABE3FF"], # 26 blue2
    ["#008080", "#008080"],     # 27 blue3
    ["#2F4F4F", "#2F4F4F"],     # 28 blue4
    ["#b16286", "#b16286"],     # 29 purple
    ["#a9a1e1", "#a9a1e1"],     # 30 purple2
    ["#689d61", "#689d61"],     # 31 aqua
    ["#928374", "#928374"],     # 32 grey
    ["#689d61", "#689d61"],     # 33 aqua
    ["#d65d0e", "#d65d0e"],     # 34 orange
    ["#E7E8D1", "#E7E8D1"],     # 35 olive
    ["#A7BEAE", "#A7BEAE"],     # 36 teal
    ["#a89984", "#a89984"],     # 37 lightgrey
    ["#fb4934", "#fb4934"],     # 38 lightred
    ["#b8bb26", "#b8bb26"],     # 39 lightgreen
    ["#fabd2f", "#fabd2f"],     # 40 lightyellow
    ["#83a598", "#83a598"],     # 41 lightblue
    ["#d3869d", "#d3869d"],     # 42 lightpurple
    ["#8ec07c", "#8ec07c"],     # 43 lightaqua
    ["#fe8019", "#fe8019"],     # 44 lightorange
    ["#7daea3", "#7daea3"],     # 45 darkblue
    ["#1d2021", "#1d2021"],     # 46 bg0
    ["#32302f", "#32302f"],     # 47 bg1
    ["#282828", "#282828"],     # 48 bg2
    ["#3c3836", "#3c3836"],     # 49 bg3
    ["#504945", "#504945"],     # 50 bg4
    ["#665c54", "#665c54"],     # 51 bg5
    ["#7c6f64", "#7c6f64"],     # 52 bg6
    ["#928374", "#928374"],     # 53 bg7
    ["#bdae93", "#bdae93"],     # 54 fg0
    ["#d5c4a1", "#d5c4a1"],     # 55 fg1
    ["#ebdbb2", "#ebdbb2"],     # 56 fg2
    ["#fbf1c7", "#fbf1c7"],     # 57 fg3
    #-More nord
    ["#ff726f", "#ff726f"],     # 58 nordlightred
    ["#ffcccb", "#ffcccb"],     # 59 nordlightrred
    ["#ECEFF4", "#ECEFF4"],     # 60 nordwhite1
    ["#2e3441", "#2e3441"],     # 61 darker grey
    ["#000000AA", "#000000AA"], # 63 Transp
]

qtile_settings = {}
file_path = os.path.expanduser("~/settings_data/qtile_data.json")
if os.path.isfile(file_path):
    with open(file_path, "r") as file:
        qtile_settings = json.load(file)

qtile_colors = {}
file_path = os.path.expanduser("~/settings_data/qtile_colors.json")
if os.path.isfile(file_path):
    with open(file_path, "r") as file:
        qtile_colors = json.load(file)

laptop = qtile_settings.get("laptop_version", False)

file_path = os.path.expanduser("~/settings_data/processes.json")
if os.path.isfile(file_path):
    with open(file_path, "r") as file:
        processes = json.load(file)

volume_menu_pid = processes.get("volume_menu_pid", None)
bluetooth_menu_pid = processes.get("bluetooth_menu_pid", None)
wifi_menu_pid = processes.get("wifi_menu_pid", None)

icon_theme_name = subprocess.check_output(
    "cat " + 
    os.path.expanduser("~/.config/gtk-3.0/settings.ini") + 
    " | grep -e gtk-icon-theme-name | awk -F '=' '{print $2}' | tr -d '[:space:]'", shell=True
    ).decode("utf-8")
current_icon_theme_path = "/usr/share/icons/" + icon_theme_name + "/scalable/"

if laptop:
    top_bar_scaling                 = 1
    bottom_bar_scaling              = 1
    icon_size_scaling               = 1
    icon_padding_scaling            = 1
    widget_padding_scaling          = 1
    widget_size_scaling             = 1
    seperator_padding_scaling       = 1
    seperator_line_scaling          = 1
    general_width_scaling           = 1
    task_list_scaling               = 1
    gap_scaling                     = 0
else:
    top_bar_scaling                 = 0.7
    bottom_bar_scaling              = 1
    icon_size_scaling               = 0.55
    icon_padding_scaling            = 0.65
    widget_padding_scaling          = 0.7
    widget_size_scaling             = 0.74
    seperator_padding_scaling       = 0.9
    seperator_line_scaling          = 0.6
    general_width_scaling           = 0.9
    task_list_scaling               = 0.9
    gap_scaling                     = 3

#*###############################
#*           BAR               ##
#*###############################
#?#############
#?   STYLE   ##
#?#############
# Styles are: "simple_1", "simple_2"
bar_style = qtile_settings.get("bar_style", "simple_1")
darkmode = qtile_settings.get("darkmode", True)

#?#############
#?   COLORS  ##
#?#############
#!ALL
transparent                         = "#000000.0"
icon_background                     = "#1e2227"
text_color                          = "#b5b7c3"
widget_default_foreground_color     = colors[9]

group_box_active_color              = colors[60]
group_box_inactive_color            = colors[10]
group_box_block_highlight_color     = colors[3]
group_box_highlight_color           = colors[3]
group_box_other_border_color        = transparent
group_box_foreground_color          = colors[2]
group_box_background_color          = colors[3]
group_box_highlight_text_color      = colors[3]
group_box_urgentborder_color        = colors[3]

if bar_style == "simple_2":
    icon_background_1                   = "#b48ead"
    icon_background_2                   = "#9B98B7"
    icon_background_3                   = "#81A1C1"
    icon_background_4                   = "#8fbcbb"
    icon_background_5                   = "#8fbcbb"
    icon_background_6                   = "#a3be8c"
    icon_background_7                   = "#a3be8c"
    icon_background_8                   = "#d08770"
    icon_background_9                   = "#bf616a"
    icon_background_10                  = "#b48ead"
    icon_background_11                  = "#9B98B7"
    icon_background_12                  = "#81A1C1"

    icon_foreground_1                   = "#1e2227"
    icon_foreground_2                   = "#1e2227"
    icon_foreground_3                   = "#1e2227"
    icon_foreground_4                   = "#1e2227"
    icon_foreground_5                   = "#1e2227"
    icon_foreground_6                   = "#1e2227"
    icon_foreground_7                   = "#1e2227"
    icon_foreground_8                   = "#1e2227"
    icon_foreground_9                   = "#1e2227"
    icon_foreground_10                  = "#1e2227"
    icon_foreground_11                  = "#1e2227"
    icon_foreground_12                  = "#1e2227"

    if darkmode:
        right_decor_background        = "#4e576d.8"
    else:
        right_decor_background        = "#1e2227.5"
else:
    icon_background_1                   = transparent
    icon_background_2                   = transparent
    icon_background_3                   = transparent
    icon_background_4                   = transparent
    icon_background_5                   = transparent
    icon_background_6                   = transparent
    icon_background_7                   = transparent
    icon_background_8                   = transparent
    icon_background_9                   = transparent
    icon_background_10                  = transparent
    icon_background_11                  = transparent
    icon_background_12                  = transparent

    icon_foreground_color               = "#b5b7c3"

    icon_foreground_1                   = icon_foreground_color
    icon_foreground_2                   = icon_foreground_color
    icon_foreground_3                   = icon_foreground_color
    icon_foreground_4                   = icon_foreground_color
    icon_foreground_5                   = icon_foreground_color
    icon_foreground_6                   = icon_foreground_color
    icon_foreground_7                   = icon_foreground_color
    icon_foreground_8                   = icon_foreground_color
    icon_foreground_9                   = icon_foreground_color
    icon_foreground_10                  = icon_foreground_color
    icon_foreground_11                  = icon_foreground_color
    icon_foreground_12                  = icon_foreground_color

    # icon_foreground_1                   = "#b48ead"
    # icon_foreground_2                   = "#9B98B7"
    # icon_foreground_3                   = "#81A1C1"
    # icon_foreground_4                   = "#8fbcbb"
    # icon_foreground_5                   = "#8fbcbb"
    # icon_foreground_6                   = "#a3be8c"
    # icon_foreground_7                   = "#a3be8c"
    # icon_foreground_8                   = "#d08770"
    # icon_foreground_9                   = "#bf616a"
    # icon_foreground_10                  = "#b48ead"
    # icon_foreground_11                  = "#9B98B7"
    # icon_foreground_12                  = "#81A1C1"

    right_decor_background = transparent

app_tray_icon_color_1               = "#81A1C1"
app_tray_icon_color_2               = "#8fbcbb"
app_tray_icon_color_3               = "#a3be8c"
app_tray_icon_color_4               = "#d08770"
app_tray_icon_color_5               = "#bf616a"

if darkmode:
    app_tray_color                = "#31373f.85"
    app_tray_seperator_color      = "#454951.9"
    bar_border_color              = "#454951"
    bar_background_color          = "#1e2227.85"
    # right_decor_background        = "#717c99.5"
else:
    app_tray_color                = "#505a67.85"
    app_tray_seperator_color      = "#606671.9"
    bar_border_color              = "#505a67"
    bar_background_color          = "#505a67.85"

#?#############
#?  GENERAL  ##
#?#############
top_bar_on                          = qtile_settings.get("top_bar_status", True)
bottom_bar_on                       = qtile_settings.get("bottom_bar_status", True)

#?#############
#?   SIZE    ##
#?#############
#!BAR
top_bar_size                        = int(qtile_settings.get("top_bar_size", 46)*top_bar_scaling)
bottom_bar_size                     = int(qtile_settings.get("bottom_bar_size", 80)*bottom_bar_scaling)

bar_width = [] 
for num in qtile_settings.get("bar_width_top", [0, 0, 0, 0]):
    bar_width.append(int(num*general_width_scaling))

bar_width_top                       = bar_width
bar_margin_top                      = qtile_settings.get("bar_margin_top", [0, 0, 0, 0])
bar_width_bottom                    = qtile_settings.get("bar_width_bottom", [0, 0, 0 ,0])

if laptop:
    bar_margin_bottom                   = qtile_settings.get("bar_margin_bottom", [10, 657, 12, 657])
    bar_1_margin_bottom                 = qtile_settings.get("bar_1_margin_bottom", [10, 477, 12, 477])
    bar_2_margin_bottom                 = qtile_settings.get("bar_2_margin_bottom", [10, 638, 12, 638])
else:
    bar_margin_bottom                   = qtile_settings.get("bar_margin_bottom", [10, 700, 12, 700])
    bar_1_margin_bottom                 = qtile_settings.get("bar_1_margin_bottom", [10, 577, 12, 577])
    bar_2_margin_bottom                 = qtile_settings.get("bar_2_margin_bottom", [10, 638, 12, 638])

#!GAP
bar_gap_size                        = (qtile_settings.get("bar_gap_size", 0) - gap_scaling)

#!SEPERATOR
seperator_padding                   = int(qtile_settings.get("seperator_padding", 0)*seperator_padding_scaling)
seperator_line_width                = int(qtile_settings.get("seperator_line_width", 15)*seperator_line_scaling)

#!WIDGET DEFAULT
widget_default_font_size            = int(17*widget_size_scaling)
widget_default_padding              = int(6*widget_padding_scaling)
bottom_widget_width                 = int(0*general_width_scaling)

#!GROUPBOX
groupbox_margin                     = int(4*widget_padding_scaling)
groupbox_padding_y                 = int(6*widget_padding_scaling)

#!LAYOUT ICON
layouticon_padding                  = int(-2*widget_padding_scaling)
layouticon_scale                    = 0.48*widget_padding_scaling

#!ICONS
icon_size                           = int(15*icon_size_scaling)
if bar_style == "simple_1":
    icon_padding                        = int(20*icon_padding_scaling)
else:
    icon_padding                        = int(8*icon_padding_scaling)

#!DECOR
left_decor_padding                  = int(7*icon_padding_scaling)
right_decor_padding                 = int(9*icon_padding_scaling)

#!TASKLIST
task_list_margin                    = int(4*task_list_scaling)
task_list_border_width              = int(4*general_width_scaling)
task_list_spacing                   = 2
task_list_icon_size                 = 28

#*###############################
#*           FOCUS             ##
#*###############################
follow_mouse_focus                  = qtile_settings.get("follow_mouse_focus", True)
cursor_warp                         = qtile_settings.get("cursor_warp", False)
scratchpad_focus_value              = qtile_settings.get("scratchpad_focus_value", True)
focus_on_window_activation          = qtile_settings.get("focus_on_window_activation", "smart")

#*###############################
#*           WINDOWS           ##
#*###############################
auto_fullscreen                     = qtile_settings.get("auto_fullscreen", True)
auto_minimize                       = qtile_settings.get("auto_minimize", True)
bring_front_click                   = qtile_settings.get("bring_front_click", True)

#*###############################
#*           OTHER             ##
#*###############################
reconfigure_screens                 = qtile_settings.get("reconfigure_screens", False)

#*###############################
#*           lAYOUT            ##
#*###############################
#?#############
#?   COLORS  ##
#?#############
#!NORMAL
layout_normal_color_stack           = colors[2][0]
layout_normal_color_monadtall       = colors[2][0]
layout_normal_color_floating        = colors[2][0]

#!FOCUS
layout_focus_color_monadtall        = "#4b5662"
layout_focus_color_stack            = colors[2][0]
layout_focus_color_floating         = bar_border_color

#?#############
#?   SIZE    ##
#?#############
#!ALL
stack_layout_margin                 = int(6*top_bar_scaling)
monadtall_layout_margin             = int(6*top_bar_scaling)
layout_border_width                 = int(qtile_settings.get("layout_border_with", 2)*general_width_scaling)
layout_num_stacks                   = 1

#!FLOATING
floating_border_width               = int(qtile_settings.get("layout_border_with", 1)*general_width_scaling)

#*#############################
#*           FONTS           ##
#*#############################
normal_font                         = "FiraCode Nerd Font"
apple_font                          = "San Francisco"
apple_font_bold                     = "San Francisco bold"
bold_font                           = "FiraCode Nerd Font Bold"
icon_font                           = "Font Awesome 6 Free Solid"
other_font                          = "ttf-dejavu"

#*#############################
#*          UPDATES          ##
#*#############################
wifi_update_interval            = 10
cpu_update_interval             = 10
battery_update_interval         = 20
backlight_update_interval       = 20
