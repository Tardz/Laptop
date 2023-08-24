### CONF IMPORTS ###
from libqtile.config import Screen
from libqtile import hook, bar
from libqtile.lazy import lazy
from typing import List
import subprocess
import libqtile
import os

### KEYBINDING AND GROUPS IMPORTS ###
from libqtile.config import Match, Key, KeyChord, Click, Drag, ScratchPad, Group, DropDown
from libqtile.extension.dmenu import DmenuRun
from libqtile import qtile as Qtile

### BAR IMPORTS ###
from qtile_extras.widget.decorations import BorderDecoration, RectDecoration
from libqtile.widget.check_updates import CheckUpdates
from libqtile.widget.textbox import TextBox
from libqtile.widget.sep import Sep
from qtile_extras import widget
from libqtile.bar import Bar
from libqtile import bar   

### LAYOUT IMPORTS ###
from libqtile.layout.floating import Floating
from libqtile.layout.xmonad import MonadTall
from libqtile.layout.stack import Stack

### SETTINGS ###
from settings import *

### LAZY FUNCTIONS ###
@lazy.function
def spawn_brave(qtile):
    if qtile.current_group.name == "2":
        qtile.cmd_spawn("brave")
    for window in qtile.windows():
        if window.name == "Brave":
            qtile.cmd_spawn("brave")

@lazy.function
def spawn_code(qtile):
    if qtile.current_group.name == "3":
        qtile.cmd_spawn("code")

@lazy.function
def spawn_pcmanfm(qtile):
    if qtile.current_group.name == "4":
        qtile.cmd_spawn("pcmanfm")

@lazy.function
def spawn_thunderbird(qtile):
    if qtile.current_group.name == "5":
        qtile.cmd_spawn("thunderbird")

@lazy.function
def spawn_discord(qtile):
    if qtile.current_group.name == "7":
        qtile.cmd_spawn("discord")

@lazy.function
def spawn_tlpui(qtile):
    if qtile.current_group.name == "8":
        qtile.cmd_spawn("sudo tlpui")

@lazy.function
def spawn_htop(qtile):
    if qtile.current_group.name == "8":
        qtile.cmd_spawn("alacritty -e htop")

@lazy.function
def spawn_youtube(qtile):
    if qtile.current_group.name == "2":
        qtile.cmd_spawn(myBrowser + " https://www.youtube.com/")

@lazy.function
def spawn_alttab_once(qtile):
    if not alttab_spawned:
        qtile.cmd_spawn('alttab -bg "#2e3440" -fg "#d8dee9" -bc "#2e3440" -bw 18 -inact "#3b4252" -frame "#81a1c1"')

@lazy.function
def check(qtile):
    qtile.cmd_spawn("python /home/jonalm/scripts/qtile/check_and_launch_app.py " + "null")

@lazy.function
def check_youtube(qtile):
    qtile.cmd_spawn("python /home/jonalm/scripts/qtile/check_and_launch_app.py " + "youtube")

@lazy.function
def close_all_windows(qtile):
    for group in qtile.groups:
        for window in group.windows:
            window.kill()
        
