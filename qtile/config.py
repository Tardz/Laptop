### CONF IMPORTS ###
from libqtile.config import Screen
from libqtile import hook
import subprocess
import os

### SHARED ###
from libqtile import qtile as Qtile
from libqtile import bar
from settings import *

### QTILE VARS ###
from layouts import layouts, floating_layout
from keybindings import keys, mouse
from groups import groups
from widgets import extension_defaults

if bar_style == "box":
    from bars import (
        box_style_single_top_bar as single_top_bar, 
        box_style_single_bottom_bar as single_bottom_bar,
        box_style_dual_top_bar_1 as dual_top_bar_1,
        box_style_dual_top_bar_2 as dual_top_bar_2,
        box_style_dual_bottom_bar_1 as dual_bottom_bar_1,
        box_style_dual_bottom_bar_2 as dual_bottom_bar_2
    )
else:
    from bars import (
        simple_style_single_top_bar as single_top_bar, 
        simple_style_single_bottom_bar as single_bottom_bar,
        simple_style_dual_top_bar_1 as dual_top_bar_1,
        simple_style_dual_top_bar_2 as dual_top_bar_2,
        simple_style_dual_bottom_bar_1 as dual_bottom_bar_1,
        simple_style_dual_bottom_bar_2 as dual_bottom_bar_2
    )

if top_bar_on and bottom_bar_on:
    single_screen = Screen(top=single_top_bar, bottom=single_bottom_bar, left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
    left_screen   = Screen(top=dual_top_bar_1, bottom=dual_bottom_bar_1, left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
    right_screen  = Screen(top=dual_top_bar_2, bottom=dual_bottom_bar_2, left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
elif top_bar_on and not bottom_bar_on:
    single_screen = Screen(top=single_top_bar, bottom=bar.Gap(bar_gap_size), left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
    left_screen   = Screen(top=dual_top_bar_1, bottom=bar.Gap(bar_gap_size), left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
    right_screen  = Screen(top=dual_top_bar_2, bottom=bar.Gap(bar_gap_size), left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
elif bottom_bar_on and not top_bar_on:
    single_screen = Screen(top=bar.Gap(bar_gap_size), bottom=single_bottom_bar, left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
    left_screen   = Screen(top=bar.Gap(bar_gap_size), bottom=dual_bottom_bar_1, left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
    right_screen  = Screen(top=bar.Gap(bar_gap_size), bottom=dual_bottom_bar_2, left=bar.Gap(bar_gap_size), right=bar.Gap(bar_gap_size))
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
            # log.warning(f"Connected is Monitor {data['name']}, screen count set to {count}")

    amt_screens = count
    if amt_screens == 2:
        if laptop:
            subprocess.run("xrandr --output eDP --mode 2560x1440 --rate 120 --pos 2976x117 --primary --output HDMI-A-0 --scale 1.55x1.55 --rate 120 --pos 0x0 --auto", shell=True)
            screens = [left_screen, right_screen]
        else:
            # subprocess.run("xrandr --output DisplayPort-0 --mode 1920x1080 --rate 144 --output DisplayPort-2 --mode 1920x1080 --rate 144", shell=True)
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
        
@hook.subscribe.suspend
def lock_on_sleep():
    Qtile.spawn("sudo sddm")

def float_to_front():
    for group in Qtile.groups:
        for window in group.windows:
            if window.floating:
                window.cmd_bring_to_front()

@hook.subscribe.focus_change
def client_focus():
    current_window = Qtile.current_window
    if current_window is not None:
        if not current_window.floating:
            float_to_front()
        else:
            current_window.cmd_bring_to_front()

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

wmname = "LG3D"
