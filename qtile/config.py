### CONF IMPORTS ###
from libqtile.config import Screen
from libqtile import hook, bar
from libqtile.lazy import lazy
import subprocess
import os
import re

### KEYBINDING AND GROUPS IMPORTS ###
from libqtile.config import Match, Key, KeyChord, Click, Drag, ScratchPad, Group, DropDown
from libqtile import qtile as Qtile

### BAR IMPORTS ###
from qtile_extras.widget.decorations import BorderDecoration, RectDecoration
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

### LOGGING ###
import logging
log = logging.getLogger("qtile")

clear_handler = logging.FileHandler("/home/jonalm/.config/qtile/logfile.log", mode="w")
log.addHandler(clear_handler)

handler = logging.FileHandler("/home/jonalm/.config/qtile/logfile.log")
handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
log.addHandler(handler)
log.setLevel(logging.DEBUG)

### LAZY FUNCTIONS FOR SHORTCUTS ###
@lazy.function
def move_focus_and_mouse(qtile, group):
    global amt_screens
    if amt_screens == 2:
        monitor = check_dict[group][2]
        qtile.cmd_to_screen(monitor)
        if laptop: #Quick fix
            if monitor == 0:
                qtile.cmd_spawn("xdotool mousemove 4300 900")
            elif monitor == 1:
                qtile.cmd_spawn("xdotool mousemove 1500 800")
        else:
            if monitor == 0:
                qtile.cmd_spawn("xdotool mousemove 1000 500")
            elif monitor == 1:
                qtile.cmd_spawn("xdotool mousemove 2900 500")

@lazy.function
def spawn_alttab_once(qtile):
    if not alttab_spawned:
        qtile.cmd_spawn('alttab -bg "#2e3440" -fg "#d8dee9" -bc "#2e3440" -bw 18 -inact "#3b4252" -frame "#81a1c1"')

@lazy.function
def check(qtile, group_name=None, from_key_press=None):
    if from_key_press:
        qtile.cmd_spawn(["/home/jonalm/scripts/qtile/check_and_launch_app.py", from_key_press[0], from_key_press[1], from_key_press[2]])
    elif group_name and check_dict[group_name][0]:
        info = check_dict[group_name]
        if info != []:
            try:
                command = ""
                if info[1]:
                    command = info[1]

                qtile.cmd_spawn(["/home/jonalm/scripts/qtile/check_and_launch_app.py", info[0], group_name, command])
            except Exception as e:
                log.exception(f"Error in check function: {e}")
                log.debug("END OF ERROR\n")

@lazy.function
def notify(qtile, group_name):
    try:
        group_name_upper = group_name.upper()

        qtile.cmd_spawn(f'notify-send -u low -t 1000 \'-h\' \'int:transient:1\' "Sent to ""{group_name_upper} "')
    except Exception as e:
        log.exception(f"Error in check function: {e}")
        log.debug("END OF ERROR\n")

@lazy.function
def close_all_windows(qtile):
    for group in qtile.groups:
        for window in group.windows:
            window.kill()

@lazy.function
def get_next_screen_group(qtile):
    ## NOT WORKING
    qtile.cmd_spawn(["qtile", "cmd-obj", "-o", "cmd", "-f", "next_screen"])
    data = subprocess.check_output(["qtile", "cmd-obj", "-o", "group", "-f", "info"]).decode().strip()

    matches = re.findall(r"'name': '([^']+)'", data)

    if len(matches) >= 2:
        group_name = matches[1]
        return group_name
    else:
        log.error("Group not found.")

@lazy.function
def mute_or_unmute(qtile):
    qtile.cmd_spawn("/home/jonalm/scripts/qtile/mute_or_unmute.sh")

@lazy.function
def show_or_hide_tabs(screen=None, offset=0):
    if screen is None:
        screen = Qtile.current_screen   

    bar = screen.bottom
    if not bar:
        return

    nwindows = len(screen.group.windows) + offset
    if nwindows > 1:
        bar.show()
    else:
        if bar.window:
            bar.show(False)