### KEYBINDINGS ###
#-START_KEYS
keys = [
        #ESSENTIALS
        Key([mod], "Tab", lazy.next_layout(), desc='Toggle through layouts'),
        Key([mod], "q", lazy.window.kill(), desc='Kill active window'),
        Key([mod, "shift"], "r", lazy.restart(), lazy.spawn("/home/jonalm/scripts/term/reset_screens.sh"), desc='Restart Qtile'),
        Key([mod, "shift"], "q", lazy.shutdown(), desc='Shutdown Qtile'),
        Key([mod, "control"], "q", close_all_windows, desc='close all windows'),

        #ASUSCTL
        #Key([], "XF86Launch3", lazy.spawn("asusctl led-mode -n"), desc='Aurora key'),
        #Key([], "XF86Launch4", lazy.spawn("asusctl profile -n"), desc='Aurora key'),
        Key([], "XF86Launch1", lazy.spawn("sudo tlpui"), desc='Aurora key'),
        Key([], "XF86KbdBrightnessUp", lazy.spawn("brightnessctl --device='asus::kbd_backlight' set +1"), desc='Keyboardbrightness up'),
        Key([], "XF86KbdBrightnessDown", lazy.spawn("brightnessctl --device='asus::kbd_backlight' set 1-"), desc='Keyboardbrightness down'),

        #SCREEN
        Key([], "XF86MonBrightnessUp", lazy.spawn("sudo brillo -A 9"), desc='Increase display brightness'),
        Key([], "XF86MonBrightnessDown", lazy.spawn("sudo brillo -U 9"), desc='Increase display brightness'),
        
        #AUDIO
        # Key([], 'XF86AudioMute', lazy.spawn('ponymix toggle')),
        # Key([], 'XF86AudioRaiseVolume', lazy.spawn('ponymix increase 5')),
        # Key([], 'XF86AudioLowerVolume', lazy.spawn('ponymix decrease 5')),
        # Key([], 'XF86AudioPlay', lazy.spawn(music_cmd + 'PlayPause')),
        # Key([], 'XF86AudioNext', lazy.function(next_prev('Next'))),
        # Key([], 'XF86AudioPrev', lazy.function(next_prev('Previous'))),
        
        #SWITCH MONITOR FOCUS AND GROUPS
        Key(["control"], "Tab", spawn_alttab_once, desc='alttab'),
        Key([mod], "Right", lazy.screen.next_group(), desc='Next group right'),
        Key([mod], "Left", lazy.screen.prev_group(), desc='Next group left'),

        #WINDWOW CONTROLS  
        Key([mod], "Down", lazy.layout.down(), desc='Move focus down in current stack pane'),
        Key([mod], "Up", lazy.layout.up(), desc='Move focus up in current stack pane'),
        Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), lazy.layout.section_down(), desc='Move windows down in current stack'),
        Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), lazy.layout.section_up(), desc='Move windows up in current stack'),
        Key([mod, "control"], "Left", lazy.layout.shrink(), lazy.layout.decrease_nmaster(), desc='Shrink window'),
        Key([mod, "control"], "Right", lazy.layout.grow(), lazy.layout.increase_nmaster(), desc='Expand window'),
        Key([mod, "control"], "Down", lazy.layout.normalize(), desc='normalize window size ratios'),
        Key([mod, "control"], "Up", lazy.layout.maximize(), desc='toggle window between minimum and maximum sizes'),
        Key([mod], "f", lazy.window.toggle_floating(), desc='toggle floating'),
        Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),
        Key([mod], "z", lazy.window.toggle_minimize(), lazy.group.next_window(), desc="Minimize window"),

        #APPS
        Key([mod], "c", spawn_brave, lazy.group["2"].toscreen(), check, desc='Browser'),
        Key([mod], "n", spawn_pcmanfm, lazy.group["4"].toscreen(), check,desc='Filemanager'),
        Key([mod], "d", spawn_discord, lazy.group["7"].toscreen(), check, desc='Discord'),
        Key([mod], "v", spawn_code, lazy.group["3"].toscreen(), check, desc='VScode'),
        Key([mod], "m", spawn_thunderbird, lazy.group["5"].toscreen(), check, desc='Mail'),

        #URL
        Key([mod], "y", spawn_youtube, lazy.group["2"].toscreen(), check_youtube, desc='Youtube'),

        #TERM
        Key([mod], "h", spawn_htop, lazy.group["8"].toscreen(), desc='Htop'),
        Key([mod], "plus", lazy.spawn("/home/jonalm/scripts/term/show_keys.sh"), desc='Keybindings'),
        #Key([mod], "plus", lazy.spawn("/home/jonalm/scripts/term/show_keys.sh"), desc='Keybindings'),

        #ROFI
        Key([mod], "space", lazy.spawn("/home/jonalm/.config/rofi/files/launchers/type-1/launcher.sh"), desc='Rofi drun'),
        Key([mod], "Escape", lazy.spawn("/home/jonalm/.config/rofi/files/powermenu/type-2/powermenu.sh"), desc='Rofi powermenu'),
        Key([mod], "w", lazy.spawn("/home/jonalm/scripts/rofi/config/config_files.sh"), desc='Rofi config files'),
        Key([mod], "l", lazy.spawn("/home/jonalm/scripts/rofi/search/search_web.sh"), desc='Rofi web search'),
        Key([mod], "k", lazy.spawn("/home/jonalm/scripts/rofi/automation/automation.sh"), desc='Rofi automation scripts'),
#-END_KEYS
]
        
