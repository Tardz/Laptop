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
from libqtile.widget import base
from qtile_extras import widget
from libqtile.bar import Bar
from libqtile import bar   


### LAYOUT IMPORTS ###
from libqtile.layout.floating import Floating
from libqtile.layout.xmonad import MonadTall
from libqtile.layout.stack import Stack

### SETTINGS ###
from settings import *

### LAZY FUNCTIONS FOR SHORTCUTS ###
@lazy.function
def move_focus_and_mouse(qtile, monitor = 0):
    if not single_monitor:
        qtile.cmd_to_screen(monitor)
        if monitor == 0:
            qtile.cmd_spawn("xdotool mousemove 950 500")
        elif monitor == 1:
            qtile.cmd_spawn("xdotool mousemove 2900 500")

@lazy.function
def spawn_alttab_once(qtile):
    if not alttab_spawned:
        qtile.cmd_spawn('alttab -bg "#2e3440" -fg "#d8dee9" -bc "#2e3440" -bw 18 -inact "#3b4252" -frame "#81a1c1"')

@lazy.function
def check(qtile, app, group, command = ""):
    qtile.cmd_spawn(["/home/jonalm/scripts/qtile/check_and_launch_app.py", app, group, command])

@lazy.function
def close_all_windows(qtile):
    for group in qtile.groups:
        for window in group.windows:
            window.kill()

@lazy.function
def mute_or_unmute(qtile):
    qtile.cmd_spawn("/home/jonalm/scripts/qtile/mute_or_unmute.sh")