@lazy.function
def hide_bottom_bar(screen=None, offset=0):
    if screen is None:
        screen = Qtile.current_screen

    bar = screen.bottom

    if bar.window:
        bar.show(False)
    else:
        bar.show()

@lazy.function
def minimize_windows(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()

@lazy.function
def swap_screens(qtile):
    qtile.cmd_spawn("/home/jonalm/scripts/qtile/get_next_screen_group.py")
    screen = Qtile.current_screen
    qtile.current_group.toscreen()
    
### KEYBINDINGS ###
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
        Key([mod], "space", lazy.spawn("/home/jonalm/.config/rofi/files/launchers/type-1/launcher.sh"), desc='Rofi drun'),
        Key([mod], "Escape", lazy.spawn("/home/jonalm/.config/rofi/files/powermenu/type-2/powermenu.sh"), desc='Rofi powermenu'),
        Key([mod], "w", lazy.spawn("/home/jonalm/scripts/rofi/config/config_files.sh"), desc='Rofi config files'),
        Key([mod], "l", lazy.spawn("/home/jonalm/scripts/rofi/search/search_web.sh"), desc='Rofi web search'),
        Key([mod], "k", lazy.spawn(home + "/scripts/rofi/automation/laptop/automation.sh") if laptop else lazy.spawn(home + "/scripts/rofi/automation/desktop/automation.sh"), desc='Rofi automation scripts'),
#- KEYS_END
]

### GROUP SETTINGS ###
groups = [
        Group('c', label = "", matches=[ #Browser
            Match(wm_class = ["Navigator"]),
            Match(wm_class = ["chromium"]),
            Match(wm_class = ["brave-browser"]),
                ]),
        Group('v', label = "", matches=[ #Code
            Match(wm_class = ["code"]),
            Match(wm_class = ["jetbrains-clion"]),
            Match(wm_class = ["jetbrains-studio"]),
            Match(wm_class = ["jetbrains-idea"]),
            ]),
        Group('n', label = "", matches=[ #Files
            Match(wm_class = ["pcmanfm"]),
            Match(wm_class = ["thunderbird"]),
            Match(wm_class = ["lxappearance"]),
            Match(wm_class = ["tlpui"]),
            ]),
        Group('d', label = "", matches=[ #Social
            Match(wm_class = ["discord"]),
            ]),
        Group('9', label = ""), #Scratchpad
]

### SCRATCHPAD ###
groups.append(ScratchPad('9', [
    DropDown('terminal', 'alacritty --title alacritty', warp_pointer=True, width=0.45, height=0.55, x=0.28, y=0.18, opacity=1, on_focus_lost_hide = scratchpad_focus_value),
    DropDown('filemanager', 'pcmanfm', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = scratchpad_focus_value),
    DropDown('music', 'spotify', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=1, on_focus_lost_hide = scratchpad_focus_value),
    DropDown('todo', 'ticktick', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = scratchpad_focus_value),
]))

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

