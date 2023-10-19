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
def spawn_browser(qtile):
    if qtile.current_group.name == "2":
        qtile.cmd_spawn(myBrowser)

@lazy.function
def spawn_code(qtile):
    if qtile.current_group.name == "3":
        qtile.cmd_spawn("code")

@lazy.function
def spawn_filemanager(qtile):
    if qtile.current_group.name == "4":
        qtile.cmd_spawn("alacritty -e ranger")

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
    qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/check_and_launch_app.py " + "null")

@lazy.function
def check_youtube(qtile):
    qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/check_and_launch_app.py " + "youtube")

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
            Key([], "r", lazy.spawn("sudo systemctl reboot"))
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
        Key([mod], "c", spawn_browser, lazy.group["2"].toscreen(), check, desc='Browser'),
        Key([mod], "n", spawn_filemanager, lazy.group["4"].toscreen(), check,desc='Filemanager'),
        Key([mod], "d", spawn_discord, lazy.group["7"].toscreen(), check, desc='Discord'),
        Key([mod], "v", spawn_code, lazy.group["3"].toscreen(), check, desc='VScode'),
        Key([mod], "m", spawn_thunderbird, lazy.group["5"].toscreen(), check, desc='Mail'),

        #--[URLS]--#
        Key([mod], "y", spawn_youtube, lazy.group["2"].toscreen(), check_youtube, desc='Youtube'),

        #--[TERM]--#
        Key([mod], "h", spawn_htop, lazy.group["8"].toscreen(), desc='Htop'),
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
        Group('1', label = "", matches=[ #Other
            ]), 
        Group('2', label = "", matches=[ #Browser
            Match(wm_class = ["chromium"]),
            Match(wm_class = ["brave-browser"]),
                ]), 
        Group('3', label = "", matches=[ #Code
            Match(wm_class = ["code"]),
            Match(wm_class = ["jetbrains-clion"]),
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

### SCRATCHPAD ###
groups.append(ScratchPad('9', [
    DropDown('terminal', 'alacritty', warp_pointer=True, width=0.35, height=0.55, x=0.33, y=0.18, opacity=1, on_focus_lost_hide = scratchpad_focus_value),
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
        foreground   = widget_default_background_color,
        background   = bar_background_color,
        padding      = custom_padding,
        size_percent = seperator_size,
    )

class WifiSsidWidget(widget.TextBox, base.InLoopPollText):
    def __init__(self):
        base.InLoopPollText.__init__(
            self, 
            update_interval = wifi_update_interval,
            font            = bold_font,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("alacritty -e nmtui")},
            decorations = [
                BorderDecoration(
                    colour       = wifi_icon_color,
                    border_width = decorator_border_width,
                    padding      = decorator_padding,
                )
            ],
        )
        
    def poll(self):
        ssid = subprocess.check_output(['python3', '/home/jonalm/scripts/qtile/get_wifi_ssid.py'], text=True).strip()
        if ssid == "lo":
            return "<span font='Font Awesome 6 free solid 15' foreground='#b48ead' size='medium'>  </span>Disconnected"
        else:
            return "<span font='Font Awesome 6 free solid 15' foreground='#b48ead' size='medium'>  </span>" + ssid
        
### WIDGET SETTINGS ###
widget_defaults = dict(
    font        = bold_font,
    fontsize    = widget_default_font_size,
    padding     = widget_default_padding,
    background  = widget_default_background_color,
    foreground  = widget_default_foreground_color,
    decorations = [
        BorderDecoration(
            colour       = bar_background_color,
            border_width = decorator_border_width,
            padding      = decorator_padding,
        )
    ],
)

### BAR ###
top_bar = Bar([
    # GROUPBOX #
    widget.GroupBox(
        margin                      = groupbox_margin,
        font                        = icon_font,
        borderwidth                 = 6,
        active                      = group_box_active_color,
        inactive                    = group_box_inactive_color,
        block_highlight_text_color  = group_box_highlight_color,
        highlight_color             = group_box_highlight_color,
        highlight_method            = "block",
        disable_drag                = True,
        rounded                     = True,
        this_current_screen_border  = widget_default_background_color,
        other_current_screen_border = group_box_other_border_color,
        this_screen_border          = group_box_this_border_color,
        other_screen_border         = group_box_other_border_color,
        foreground                  = group_box_foreground_color,
        background                  = group_box_background_color,
        urgent_border               = group_box_urgentborder_color,
    ),

    # TIME #
    widget.Spacer(
        bar.STRETCH,
    ),
    widget.Clock(
        format   = "%R:%S",
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
        format           = "<span font='Font Awesome 6 free solid 15' foreground='#88c0d0'size='medium'>  </span>{percent:2.0%}",
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
        format          = "<span font='Font Awesome 6 free solid 15' foreground='#a3be8c'size='medium'>  </span>{percent:2.0%}", 
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
        format          ="<span font='Font Awesome 6 free solid 15' foreground='#d08770'size='medium'>  </span>{percent:2.0%}",
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
        format      = "<span font='Font Awesome 6 free solid 15' foreground='#bf616a'size='medium'>   </span>%a %b %d",
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
], bar_size, margin = bar_margin_top, border_width = bar_width_top, border_color = bar_border_color)

bottom_bar = Bar([
    # ROFI APP LAUNCHER #
    widget.TextBox(
        text            = "",
        font            = icon_font,
        fontsize        = widget_default_font_size + bottom_icons_font_size_plus,
        padding         = widget_default_padding + bottom_icons_padding_plus,
        foreground      = wifi_icon_color,
        mouse_callbacks = {
            'Button1': lambda: Qtile.cmd_spawn("/home/jonalm/.config/rofi/files/launchers/type-1/launcher.sh"),
        }
    ),
    # ROFI SEARCH #
    widget.TextBox(
        text            = "",
        font            = icon_font,
        fontsize        = widget_default_font_size + bottom_icons_font_size_plus,
        padding         = widget_default_padding + bottom_icons_padding_plus,
        foreground      = volume_icon_color,
        mouse_callbacks = {
            'Button1': lambda: Qtile.cmd_spawn("/home/jonalm/scripts/rofi/search/search_web.sh"),
        }
    ),

    # ROFI CONFIG #
    widget.TextBox(
        text            = "",
        font            = icon_font,
        fontsize        = widget_default_font_size + bottom_icons_font_size_plus,
        padding         = widget_default_padding + bottom_icons_padding_plus,
        foreground      = cpu_icon_color,
        mouse_callbacks = {
            'Button1': lambda: Qtile.cmd_spawn("/home/jonalm/scripts/rofi/config/config_files.sh"),
        }
    ),

    # CURRENT OPENED APPS #
    widget.Sep(
        linewidth    = bottom_seperator_line_width,
        foreground   = bar_border_color,
        size_percent = bottom_seperator_size_percent,
        padding      = bottom_seperator_padding
    ),
    widget.TaskList(
        font                = "FiraCode Nerd Font Bold",
        fontsize            = widget_default_font_size + 1,
        padding             = widget_default_padding - 2,
        margin              = 5,
        borderwidth         = 6,
        txt_floating        = ' 缾 ',
        txt_maximized       = ' 类 ',
        txt_minimized       = ' 絛 ',
        title_width_method  = "uniform",
        urgent_alert_method = "border",
        highlight_method    = 'block',
        border              = bar_border_color,
        unfocused_border    = colors[61],
    ),
    widget.Sep(
        linewidth    = bottom_seperator_line_width,
        foreground   = bar_border_color,
        size_percent = bottom_seperator_size_percent,
        padding      = bottom_seperator_padding
    ),

    # ROFI AUTOMATION #
    widget.TextBox(
        text            = "",
        font            = icon_font,
        fontsize        = widget_default_font_size + bottom_icons_font_size_plus,
        padding         = widget_default_padding + bottom_icons_padding_plus,
        foreground      = battery_icon_color,
        mouse_callbacks = {
            'Button1': lambda: Qtile.cmd_spawn("/home/jonalm/scripts/rofi/automation/automation.sh"),
        }
    ),

    # KEYBOARD SHORTCUTS #
    widget.TextBox(
        text            = "",
        font            = icon_font,
        fontsize        = widget_default_font_size + bottom_icons_font_size_plus,
        padding         = widget_default_padding + bottom_icons_padding_plus,
        foreground      = backlight_icon_color,
        mouse_callbacks = {
            'Button1': lambda: Qtile.cmd_spawn("/home/jonalm/scripts/term/show_keys.sh"),
        }
    ),

    # ROFI POWER MENU #
    widget.TextBox(
        text            = "",
        font            = icon_font,
        fontsize        = widget_default_font_size + bottom_icons_font_size_plus,
        padding         = widget_default_padding + bottom_icons_padding_plus,
        foreground      = date_icon_color,
        mouse_callbacks = {
            'Button1': lambda: Qtile.cmd_spawn("/home/jonalm/.config/rofi/files/powermenu/type-2/powermenu.sh"),
        }
    ),
], bar_size + 3, margin = bar_margin_bottom, border_width = bar_width_bottom, border_color = bar_border_color)

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

### DECLARING PANEL ###
screens = [Screen(top=top_bar, bottom=bottom_bar, left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))]
        
### HOOKS ###
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

wmname = "LG3D"