### KEYBINDINGS ###
#- KEYS_START 
keys = [
        #--[ESSENTIALS]--#
        Key([mod], "Tab", lazy.next_layout(), desc='Toggle through layouts'),
        Key([mod], "q", lazy.window.kill(), desc='Kill active window'),
        Key([mod, "shift"], "r", lazy.restart(), lazy.spawn("/home/jonalm/scripts/term/reset_screens.sh"), desc='Restart Qtile'),
        Key([mod, "shift"], "q", lazy.shutdown(), desc='Shutdown Qtile'),
        Key([mod, "control"], "q", close_all_windows, desc='close all windows'),
        KeyChord([mod], "x", [
            Key([], "u", lazy.spawn("sudo systemctl poweroff")),
            Key([], "s", lazy.spawn("sudo systemctl suspend")),
            Key([], "r", lazy.spawn("sudo systemctl reboot")),
            Key([], "h", lazy.spawn("sudo systemctl hibernate")),
        ]),

        #--[ASUSCTL]--#
        Key([], "XF86Launch1", lazy.spawn("sudo tlpui"), desc='Aurora key'),
        Key([], "XF86KbdBrightnessUp", lazy.spawn("brightnessctl --device='asus::kbd_backlight' set +1"), desc='Keyboardbrightness up'),
        Key([], "XF86KbdBrightnessDown", lazy.spawn("brightnessctl --device='asus::kbd_backlight' set 1-"), desc='Keyboardbrightness down'),

        #--[SCREEN]--#
        Key([], "XF86MonBrightnessUp", lazy.spawn("sudo brillo -A 9"), desc='Increase display brightness'),
        Key([], "XF86MonBrightnessDown", lazy.spawn("sudo brillo -U 9"), desc='Increase display brightness'),        
        
        #--[AUDIO]--#
        Key([], 'XF86AudioMute', mute_or_unmute),
        Key([], 'XF86AudioRaiseVolume', lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ +5%')),
        Key([], 'XF86AudioLowerVolume', lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ -5%')),
        
        #--[SWITCH MONITOR FOCUS AND GROUPS]--#
        Key(["control"], "Tab", spawn_alttab_once, desc='alttab'),
        Key([mod], "Right", lazy.screen.next_group(), desc='Next group right'),
        Key([mod], "Left", lazy.screen.prev_group(), desc='Next group left'),

        #--[WINDWOW CONTROLS]--#
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

        #--[APPS]--#
        Key([mod], "c", move_focus_and_mouse(1), lazy.group["1"].toscreen(), check("brave", "1"), desc='Browser'),
        Key([mod], "n", move_focus_and_mouse(1), lazy.group["3"].toscreen(), check("ranger", "3", "alacritty --title Ranger -e"), desc='Filemanager'),
        Key([mod], "d", move_focus_and_mouse(1), lazy.group["4"].toscreen(), check("discord", "4"), desc='Discord'),
        Key([mod], "v", move_focus_and_mouse(0), lazy.group["2"].toscreen(), desc='VScode'),
        Key([mod], "m", move_focus_and_mouse(1), lazy.group["3"].toscreen(), check("thunderbird", "3"), desc='Mail'),

        #--[URLS]--#
        Key([mod], "y", move_focus_and_mouse(1), lazy.group["1"].toscreen(), check("youtube.com", "1", "brave"), desc='Youtube'),

        #--[TERM]--#
        Key([mod], "h", move_focus_and_mouse(0), lazy.group["3"].toscreen(), check("htop", "3", "alacritty --title Htop -e"), desc='Htop'),
        Key([mod], "plus", lazy.spawn("/home/jonalm/scripts/term/show_keys.sh"), desc='Keybindings'),

        #--[ROFI]--#
        Key([mod], "space", lazy.spawn("/home/jonalm/.config/rofi/files/launchers/type-1/launcher.sh"), desc='Rofi drun'),
        Key([mod], "Escape", lazy.spawn("/home/jonalm/.config/rofi/files/powermenu/type-2/powermenu.sh"), desc='Rofi powermenu'),
        Key([mod], "w", lazy.spawn("/home/jonalm/scripts/rofi/config/config_files.sh"), desc='Rofi config files'),
        Key([mod], "l", lazy.spawn("/home/jonalm/scripts/rofi/search/search_web.sh"), desc='Rofi web search'),
        Key([mod], "k", lazy.spawn("/home/jonalm/scripts/rofi/automation/automation.sh"), desc='Rofi automation scripts'),
#- KEYS_END
]

### GROUP SETTINGS ###
groups = [
        Group('1', label = "", matches=[ #Browser
            Match(wm_class = ["chromium"]),
            Match(wm_class = ["brave-browser"]),
                ]), 
        Group('2', label = "", matches=[ #Code
            Match(wm_class = ["code"]),
            Match(wm_class = ["jetbrains-clion"]),
            Match(wm_class = ["jetbrains-studio"]),
            Match(wm_class = ["jetbrains-idea"]),
            ]), 
        Group('3', label = "", matches=[ #Files
            Match(wm_class = ["pcmanfm"]),
            Match(wm_class = ["thunderbird"]),
            Match(wm_class = ["lxappearance"]),
            Match(wm_class = ["tlpui"]),
            ]), 
        Group('4', label = "", matches=[ #Social
            Match(wm_class = ["discord"]),
            ]), 
        Group('9', label = ""), #Scratchpad

]

# groups = [
#         Group('1', label = "", matches=[ #Other
#             ]), 
#         Group('2', label = "", matches=[ #Browser
#             Match(wm_class = ["chromium"]),
#             Match(wm_class = ["brave-browser"]),
#                 ]), 
#         Group('3', label = "", matches=[ #Code
#             Match(wm_class = ["code"]),
#             Match(wm_class = ["jetbrains-clion"]),
#             Match(wm_class = ["jetbrains-studio"]),
#             Match(wm_class = ["jetbrains-idea"]),
#             ]), 
#         Group('4', label = "", matches=[ #Files
#             Match(wm_class = ["pcmanfm"]),
#             ]), 
#         Group('5', label = "", matches=[ #Mail
#             Match(wm_class = ["thunderbird"]),
#             ]), 
#         Group('6', label = "", matches=[ #Docs
#             Match(wm_class = ["libreoffice"]),
#             ]), 
#         Group('7', label = "", matches=[ #Social
#             Match(wm_class = ["discord"]),
#             ]), 
#         Group('8', label = "", matches=[ #Settings
#             Match(wm_class = ["lxappearance"]),
#             Match(wm_class = ["tlpui"]),
#             ]), 
#         Group('9', label = ""), #Scratchpad

# ]

### SCRATCHPAD ###
groups.append(ScratchPad('9', [
    DropDown('terminal', 'alacritty --title alacritty', warp_pointer=True, width=0.35, height=0.55, x=0.33, y=0.18, opacity=1, on_focus_lost_hide = scratchpad_focus_value),
    DropDown('mixer', 'pavucontrol', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = scratchpad_focus_value),
    DropDown('net', 'nm-connection-editor', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = scratchpad_focus_value),
    DropDown('bluetooth', 'blueman-manager', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = scratchpad_focus_value),
    DropDown('filemanager', 'pcmanfm', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = scratchpad_focus_value),
    DropDown('music', 'spotify', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=1, on_focus_lost_hide = scratchpad_focus_value),
    DropDown('todo', 'ticktick', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = scratchpad_focus_value),
]))

### MOVE WINDOW TO WORKSPACE AND DROPDOWNS ###
for i in groups:
    keys.extend([
#- SCRATCHPAD_KEYS_START

        #--[WINDOWS]--#
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name), desc="move focused window to group {}".format(i.name)),
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name)),
        #--[SCRATCHPAD]--#
        Key([mod], "Return", lazy.group['9'].dropdown_toggle('terminal'), desc='Terminal'),
        Key([mod], "period", lazy.group['9'].dropdown_toggle('mixer'), desc='Volume'),
        Key([mod], "minus", lazy.group['9'].dropdown_toggle('net'), desc='Wifi'),
        Key([mod], "comma", lazy.group['9'].dropdown_toggle('bluetooth'), desc='Bluetooth'),
        Key([mod], "s", lazy.group['9'].dropdown_toggle('music'), desc='Spotify'),
        Key([mod], "r", lazy.group['9'].dropdown_toggle('todo'), desc='Ticktick'), 
