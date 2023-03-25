from libqtile.bar import Bar
from libqtile.widget.clock import Clock
from libqtile.widget.cpu import CPU
from libqtile.widget.currentlayout import CurrentLayout
from libqtile.widget.groupbox import GroupBox
from libqtile.widget.memory import Memory
from libqtile.widget.spacer import Spacer
from libqtile.widget.systray import Systray
from libqtile.widget.window_count import WindowCount
from libqtile.widget.windowtabs import WindowTabs
from libqtile.widget.tasklist import TaskList
from libqtile.widget.check_updates import CheckUpdates
from libqtile.widget.quick_exit import QuickExit
from libqtile.widget.sensors import ThermalSensor
from libqtile.widget.volume import Volume
from libqtile.widget.bluetooth import Bluetooth
from libqtile.widget.sep import Sep

from unicodes import right_arrow, left_arrow
from colors import gruvbox

### WIDGET SETTINGS ###
widget_defaults = dict(
    font     ='TerminessTTF Nerd Font',
    fontsize = 13,
    padding  = 10,
    )

### BAR ON SCREEN 1 ###
bar = Bar([
    GroupBox(
        disable_drag=True,
        active=gruvbox['groupboxactive'],
        inactive=gruvbox['groupboxinactive'],
        highlight_method='line',
        block_highlight_text_color=gruvbox['groupboxcurrent'],
        borderwidth=0,
        highlight_color=gruvbox['groupboxbg'],
        background=gruvbox['groupboxbg']
    ),

    right_arrow(gruvbox['background'], gruvbox['groupboxbg']),
    Spacer(8),
    TaskList(padding=3, highlight_method='block', border='#3a3a3a',unfocused_border='#262626', foreground=gruvbox['bartext']),

    left_arrow(gruvbox['background'], gruvbox['arrow1']),
    WindowCount(text_format='{num} 缾', background=gruvbox['arrow1'], foreground=gruvbox['bartext'], show_zero=True,),
    
    left_arrow(gruvbox['arrow1'], gruvbox['arrow2']),
    CurrentLayout(background=gruvbox['arrow2'], foreground=gruvbox['bartext']),

    ], background=gruvbox['background'], size=24, margin=0, opacity=0.95)

### BAR ON SCREEN 2 ###
bar2 = Bar([
    CurrentLayout( background=gruvbox['arrow2'], foreground=gruvbox['bartext']),
    right_arrow(gruvbox['arrow1'], gruvbox['arrow2']),

    WindowCount(text_format='缾 {num}', background=gruvbox['arrow1'], foreground=gruvbox['bartext'], show_zero=True,),

    right_arrow(gruvbox['background'], gruvbox['arrow1']),
    Spacer(8),

    TaskList(padding=3, highlight_method='block', border='#3a3a3a',unfocused_border='#262626', foreground=gruvbox['bartext']),

    left_arrow(gruvbox['background'], gruvbox['arrow1']),
    ThermalSensor(format=" {temp:.1f}{°}", background=gruvbox['arrow1'], foreground=gruvbox['bartext']),

    left_arrow(gruvbox['arrow1'], gruvbox['arrow2']),
    CPU(format='{load_percent}%', background=gruvbox['arrow2'], foreground=gruvbox['bartext']),

    left_arrow(gruvbox['arrow2'], gruvbox['arrow1']),
    Memory(format=' {MemUsed: .0f}{mm} /{MemTotal: .0f}{mm}', background=gruvbox['arrow1'], foreground=gruvbox['bartext']),

    left_arrow(gruvbox['arrow1'], gruvbox['arrow2']),
    Clock(background=gruvbox['arrow2'], foreground=gruvbox['bartext'], format=' %Y-%m-%d %R'),

    left_arrow(gruvbox['arrow2'], gruvbox['arrow3']),
    Systray(background=gruvbox['arrow3']),
    CheckUpdates(display_format="  {updates}" ,background=gruvbox['arrow3'], foreground=gruvbox['bartext']),
    #Volume(background=gruvbox['arrow3'], foreground=gruvbox['bartext']),
    Spacer(background=gruvbox['arrow3'], length=11),
    Sep(background=gruvbox['arrow3'], foreground=gruvbox['sep'], size_percent=60, linewidth=1),
    QuickExit(countdown_format='', countdown_start=1, default_text='', background=gruvbox['arrow3'], foreground=gruvbox['bartext']),
    Spacer(length=5, background=gruvbox['arrow3'])

    ], background=gruvbox['background'], size=24, margin=0, opacity=0.95)
