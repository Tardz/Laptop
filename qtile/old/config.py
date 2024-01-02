import os
import subprocess
from typing import List
from libqtile import hook
from libqtile import qtile
from libqtile.config import Screen
from bar_vertical import bar, bar2, widget_defaults
from keybindings_and_groups import keys, groups, mouse, mod
from layouts import layouts, horizontal_layouts, vertical_layouts, floating_layout

#-- DECLARING WIDGET SETTINGS --#
extension_defaults = widget_defaults.copy()

#-- DECLARING PANEL --#
screens = [Screen(top=bar), Screen(top=bar2)]

#-- OTHER QTILE SETTINGS --#
dgroups_key_binder         = None
dgroups_app_rules          = []  # type: List
follow_mouse_focus         = True
bring_front_click          = True
cursor_warp                = False
auto_fullscreen            = True
focus_on_window_activation = "smart"
reconfigure_screens        = True
auto_minimize              = True

#-- START PROCESS --#
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])
    #- SCRATCHPAD
    qtile.cmd_simulate_keypress([mod],               'period')
    qtile.cmd_simulate_keypress([mod],               'comma' )
    qtile.cmd_simulate_keypress([mod],               'n'     )
    qtile.cmd_simulate_keypress([mod],               's'     )
    qtile.cmd_simulate_keypress([mod],               'r'     )
    qtile.cmd_simulate_keypress([mod],               'x'     )
    qtile.cmd_simulate_keypress([mod],               'p'     )
    #- SWITCH GROUP
    qtile.cmd_simulate_keypress([mod],               "Right" )
    qtile.cmd_simulate_keypress(["mod1", "control"], "Right" )
    qtile.cmd_simulate_keypress(["mod1", "control"], "Right" )
    qtile.cmd_simulate_keypress(["mod1", "control"], "Right" )
    qtile.cmd_simulate_keypress(["mod1", "control"], "Right" )
    qtile.cmd_simulate_keypress([mod], 'Left')

wmname = "LG3D"