### DRAG FLOATING LAYOUTS ###
mouse = [
    Drag([mod], "Button1", lazy.window.set_position(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button1", lazy.window.bring_to_front())
]

### CUSTOM WIDGETS ###
def seperator(custom_padding=seperator_padding, background=None):
    return Sep(
        background = background,
        linewidth = seperator_line_width,
        foreground = bar_background_color,
        padding = custom_padding,
        size_percent = 0,
    )

# Default padding_y = 9, Default padding_x = None
def left_decor(color, round=True, padding_x=None, padding_y=left_decor_padding):
    radius = 6 if round else [4, 0, 0, 4]
    if not laptop:
        radius = 5
    return [
        RectDecoration(
            colour = color,
            radius = radius,
            filled = True,
            padding_x = padding_x,
            padding_y = padding_y,
        )
    ]

def right_decor(color=right_decor_background, round=True, padding_x=0, padding_y=left_decor_padding):
    radius = 6 if round else [0, 4, 4, 0]
    if not laptop:
        radius = 5
    return [
        RectDecoration(
            colour = color,
            radius = radius,
            filled = True,
            padding_x = padding_x,
            padding_y = padding_y,
        )
    ]

def task_list_decor(color=bar_background_color, radius=8 if laptop else 5, padding_x=0, padding_y=0):
    return RectDecoration(
        line_width = bottom_widget_width,
        line_colour = bar_border_color,
        colour = color,
        radius = radius,
        filled = True,
        padding_y = padding_y,
        padding_x = padding_x,
    )

def icon_decor(color=bar_background_color, border_width=[3, 0, 3, 0]):
    return BorderDecoration(
        border_width = border_width,
        colour = color,
    )

def modify_window_name(text):
    parts = text.split('-')

    cleaned_parts = [part.strip() for part in parts]

    if len(cleaned_parts) >= 2:
        if cleaned_parts[-1] == "Visual Studio Code":
            return f"Code - {cleaned_parts[0]}"
        return f"{cleaned_parts[-1]} - {cleaned_parts[0]}"
    elif len(cleaned_parts) == 1:
        return cleaned_parts[0]
    else:
        return ''

class PowerButton(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text = f"<span font='Font Awesome 6 free solid {icon_size}' foreground='{icon_foreground_12}' size='medium'></span>",
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/system/system_menu.py")},
            decorations = left_decor(icon_background_12),
        )

class LayoutIcon(widget.CurrentLayoutIcon):
    def __init__(self):
        widget.CurrentLayoutIcon.__init__(
            self,
            custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
            scale             = layouticon_scale,
            decorations       = left_decor(icon_background_11),
        )

class TickTickMenu(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text        = f"<span font='Font Awesome 6 free solid {icon_size}' foreground='{icon_foreground_10}' size='medium'></span>",
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/ticktick/launch.py")},
            decorations = left_decor(icon_background_10),
        )

class BluetoothIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text            = f"<span font='Font Awesome 6 free solid {icon_size + 1}' foreground='{icon_foreground_1}' size='medium'></span>",
            foreground      = text_color,
            padding         = widget_default_padding + 2, 
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/bluetooth/bluetooth_menu.py")},
            decorations     = left_decor(icon_background_1),
        )

class BluetoothWidget(widget.TextBox, base.InLoopPollText):
    def __init__(self):
        base.InLoopPollText.__init__(
            self,
            update_interval = wifi_update_interval,
            font            = bold_font,
            padding         = widget_default_padding,
            decorations     = right_decor()
        )
        
    def poll(self):
        try:
            bluetooth_state = subprocess.check_output("systemctl status bluetooth | grep Running", shell=True, stderr=subprocess.PIPE, text=True).strip()
            if "Running" in bluetooth_state:
                connected_devices_output = subprocess.check_output("bluetoothctl devices Connected", shell=True).decode("utf-8")
                lines = connected_devices_output.splitlines()

                if connected_devices_output:
                    lines = connected_devices_output.splitlines()

                    parts = lines[0].split(" ", 2)

                    device_name = parts[2]
                    headphone_icon = "<span font='Font Awesome 6 free solid {icon_size}' foreground='white' size='medium'> </span>"
                    airpods_icon = "<span font='Font Awesome 6 fvree solid 12' foreground='white' size='medium'> </span>"

                    if device_name == "N/A":
                        return
                    elif "Jonathans Bose QC35 II" in device_name:
                        return "Bose"
                    elif device_name == "Jonathans Pods - Find My":
                        return "AirPods"
                    elif device_name == "controller available":
                        return "Error"
                    else:
                        return device_name

        except subprocess.CalledProcessError as e:
            return "Off"

class VolumeIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text            = f"<span font='Font Awesome 6 free solid {icon_size - 1}' foreground='{icon_foreground_2}' size='medium'></span>",
            foreground      = text_color,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/volume/volume_menu.py")},
            decorations     = left_decor(icon_background_2),
        )

class VolumeWidget(widget.PulseVolume):
    def __init__(self):
        widget.PulseVolume.__init__(
            self,
            decorations     = right_decor(),
        )

class WifiIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text            = f"<span font='Font Awesome 6 free solid {icon_size - 1}' foreground='{icon_foreground_3}' size='medium'></span>",
            foreground      = text_color,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/wifi/wifi_menu.py")},
            decorations     = left_decor(icon_background_3),
        )

class WifiWidget(widget.TextBox, base.InLoopPollText):
    def __init__(self):
        base.InLoopPollText.__init__(
            self,
            update_interval = wifi_update_interval,
            font            = bold_font,
            padding         = widget_default_padding,
            decorations     = right_decor()
        )

    def poll(self):
        wifi_state = subprocess.check_output(["nmcli",  "radio", "wifi"]).strip().decode("utf-8")
        if wifi_state == "disabled":
            return "Off"

        connection_output = subprocess.check_output(['nmcli', '-t', '-f', 'NAME', 'connection', 'show', '--active'], text=True)
        connection_names = connection_output.strip().split('\n')

        if connection_names:
            ssid = connection_names[0]
            if ssid == "lo":
                return "Disconnected"
            elif ssid == "Wired connection 1":
                return "Ethernet"
            else:
                return ssid
        else:
            return "Error"
        
class CpuTempIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            padding = widget_default_padding + 2,
            text = f"<span font='Font Awesome 6 free solid {icon_size + 1}' foreground='{icon_foreground_4}'size='medium'></span>",
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/cpu/cpu_stats_menu.py")},
            decorations = left_decor(icon_background_4),
        )

class CpuTempWidget(widget.ThermalSensor):
    def __init__(self):
        widget.ThermalSensor.__init__(
            self,
            format = "{temp:.0f}{unit}",
            threshold = 80.0,
            foreground_alert = "#bf616a",
            markup = True,
            update_interval = cpu_update_interval,
            decorations = right_decor(),
        )

class CpuLoadIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text = f"<span font='Font Awesome 6 free solid {icon_size}' foreground='{icon_foreground_5}'size='medium'></span>",
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/cpu/cpu_stats_menu.py")},
            decorations = left_decor(icon_background_5),
        )

class CpuLoadWidget(widget.CPU):
    def __init__(self):
        widget.CPU.__init__(
            self,
            format = "{load_percent}%",
            markup = True,
            update_interval = cpu_update_interval,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("alacritty -e sudo auto-cpufreq --stats")},
            decorations = right_decor(),
        )

class BatteryIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text = f"<span font='Font Awesome 6 free solid {icon_size}' foreground='{icon_foreground_6}'size='medium'></span>",
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/power/power_management_menu.py")},
            decorations = left_decor(icon_background_6),
        )

class BatteryWidget(widget.Battery):
    def __init__(self):
        widget.Battery.__init__(
            self,
            format = "{percent:2.0%}",
            markup = True,
            update_interval = battery_update_interval,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("alacritty -e sudo powertop")},
            decorations = right_decor(),
        )

class WattageIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text = f"<span font='Font Awesome 6 free solid {icon_size}' foreground='{icon_foreground_7}'size='medium'></span>",
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/power/power_management_menu.py")},
            decorations=left_decor(icon_background_7),
        )

class WattageWidget(widget.Battery):
    def __init__(self):
        widget.Battery.__init__(
            self,
            format = "{watt:.2f}",
            markup = True,
            update_interval = battery_update_interval,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("alacritty -e sudo powertop")},
            decorations = right_decor(),
        )

notification_shown = False

class NotificationWidget(widget.TextBox, base.InLoopPollText):
    def __init__(self):
        base.InLoopPollText.__init__(
            self,
            update_interval = wifi_update_interval,
            max_chars = 6,
            decorations = right_decor()
        )

        self.shown = False
        self.notification_message = None
        self.seen_notification_message = None

    def poll(self):
        global notification_shown
        self.notification_message = subprocess.check_output(['/home/jonalm/scripts/other/get_recent_urgent_notification.py'], text=True).strip()
        if self.notification_message and self.notification_message != self.seen_notification_message:
            notification_shown = True
            return self.notification_message
        else:
            notification_shown = False
            return ""

    def mouse_enter(self, *args, **kwargs):
        Qtile.cmd_spawn("/home/jonalm/scripts/other/get_notifications.py")

    def mouse_leave(self, *args, **kwargs):
        self.seen_notification_message = self.notification_message
        if self.notification_message:
            self.notification_message = None
        
        Qtile.cmd_spawn("/home/jonalm/scripts/other/get_notifications.py")
        self.poll()

class NotificationIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text = f"<span font='Font Awesome 6 free solid {icon_size}' foreground='{icon_foreground_8}' size='medium'></span>",
            decorations = left_decor(icon_background_8),
        )

    def mouse_enter(self, *args, **kwargs):
        if not notification_shown:
            Qtile.cmd_spawn("/home/jonalm/scripts/other/get_notifications.py")

    def mouse_leave(self, *args, **kwargs):
        if not notification_shown:
            Qtile.cmd_spawn("/home/jonalm/scripts/other/get_notifications.py")

class BacklightIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text        = f"<span font='Font Awesome 6 free solid {icon_size}' foreground='{icon_foreground_9}'size='medium'></span>",
            decorations = left_decor(icon_background_9),
        )

class BacklightWidget(widget.Backlight):
    def __init__(self):
        widget.Backlight.__init__(
            self,
            format = "{percent:2.0%}",
            markup = True,
            backlight_name = "amdgpu_bl1",
            brightness_file = "/sys/class/backlight/amdgpu_bl1/actual_brightness",
            update_interval = backlight_update_interval,
            decorations = right_decor(),
        )

class MouseOverClock(widget.Clock):
    def __init__(self, **config):
        widget.Clock.__init__(
            self,
            long_format = "%A %d %B %Y %H:%M",
            decorations = right_decor(),
            **config
        )
        self.short_format = self.format

    def mouse_enter(self, *args, **kwargs):
        self.format = self.long_format
        self.bar.draw()

    def mouse_leave(self, *args, **kwargs):
        self.format = self.short_format
        self.bar.draw()

class NothingWidget(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            padding = 0,
            fontsize = 0,
        )

### WIDGET SETTINGS ###
widget_defaults = dict(
    font        = bold_font,
    fontsize    = widget_default_font_size,
    padding     = widget_default_padding,
    foreground  = widget_default_foreground_color,
)

task_list_settings = dict(
    font                = "FiraCode Nerd Font Bold",
    fontsize            = widget_default_font_size + 1,
    padding_y           = widget_default_padding - 2,
    margin              = task_list_margin,
    borderwidth         = task_list_border_width,
    spacing             = task_list_spacing,
    icon_size           = task_list_icon_size,
    markup_floating     = "<span font='Font Awesome 6 free solid {icon_size}' foreground='#A7BEAE' size='medium'> 缾 </span>{}",
    markup_minimized    = "<span font='Font Awesome 6 free solid {icon_size}' foreground='#b16286' size='medium'> 絛 </span>{}",
    markup_maximized    = "<span font='Font Awesome 6 free solid {icon_size}' foreground='#b16286' size='medium'> 类 </span>{}",
    title_width_method  = "uniform",
    urgent_alert_method = "border",
    highlight_method    = 'block',
    rounded             = True,
    parse_text          = modify_window_name,
    border              = bar_border_color,
    background          = transparent,
    foreground          = "#d8dee9",
    unfocused_border    = "#383b41",
    theme_mode          = "preferred",
    theme_path          = "/usr/share/icons/Adwaita",
    decorations         = [task_list_decor()],
)

group_box_settings = dict(
    # margin                      = groupbox_margin,
    padding_x                   = 15,
    margin_x                    = 10,
    borderwidth                 = 2,
    rounded                     = True,
    disable_drag                = True,
    hide_unused                 = True,
    font                        = icon_font,
    highlight_method            = "block",
    active                      = bar_border_color,
    inactive                    = bar_background_color,
    block_highlight_text_color  = "#000000",
    highlight_color             = "#000000",
    this_current_screen_border  = "#bf616a",
    this_screen_border          = bar_border_color,
    other_current_screen_border = group_box_other_border_color,
    other_screen_border         = group_box_other_border_color,
    foreground                  = group_box_foreground_color,
    urgent_border               = group_box_urgentborder_color,
)

