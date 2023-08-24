### KEYBINDING VARIABLES ###
mod1           = "Alt"
mod            = "mod4"
myBrowser      = "brave"
myTerm         = "alacritty"
alttab_spawned = False

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
    ["#242831", "#242831"],     # 14 super dark background
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
]

#-UNIVERSAL
barbackground                 = colors[14]
bar_border_color              = colors[2][0]
widgetbackground              = colors[14]
textbackground                = colors[9]
    
#-SPECIFIC    
group_box_active              = colors[60]
group_box_inactive            = colors[10]
group_box_block_highlight     = colors[3]
group_box_highlight           = colors[3]
group_box_this_border         = widgetbackground
group_box_other_border        = colors[0]
group_box_foreground          = colors[2]
group_box_background          = widgetbackground
group_box_urgentborder        = colors[3]
    
sidebuttons_color             = colors[13]
cpu_color                     = colors[7]
cpu_temp_color                = colors[11]
updates_color                 = colors[13]
windowname_color              = colors[12]
volume_color                  = colors[8]
backlight_color               = colors[11]
battery_color                 = colors[4]
clock_color                   = colors[3]
layouticon_Background         = colors[14]
time_color                    = colors[26]

layout_normal_color_stack     = colors[2][0]
layout_focus_color_stack      = colors[2][0]
layout_normal_color_monadtall = colors[2][0]
layout_focus_color_monadtall  = colors[10][0]
layout_normal_color_floating  = colors[2][0]
layout_focus_color_floating   = colors[2][0]

### GROUPS ###
focus_value                = True

### FONTS ###
fnt1                       = "Font Awesome 6 Brands"
fnt2                       = "TerminessTTF Nerd Font"
fnt3                       = "FiraCode Nerd Font"
fnt1                       = "Font Awesome 6 Free Solid"

### BAR VARIABLES ###
##-UNIVERSAL
#-SIZE
icon_size                  = 18
circle_size                = 26
seperator_size             = 40
widget_default_size        = 19     

#-PADDING
circle_padding             = 0
seperator_padding          = 15
widget_default_padding     = 8     

#-WIDTH
middlewidgetwidth          = 265
seperator_line_width       = 15
widget_default_width       = [8.8, 0, 6.8, 0]

##-SPECIFIC 
#-SIZE
powerbutton_size           = 24
update_icon_size           = 25
pacs_text_size             = 19
menu_button_size           = 30
bar_size                   = 48
bar_gap_size               = -3
layouticon_scale           = 0.5

#-PADDING
powerbutton_padding        = 16
layouticon_padding         = -2
menu_button_padding        = 26

#-WIDTH
bar_width                  = 3

#-MARGIN
groupbox_margin            = 4
bar_margin                 = [6, 6, 0, 6]
 
#-UPDATE INTERVAL
cpu_update_interval        = 5
update_update_interval     = 120
backlight_update_interval  = 3
battery_update_interval    = 3
 
#-OTHER
windowname_max_chars       = 43
 
### LAYOUT VARIABLES ### 
layout_margin              = 12
layout_border_width        = 3
floating_border_width      = 3
layout_num_stacks          = 1

### QTILE SETTINGS ###
dgroups_key_binder         = None
dgroups_app_rules          = [] 
follow_mouse_focus         = True
bring_front_click          = True
cursor_warp                = False
auto_fullscreen            = True
focus_on_window_activation = "smart"
reconfigure_screens        = True
auto_minimize              = True