#- SCRATCHPAD_KEYS_END
    ])

### DRAG FLOATING LAYOUTS ###
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position() ),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

### CUSTOM WIDGETS ###
def seperator(custom_padding = seperator_padding):
    return Sep(
        linewidth    = seperator_line_width,
        foreground   = bar_background_color,
        padding      = custom_padding,
        size_percent = 0,
    )

def left_decor(color: str, padding_x=None, padding_y=9, round=False):
    radius = 4 if round else [4, 0, 0, 4]
    return [
        RectDecoration(
            colour=color,
            radius=radius,
            filled=True,
            padding_x=padding_x,
            padding_y=padding_y,
        )
    ]


def right_decor(round=False, padding_x=0, padding_y=9):
    radius = 4 if round else [0, 4, 4, 0]
    return [
        RectDecoration(
            colour=bar_border_color,
            radius=radius,
            filled=True,
            padding_y=padding_y,
            padding_x=padding_x,
        )
    ]

class WifiSsidWidget(widget.TextBox, base.InLoopPollText):
    def __init__(self):
        base.InLoopPollText.__init__(
            self, 
            update_interval = wifi_update_interval,
            font            = bold_font,
            padding         = widget_default_padding,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("alacritty -e nmtui")},
            decorations     = right_decor(True)
        )
        
    def poll(self):
        ssid = subprocess.check_output(['python3', '/home/jonalm/scripts/qtile/get_wifi_ssid.py'], text=True).strip()
        if ssid == "lo":
            return "Disconnected"
        else:
            return ssid
        
class NotificationWidget(widget.TextBox, base.InLoopPollText):
    def __init__(self):
        base.InLoopPollText.__init__(
            self, 
            update_interval = wifi_update_interval,
            font            = bold_font,
            padding         = widget_default_padding,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("/home/jonalm/scripts/other/get_notifications.py")},
            max_chars       = 6,
            decorations     = right_decor(True)
        )
        
    def poll(self):
        notification_message = subprocess.check_output(['/home/jonalm/scripts/other/get_recent_urgent_notification.py'], text=True).strip()
        if notification_message:
            return notification_message

### WIDGET SETTINGS ###
widget_defaults = dict(
    font        = bold_font,
    fontsize    = widget_default_font_size,
    padding     = widget_default_padding,
    foreground  = widget_default_foreground_color,
)

group_box_settings = {
        "margin"                      : groupbox_margin,
        "font"                        : icon_font,
        "highlight_method"            : "block",
        "borderwidth"                 : 6,
        "rounded"                     : True,
        "disable_drag"                : True,
        "active"                      : bar_border_color,
        "inactive"                    : bar_background_color,
        "block_highlight_text_color"  : "#000000",
        "highlight_color"             : "#000000",
        "this_current_screen_border"  : "#81A1C1",
        "hide_unused"                 : True,
        "other_current_screen_border" : group_box_other_border_color,
        "this_screen_border"          : group_box_this_border_color,
        "other_screen_border"         : group_box_other_border_color,
        "foreground"                  : group_box_foreground_color,
        # "background"                  : group_box_background_color,
        "urgent_border"               : group_box_urgentborder_color,
}