class GroupBoxWidget(widget.GroupBox):
    def __init__(self):
        widget.GroupBox.__init__(
            self,
            **group_box_settings, 
            background = transparent, 
            decorations = [task_list_decor()]
        )

class WindowCountWidget(widget.WindowCount):
    def __init__(self):
        widget.WindowCount.__init__(
            self,
            padding = widget_default_padding + 8, 
            background = transparent, 
            show_zero = True, 
            decorations = [task_list_decor()]
        )

### BARS ###
single_top_bar = Bar([
    # POWERBUTTON # 
    seperator(-3),
    PowerButton(),

    # LAYOUTICON # 
    seperator(),
    LayoutIcon(),

    # TICKTICK MENU #
    seperator(),
    TickTickMenu(),

    widget.Spacer(bar.STRETCH),

    # BLUETOOTH #
    BluetoothIcon(),
    BluetoothWidget(),
    seperator(),

    # VOLUME #
    VolumeIcon(),
    VolumeWidget(),
    seperator(),

    #  WIFI #
    WifiIcon(),
    WifiWidget(),

    # CPU TEMP #
    seperator(),
    CpuTempIcon(),
    CpuTempWidget(),

    # CPU LOAD #
    seperator(),
    CpuLoadIcon(),
    CpuLoadWidget(),

    # BATTERY #
    seperator(),
    BatteryIcon(),
    BatteryWidget(),

    # WATTAGE #
    seperator(),
    WattageIcon(),
    WattageWidget(),

    # URGENT NOTIFICATION #
    seperator(),
    NotificationIcon(),
    NotificationWidget(),

    # BACKLIGHT #
    seperator(),
    BacklightIcon(),
    BacklightWidget(),

    # TIME #
    seperator(),
    MouseOverClock(),
    seperator(-5),

], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

single_bottom_bar = Bar([
    # GROUPBOX #
    GroupBoxWidget(),
    
    # TASKLIST #
    seperator(background=transparent),
    widget.TaskList(**task_list_settings),

    # WINDOWCOUNT #
    seperator(background=transparent),
    WindowCountWidget(),

], bottom_bar_size, margin = bar_margin_bottom, background = bar_background_color, border_width = bar_width_bottom, border_color = bar_border_color, opacity=1)

top_bar_1 = Bar([
    widget.Spacer(bar.STRETCH),
    
    # BLUETOOTH #
    BluetoothIcon(),
    BluetoothWidget(),
    
    # VOLUME #
    seperator(),
    VolumeIcon(),
    VolumeWidget(),

    #  WIFI #
    seperator(),
    WifiIcon(),
    WifiWidget(),

    # CPU TEMP #
    seperator(),
    CpuTempIcon(),
    CpuTempWidget(),

    # CPU LOAD #
    seperator(),
    CpuLoadIcon(),
    CpuLoadWidget(),

    # BATTERY #
    seperator() if laptop else NothingWidget(),
    BatteryIcon() if laptop else NothingWidget(),
    BatteryWidget() if laptop else NothingWidget(),

    # WATTAGE #
    seperator() if laptop else NothingWidget(),
    WattageIcon() if laptop else NothingWidget(),
    WattageWidget() if laptop else NothingWidget(),

    # URGENT NOTIFICATION #
    seperator(),
    NotificationIcon(),
    NotificationWidget(),

    # BACKLIGHT #
    seperator() if laptop else NothingWidget(),
    BacklightIcon() if laptop else NothingWidget(),
    BacklightWidget() if laptop else NothingWidget(),

    # TIME #
    seperator(),
    MouseOverClock(),
    seperator(),

], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

top_bar_2 = Bar([
    # POWERBUTTON #
    seperator(),
    PowerButton(),

    # LAYOUTICON #
    seperator(),
    LayoutIcon(),

    # TICKTICK MENU #
    seperator(),
    TickTickMenu(),

    widget.Spacer(bar.STRETCH),

], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

bottom_bar_1 = Bar([
    # WINDOWCOUNT #
    WindowCountWidget(),

    # TASKLIST #
    seperator(background=transparent),
    widget.TaskList(**task_list_settings),

    # GROUPBOX #
    seperator(background=transparent),
    GroupBoxWidget(),

], bottom_bar_size, margin = bar_margin_bottom, background = bar_background_color, border_width = bar_width_bottom, border_color = bar_border_color, opacity=1)

bottom_bar_2 = Bar([
    # GROUPBOX #
    GroupBoxWidget(),

    # TASKLIST #
    seperator(background=transparent),
    widget.TaskList(**task_list_settings),

    # WINDOWCOUNT #
    seperator(background=transparent),
    WindowCountWidget(),

], bottom_bar_size, margin = bar_margin_bottom, background = bar_background_color, border_width = bar_width_bottom, border_color = bar_border_color, opacity=1)

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
if top_bar_on and bottom_bar_on:
    single_screen = Screen(top=single_top_bar, bottom=single_bottom_bar, left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
    left_screen   = Screen(top=top_bar_1, bottom=bottom_bar_1, left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
    right_screen  = Screen(top=top_bar_2, bottom=bottom_bar_2, left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
elif top_bar_on and not bottom_bar_on:
    single_screen = Screen(top=single_top_bar, bottom=bar.Gap(bar_gap_size), left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
    left_screen   = Screen(top=top_bar_1, bottom=bar.Gap(bar_gap_size), left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
    right_screen  = Screen(top=top_bar_2, bottom=bar.Gap(bar_gap_size), left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
elif bottom_bar_on and not top_bar_on:
    single_screen = Screen(top=bar.Gap(bar_gap_size), bottom=single_bottom_bar, left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
    left_screen   = Screen(top=bar.Gap(bar_gap_size), bottom=bottom_bar_1, left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
    right_screen  = Screen(top=bar.Gap(bar_gap_size), bottom=bottom_bar_2, left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
else:
    single_screen = Screen(top=bar.Gap(bar_gap_size), bottom=bar.Gap(bar_gap_size), left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
    left_screen   = Screen(top=bar.Gap(bar_gap_size), bottom=bar.Gap(bar_gap_size), left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
    right_screen  = Screen(top=bar.Gap(bar_gap_size), bottom=bar.Gap(bar_gap_size), left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))

amt_screens = 2
from Xlib import display
from Xlib.ext import randr
def configure_screens(startup=False):
    d = display.Display()
    s = d.screen()
    res = randr.get_screen_resources(s.root)
    global screens, amt_screens, laptop
    count = 0
    for output in res.outputs:
        params = randr.get_output_info(s.root, output, res.config_timestamp)
        data = params._data
        if data["connection"] == 0:
            count += 1
            log.warning(f"Connected is Monitor {data['name']}, screen count set to {count}")

    amt_screens = count
    if amt_screens == 2:
        if laptop:
            subprocess.run("xrandr --output eDP --mode 2560x1440 --rate 120 --pos 2976x117 --primary --output HDMI-A-0 --scale 1.55x1.55 --rate 120 --pos 0x0 --auto", shell=True)
            screens = [left_screen, right_screen]
        else:
            subprocess.run("xrandr --output DisplayPort-0 --mode 1920x1080 --rate 144 --output DisplayPort-2 --mode 1920x1080 --rate 144", shell=True)
            screens = [right_screen, left_screen]
    else:
        if laptop:
            subprocess.run("xrandr --output eDP --mode 2560x1440 --rate 120 --output HDMI-A-0 --off", shell=True)
        screens = [single_screen]
    if not startup:
        Qtile.reload_config()
    
configure_screens(startup=True)

### HOOKS ###
@hook.subscribe.screen_change
def _(notify_event):
    configure_screens()

@hook.subscribe.restart
def run_every_restart():
    log.info("top_bar_on", top_bar_on,"bottom_bar_on", bottom_bar_on)
        
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

wmname = "LG3D"