### GROUP SETTINGS ###
groups = [
        Group('1', label = "", matches=[ #Other
            ]), 
        Group('2', label = "", matches=[ #Browser
            Match(wm_class = ["chromium"]),
            Match(wm_class = ["brave-browser"])
                ]), 
        Group('3', label = "", matches=[ #Code
            Match(wm_class = ["code"]),
            Match(wm_class = ["jetbrains-studio"]),
            Match(wm_class = ["jetbrains-idea"]),
            ]), 
        Group('4', label = "", matches=[ #Files
            Match(wm_class = ["pcmanfm"]),
            ]), 
        Group('5', label = "", matches=[ #Mail
            Match(wm_class = ["thunderbird"]),
            ]), 
        Group('6', label = "", matches=[ #Docs
            Match(wm_class = ["libreoffice"]),
            ]), 
        Group('7', label = "", matches=[ #Social
            Match(wm_class = ["discord"]),
            ]), 
        Group('8', label = "", matches=[ #Settings
            Match(wm_class = ["lxappearance"]),
            Match(wm_class = ["tlpui"]),
            ]), 
        Group('9', label = ""), #Scratchpad
]

focus_value = True

### SCRATCHPAD ###
groups.append(ScratchPad('9', [
    DropDown('terminal', 'alacritty', warp_pointer=True, width=0.35, height=0.55, x=0.33, y=0.18, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('mixer', 'pavucontrol', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('net', 'nm-connection-editor', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('bluetooth', 'blueman-manager', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('filemanager', 'pcmanfm', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = focus_value),
    DropDown('music', 'spotify', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('todo', 'ticktick', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = focus_value),
    #DropDown('passwords', '/home/jonalm/.webcatalog/LastPass/LastPass', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=1, on_focus_lost_hide = focus_value),
    #DropDown('drive', '/home/jonalm/.webcatalog/GoogleDrive/GoogleDrive', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=1, on_focus_lost_hide = focus_value),
    #DropDown('github', '/home/jonalm/.webcatalog/GitHub/GitHub', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = focus_value),
    #DropDown('githubPushLabb', '/home/jonalm/scripts/term/gitpushlabb.sh', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = focus_value),
    #DropDown('githubPush', '/home/jonalm/scripts/term/gitpush.sh', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = focus_value)
]))

### MOVE WINDOW TO WORKSPACE AND DROPDOWNS ###
for i in groups:
    keys.extend([
        #WINDOWS
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name), desc="move focused window to group {}".format(i.name)),
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name)),
        #SCRATCHPAD
        Key([mod], "Return", lazy.group['9'].dropdown_toggle('terminal')),
        Key([mod], "s", lazy.group['9'].dropdown_toggle('music')),
        Key([mod], "r", lazy.group['9'].dropdown_toggle('todo')), 
    ])

### DRAG FLOATING LAYOUTS ###
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position() ),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
    ]

### UNICODE FUNCTIONS ###
def left_circle():
    return TextBox(
        text = "",
        foreground = widgetbackground,
        background = barbackground,
        fontsize = circle_size,
        padding = circle_padding,
    )

def right_circle():
    return TextBox(
        text="",
        foreground = widgetbackground,
        background = barbackground,
        fontsize = circle_size,
        padding = circle_padding,
    )

def seperator():
    return Sep(
        linewidth = seperator_line_width,
        foreground = widgetbackground,
        background = barbackground,
        padding = seperator_padding,
        size_percent = seperator_size,
    )

def lower_left_triangle(bg_color, fg_color):
    return TextBox(
        text='\u25e2',
        padding=-8,
        fontsize=50,
        background=bg_color,
        foreground=fg_color
        )

def left_arrow(bg_color, fg_color):
    return TextBox(
        text='\uE0B2',
        padding=0,
        fontsize=34,
        background=bg_color,
        foreground=fg_color
        )

def right_arrow(bg_color, fg_color):
    return TextBox(
        text='\uE0B0',
        padding=0,
        fontsize=34,
        background=bg_color,
        foreground=fg_color
        )

def upper_left_triangle(bg_color, fg_color):
    return TextBox(
        text="\u25E4",
        padding=-10,
        fontsize=100,
        background=bg_color,
        foreground=fg_color
        )

def upper_right_triangle(bg_color, fg_color):
    return TextBox(
        text="\u25E5",
        padding=-10,
        fontsize=100,
        background=bg_color,
        foreground=fg_color
        )

### Callbacks ###
@lazy.function
def open_rofi_search(qtile):
    qtile.cmd_spawn("/home/jonalm/scripts/rofi/search/search_web.sh")
        
@lazy.function
def open_rofi_config_files(qtile):
    qtile.cmd_spawn("/home/jonalm/scripts/rofi/config/config_files.sh")

@lazy.function
def open_rofi_automation(qtile):
    qtile.cmd_spawn("/home/jonalm/scripts/rofi/automation/automation.sh")

@lazy.function
def open_rofi_apps(qtile):
    qtile.cmd_spawn("/home/jonalm/.config/rofi/files/launchers/type-1/launcher.sh")