### BAR ###
top_bar_1 = Bar([
    seperator(icon_seperator_padding - 1),
    widget.TextBox(        
        text        = "<span font='Font Awesome 6 free solid 14' foreground='#000000' size='medium'></span>",
        padding     = widget_default_font_size - 12,
        mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/main_menu.py")},
        decorations = left_decor(round = True, color = battery_icon_color),
    ),

    seperator(icon_seperator_padding),
    widget.CurrentLayoutIcon(
        custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
        scale             = layouticon_scale,
        decorations       = left_decor(round = True, color = cpu_icon_color),
    ),

    # GROUPBOX #
    seperator(icon_seperator_padding),
    widget.GroupBox(
        **group_box_settings,
        decorations = left_decor(round = True, color = wifi_icon_color),
    ),

    seperator(icon_seperator_padding - 10),
    widget.TaskList(
        font                = "FiraCode Nerd Font Bold",
        fontsize            = widget_default_font_size + 1,
        padding_y           = widget_default_padding - 2,
        margin              = 6,
        borderwidth         = 6,
        spacing             = 2,
        txt_floating        = ' 缾 ',
        txt_maximized       = ' 类 ',
        txt_minimized       = ' 絛 ',
        title_width_method  = "uniform",
        urgent_alert_method = "border",
        highlight_method    = 'block',
        border              = bar_border_color,
        unfocused_border    = "#3c4455",
    ),
    seperator(icon_seperator_padding - 10),

    #  WIFI #
    widget.TextBox(        
        text            = "<span font='Font Awesome 6 free solid 14' foreground='#000000' size='medium'></span>",
        padding         = widget_default_font_size - 12,
        foreground      = notification_history_icon_color,
        decorations     = left_decor(wifi_icon_color, round = True),
    ),
    WifiSsidWidget(),

    # CPU #
    seperator(icon_seperator_padding),
    widget.TextBox(        
        text        = "<span font='Font Awesome 6 free solid 15' foreground='#000000'size='medium'></span>",
        padding     = widget_default_font_size - 12,
        decorations = left_decor(cpu_icon_color, round = True),
    ),
    widget.CPU(
        format          = "{load_percent}%",
        markup          = True,
        update_interval = cpu_update_interval,
        mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("alacritty -e sudo auto-cpufreq --stats")},
        decorations     = right_decor(True),
    ),    
    
    # BATTERY #
    seperator(icon_seperator_padding),
    widget.TextBox(        
        text        = "<span font='Font Awesome 6 free solid 14' foreground='#000000'size='medium'></span>",
        padding     = widget_default_font_size - 12,
        mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/power_management.py")},
        decorations = left_decor(battery_icon_color, round = True),
    ),
    widget.Battery(
        format          = "{percent:2.0%}", 
        markup          = True,
        update_interval = battery_update_interval, 
        mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("alacritty -e sudo powertop")},
        decorations     = right_decor(True),
    ),
    
    # URGENT NOTIFICATION #
    seperator(icon_seperator_padding),
    widget.TextBox(        
        text        = "<span font='Font Awesome 6 free solid 14' foreground='#000000' size='medium'></span>",
        padding     = widget_default_font_size - 12,
        decorations = left_decor(notification_icon_color, round = True),
    ),
    NotificationWidget(),
    
    # BACKLIGHT #
    seperator(icon_seperator_padding),
    widget.TextBox(        
        text        = "<span font='Font Awesome 6 free solid 14' foreground='#000000'size='medium'></span>",
        padding     = widget_default_font_size - 12,
        decorations = left_decor(backlight_icon_color, round = True),
    ),
    widget.Backlight(
        format          = "{percent:2.0%}",
        markup          = True,
        backlight_name  = "amdgpu_bl0",
        brightness_file = "/sys/class/backlight/amdgpu_bl0/actual_brightness",
        update_interval = backlight_update_interval, 
        decorations     = right_decor(True),
    ),
    
    # DATE #
    seperator(icon_seperator_padding),
    widget.TextBox(        
        text        = "<span font='Font Awesome 6 free solid 14' foreground='#000000'size='medium'></span>",
        padding     = widget_default_font_size - 12,
        decorations = left_decor(date_icon_color, round = True),
    ),
    widget.Clock(
        format      = "%a %b %d",
        markup      = True,
        decorations = right_decor(True),
    ),

    # TIME #
    seperator(icon_seperator_padding),
    widget.Clock(
        format      = "%R",
        fontsize    = widget_default_font_size + 1,
        decorations = right_decor(True),
    ),
    seperator(icon_seperator_padding - 4),
], bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

