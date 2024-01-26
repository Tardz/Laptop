from functions import (
    move_focus_and_mouse, spawn_alttab_once, check, notify,
    close_all_windows, mute_or_unmute, show_or_hide_tabs, 
    hide_bottom_bar, minimize_windows, swap_screens
)
from libqtile.config import Key, KeyChord, Click, Drag
from libqtile.lazy import lazy
from groups import groups
from settings import *

#- KEYS_START
keys = [
        #--[ESSENTIALS]--#
        Key([mod], "Tab", lazy.next_layout(), desc='Toggle through layouts'),
        Key([mod], "q", lazy.window.kill(), desc='Kill active window'),
        Key([mod, "shift"], "r", lazy.restart(), lazy.spawn("/home/jonalm/scripts/term/reset_screens.sh"), desc='Restart Qtile'),
        Key([mod, "shift"], "q", lazy.shutdown(), desc='Shutdown Qtile'),
        Key([mod, "control"], "q", close_all_windows, desc='close all windows'),
        Key([mod], "x", lazy.spawn("python3 /home/jonalm/scripts/qtile/bar_menus/system/system_menu.py"), desc='System menu'),

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
        Key([mod], "Up", lazy.screen.next_group(), desc='Next group right'),
        Key([mod], "Down", lazy.screen.prev_group(), desc='Next group left'),

        #--[WINDWOW CONTROLS]--#
        # Key(["mod1", "shift"], "d", hide_bottom_bar(), desc='Hide bottom bar'),
        Key([mod, "shift"], "h", minimize_windows(), desc="minimize/unminimize windows"),
        Key([mod], "Left", lazy.layout.down(), desc='Move focus down in current stack pane'),
        Key([mod], "Right", lazy.layout.up(), desc='Move focus up in current stack pane'),
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
        Key([mod, "shift"], "s", lazy.spawn("flameshot screen"), desc="screenshot screen"),

        #--[MENUS]--#
        Key([mod], "comma", lazy.spawn("python3 /home/jonalm/scripts/qtile/bar_menus/volume/volume_menu.py"), desc='Volume'),
        Key([mod], "period", lazy.spawn("python3 /home/jonalm/scripts/qtile/bar_menus/bluetooth/bluetooth_menu.py"), desc='bluetooth'),
        Key([mod], "minus", lazy.spawn("python3 /home/jonalm/scripts/qtile/bar_menus/wifi/wifi_menu.py"), desc='wifi'),

        #--[URLS]--#
        Key([mod], "y", move_focus_and_mouse("c"), lazy.group["c"].toscreen(), lazy.spawn("firefox youtube.com"), desc='Youtube'),

        #--[TERM]--#
        Key([mod], "h", move_focus_and_mouse("n"), lazy.group["n"].toscreen(), check(from_key_press=["htop", "3", "alacritty --title Htop -e"]), desc='Htop'),
        Key([mod], "plus", lazy.spawn("/home/jonalm/scripts/term/show_keys.sh"), desc='Keybindings'),

        #--[ROFI]--#
        Key([mod], "space", lazy.spawn("/home/jonalm/.config/rofi/files/launchers/apps/launcher.sh"), desc='Rofi drun'),
        Key([mod], "w", lazy.spawn("/home/jonalm/scripts/rofi/config/config_files.sh"), desc='Rofi config files'),
        Key([mod], "l", lazy.spawn("/home/jonalm/scripts/rofi/search/search_web.sh"), desc='Rofi web search'),
        Key([mod], "k", lazy.spawn(home + "/scripts/rofi/automation/laptop_version/main/automation.sh") if laptop else lazy.spawn(home + "/scripts/rofi/automation/desktop_version/main/automation.sh"), desc='Rofi automation scripts'),
#- KEYS_END
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button1", lazy.window.bring_to_front())
]

### MOVE WINDOW TO WORKSPACE AND DROPDOWNS ###
for i in groups:
    keys.extend([
#- SCRATCHPAD_KEYS_START

        #--[WINDOWS]--#
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name), lazy.group[i.name].toscreen(), notify(i.name), desc="move focused window to group {}".format(i.name)),
        Key([mod], i.name, move_focus_and_mouse(i.name), lazy.group[i.name].toscreen(), check(i.name), desc="Switch to group {}".format(i.name)),
        #--[SCRATCHPAD]--#
        Key([mod], "Return", lazy.group['9'].dropdown_toggle('terminal'), desc='Terminal'),
        Key([mod], "s", lazy.group['9'].dropdown_toggle('music'), desc='Spotify'),
        Key([mod], "r", lazy.group['9'].dropdown_toggle('todo'), desc='Ticktick'),
#- SCRATCHPAD_KEYS_END
    ])