@lazy.function
def open_rofi_power_menu(qtile):
    qtile.cmd_spawn("/home/jonalm/.config/rofi/files/powermenu/type-2/powermenu.sh")

@lazy.function
def open_keybindings_script(qtile):
    qtile.cmd_spawn("/home/jonalm/scripts/term/show_keys.sh")

### WIDGET SETTINGS ###
widget_defaults = dict(
    font = fnt3,
    fontsize = widget_default_size,
    padding = widget_default_padding,
    background = widgetbackground,
    decorations = [
        BorderDecoration(
            colour = barbackground,
            border_width = widget_default_width,
        )
    ],
)

group_box_settings = {
    "padding": 5,
    "borderwidth": 6,
    "active": group_box_active,
    "inactive": group_box_inactive,
    "block_highlight_text_color": group_box_block_highlight,
    "highlight_color": group_box_highlight,
    "highlight_method": "block",
    "disable_drag": True,
    "rounded": True,
    "this_current_screen_border": widgetbackground,
    "other_current_screen_border": group_box_other_border,
    "this_screen_border": group_box_this_border,
    "other_screen_border": group_box_other_border,
    "foreground": group_box_foreground,
    "background": group_box_background,
    "urgent_border": group_box_urgentborder,
}

### BAR ###
top_bar = Bar([
    # GROUPBOX #
    widget.GroupBox(
        margin = groupbox_margin,
        font = fnt1,
        **group_box_settings,
    ),

    # TIME #
    widget.Spacer(
        bar.STRETCH,
        background = barbackground
    ),
    widget.Clock(
        format = "%R:%S",
        fontsize = 21,
        background = widgetbackground,
        foreground = textbackground,
    ),
    widget.Spacer(
        bar.STRETCH,
        background = barbackground
    ),

    # CPU #
    seperator(),
    widget.TextBox(
        text = " ",
        font = fnt2,
        foreground = cpu_color,
        background = widgetbackground,
        fontsize = icon_size,
    ),
    widget.CPU(
        format = '{load_percent}%',
        foreground = textbackground,
        background = widgetbackground,
        update_interval = cpu_update_interval,
    ),    

    # VOLUME #
    seperator(),
    widget.TextBox(
        text = "",
        padding = 0,
        foreground = volume_color,
        background = widgetbackground,
        font = fnt1,
        fontsize = icon_size,
    ),
    widget.PulseVolume(
        foreground = textbackground,
        background = widgetbackground,
        limit_max_volume = "True",
    ),
    
    # BATTERY #
    seperator(),
    widget.TextBox(
        text = '',
        padding = -1,
        foreground = battery_color,
        background = widgetbackground,
        font = fnt1,
        fontsize = icon_size,
    ),
    widget.Battery(
        format = '{percent:2.0%}', 
        update_interval = battery_update_interval, 
        background = widgetbackground,
        foreground = textbackground,
    ),
    # widget.TextBox(
    #     text = '',
    #     foreground = battery_color,
    #     background = widgetbackground,
    #     font = fnt1,
    #     fontsize = icon_size,
    # ),
    # widget.Battery(
    #     format = '{watt:.2f}', 
    #     update_interval = battery_update_interval, 
    #     background = widgetbackground,
    #     foreground = textbackground,
    # ),
    # widget.TextBox(
    #     text = '',
    #     foreground = battery_color,
    #     background = widgetbackground,
    #     font = fnt1,
    #     fontsize = icon_size,
    # ),
    # widget.Battery(
    #     format = '{hour:d}:{min:02d}', 
    #     update_interval = battery_update_interval, 
    #     background = widgetbackground,
    #     foreground = textbackground,
    # ),

    # BACKLIGHT #
    seperator(),
    widget.TextBox(
        text = '',
        padding = -1,
        foreground = backlight_color,
        background = widgetbackground,
        font = fnt1,
        fontsize = icon_size,
    ),
    widget.Backlight(
        backlight_name = "amdgpu_bl0",
        brightness_file = "/sys/class/backlight/amdgpu_bl0/actual_brightness",
        update_interval = backlight_update_interval, 
        background = widgetbackground,
        foreground = textbackground,
    ),

    # TIME #
    seperator(),
    widget.TextBox(
        text = "",
        padding = -1,
        font = fnt1,
        foreground = clock_color,  # fontsize=38
        background = widgetbackground,
        fontsize = icon_size,
    ),
    widget.Clock(
        format = "%a %b %d",
        background = widgetbackground,
        foreground = textbackground,
    ),

    widget.TextBox(
        text = "󰍜",
        foreground = sidebuttons_color,
        background = barbackground,
        font = fnt1,
        fontsize = menu_button_size,
        padding = menu_button_padding,
    ),
    ], 
    bar_size, 
    margin = bar_margin,
    border_width = bar_width,
    border_color = bar_border_color,
    )