top_bar_2 = Bar([
    # GROUPBOX #
    widget.GroupBox(
        **group_box_settings,
    ),

    # TIME #
    widget.Spacer(
        bar.STRETCH,
    ),
    widget.Clock(
        format   = "%R",
        fontsize = widget_default_font_size + 2,
    ),
    widget.Spacer(
        bar.STRETCH,
    ),

    # WIFI #
    WifiSsidWidget(),

    # VOLUME #
    seperator(1),
    widget.Volume(
        format           = "<span font='Font Awesome 6 free solid 14' foreground='#88c0d0'size='medium'>  </span>{percent:2.0%}",
        markup           = True,
        limit_max_volume = "True",
        decorations      = [
            BorderDecoration(
                colour       = volume_icon_color,
                border_width = decorator_border_width,
                padding      = decorator_padding,
            )
        ],
    ),

    # CPU #
    seperator(1),
    widget.CPU(
        format          = "<span font='Font Awesome Bold 13' foreground='#8fbcbb'size='medium'>  </span>{load_percent}%",
        markup          = True,
        update_interval = cpu_update_interval,
        mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("alacritty -e sudo auto-cpufreq --stats")},
        decorations     = [
            BorderDecoration(
                colour       = cpu_icon_color,
                border_width = decorator_border_width,
                padding      = decorator_padding,
            )
        ],
    ),    
    
    # BATTERY #
    seperator(1),
    widget.Battery(
        format          = "<span font='Font Awesome 6 free solid 14' foreground='#a3be8c'size='medium'>  </span>{percent:2.0%}", 
        markup          = True,
        update_interval = battery_update_interval, 
        mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("alacritty -e sudo powertop")},
        decorations     = [
            BorderDecoration(
                colour       = battery_icon_color,
                border_width = decorator_border_width,
                padding      = decorator_padding,
            )
        ],
    ),
    
    # BACKLIGHT #
    seperator(1),
    widget.Backlight(
        format          ="<span font='Font Awesome 6 free solid 14' foreground='#d08770'size='medium'>  </span>{percent:2.0%}",
        markup          =True,
        backlight_name  = "amdgpu_bl0",
        brightness_file = "/sys/class/backlight/amdgpu_bl0/actual_brightness",
        update_interval = backlight_update_interval, 
        decorations     = [
            BorderDecoration(
                colour       = backlight_icon_color,
                border_width = decorator_border_width,
                padding      = decorator_padding,
            )
        ],
    ),

    # TIME #
    seperator(1),
    widget.Clock(
        format      = "<span font='Font Awesome 6 free solid 14' foreground='#bf616a'size='medium'>   </span>%a %b %d",
        markup      = True,
        decorations = [
            BorderDecoration(
                colour       = date_icon_color,
                border_width = decorator_border_width,
                padding      = decorator_padding,
            )
        ],
    ),

    # NOTIFICATION HISTORY #
    seperator(-1),
    widget.TextBox(
        text            = "",
        font            = icon_font,
        fontsize        = widget_default_font_size + 8,
        padding         = widget_default_font_size - 12,
        foreground      = notification_history_icon_color,
        mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/other/get_notifications.py")},
    ),
    seperator(-1),
], bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

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
        border_normal       = layout_normal_color_monadtall,
        border_focus        = layout_focus_color_monadtall,
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
        Match(wm_class = "yad"),
        Match(wm_class = "TSP"),
        Match(wm_class = "blueman-applet"),
        Match(wm_class = "blueman-manager"),
        Match(wm_class = "nitrogen"),
        Match(wm_class = "pavucontrol"),
        Match(wm_class = "pavucontrol"),
        Match(wm_class = "brave"),
        Match(wm_class = "se-liu-jonal155-tetris-Tester"),
        Match(wm_class = "ticktick"),
        Match(wm_class = "se-liu-davhe786_jonal155-pong-Main"),
        Match(wm_class = "qalculate-gtk"),
        ])

### DECLARING WIDGET SETTINGS ###
extension_defaults = widget_defaults.copy()

screen_output = subprocess.check_output(["xrandr", "-q"]).decode().strip()
screen_data = subprocess.check_output(['awk', '/HDMI-A-0/ {print $1}'], input=screen_output.encode()).decode().strip()
if "HDMI-A-0: connected" in screen_data:
    single_monitor   = False
    top_bar_1_var    = top_bar_1
    top_bar_2_var    = top_bar_2
else:
    top_bar_1_var    = top_bar_1
    top_bar_2_var    = None

### DECLARING PANEL ###
screens = [
    Screen(top=top_bar_1_var, bottom=bar.Gap(bar_gap_size), left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size)),
    Screen(top=top_bar_2_var, bottom=bar.Gap(bar_gap_size), left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size)) 

    ]
        
### HOOKS ###
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

wmname = "LG3D"