bottom_bar = Bar([
    widget.CurrentLayoutIcon(
        custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
        foreground = layouticon_Background,
        background = layouticon_Background,
        padding = layouticon_padding,
        scale = layouticon_scale,
    ),

    widget.Sep(
        linewidth = 2,
        foreground = widgetbackground,
        background = widgetbackground,
        padding = 0,
        size_percent = 100
    ),

    widget.Sep(
        linewidth = 3,
        foreground = bar_border_color,
        background = widgetbackground,
        padding = 0,
        size_percent = 100
    ),

    widget.TaskList(
        padding          = 4,
        spacing          = 3,
        icon_size        = 13,
        margin           = 8,
        borderwidth      = 0,
        max_title_width  = 800,
        txt_floating     = ' 缾 ',
        txt_maximized    = ' 类 ',
        txt_minimized    = ' 絛 ',
        highlight_method = 'block',
        border           = bar_border_color,
        unfocused_border = colors[61],
        # foreground       = bar_border_color
    ),

    widget.Sep(
        linewidth = 3,
        foreground = bar_border_color,
        background = widgetbackground,
        padding = 0,
        size_percent = 100
    ),

    widget.TextBox(
        text = "",
        fontsize = 25,
        padding = 20,
        background = barbackground,
        foreground = colors[7],
        mouse_callbacks = {
            'Button1': open_rofi_apps,
        }
    ),

    widget.TextBox(
        text = "",
        fontsize = 25,
        padding = 20,
        background = barbackground,
        foreground = windowname_color,
        mouse_callbacks = {
            'Button1': open_rofi_search,
        }
    ),

    widget.TextBox(
        text = "",
        fontsize = 25,
        padding = 20,
        background = barbackground,
        foreground = volume_color,
        mouse_callbacks = {
            'Button1': open_rofi_config_files,
        }
    ),

    widget.TextBox(
        text = "",
        fontsize = 25,
        padding = 20,
        background = barbackground,
        foreground = cpu_color,
        mouse_callbacks = {
            'Button1': open_rofi_automation,
        }
    ),

    widget.TextBox(
        text = "",
        fontsize = 25,
        padding = 20,
        background = barbackground,
        foreground = cpu_temp_color,
        mouse_callbacks = {
            'Button1': open_keybindings_script,
        }
    ),

    widget.TextBox(
        text = "",
        fontsize = 25,
        padding = 20,
        background = barbackground,
        foreground = clock_color,
        mouse_callbacks = {
            'Button1': open_rofi_power_menu,
        }
    ),
    ], 
    bar_size, 
    margin = [-6, 640, 9, 640],
    # margin = [0, 6, 9, 6],
    border_width = bar_width,
    border_color = bar_border_color,
    )


### LAYOUT SETTINGS ###
layouts = [
    MonadTall(
        border_normal       = layout_normal_color_monadtall,
        border_focus        = layout_focus_color_monadtall,
        margin              = layout_margin,
        single_margin       = layout_margin,
        border_width        = layout_border_width,
        single_border_width = layout_border_width,
    ),
    Stack(
        border_normal       = layout_normal_color_stack,
        border_focus        = layout_focus_color_stack,
        margin              = layout_margin,
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
        Match(wm_class = "pavucontrol"),
        Match(wm_class = "brave"),
        Match(wm_class = "se-liu-jonal155-tetris-Tester"),
        Match(wm_class = "ticktick"),
        Match(wm_class = "se-liu-davhe786_jonal155-pong-Main"),
        Match(wm_class = "qalculate-gtk"),
        Match(wm_class = "lxappearance"),
        ])

### DECLARING WIDGET SETTINGS ###
extension_defaults = widget_defaults.copy()

### DECLARING PANEL ###
screens = [Screen(top=top_bar, bottom=bottom_bar, left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))]
        
### HOOKS ###
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])
    alttab_spawned = False

    # processes = [
    #     ["alttab -bg '#2e3440' -fg '#d8dee9' -bc '#2e3440' -bw 18 -inact '#3b4252' -frame '#81a1c1' -d 2 &"]
    # ]
    # for p in processes:
    #     subprocess.Popen(p)

wmname = "LG3D"
