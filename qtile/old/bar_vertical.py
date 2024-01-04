from colors import gruvbox
from libqtile.bar import Bar
from libqtile.widget.cpu import CPU
from libqtile.widget.clock import Clock
from libqtile.widget.spacer import Spacer
from libqtile.widget.memory import Memory
from libqtile.widget.systray import Systray
from unicodes import right_arrow, left_arrow
from libqtile.widget.groupbox import GroupBox
from libqtile.widget.tasklist import TaskList
from libqtile.widget.clipboard import Clipboard
from libqtile.widget.quick_exit import QuickExit
from libqtile.widget.window_count import WindowCount
from libqtile.widget.currentlayout import CurrentLayout

### WIDGET SETTINGS ###
widget_defaults = dict(
    font     ='TerminessTTF Nerd Font',
    fontsize = 13,
    padding  = 10,
    )

### BAR ON SCREEN 1 ###
bar = Bar([
    QuickExit(
        countdown_format = '',
        countdown_start  = 1,
        default_text     = '',
        background       = gruvbox['arrow2'],
        foreground       = gruvbox['bartext']
    ),

    Spacer(
        background = gruvbox['arrow2'],
        length     = 4
    ),

    left_arrow(
        gruvbox['arrow2'],
        gruvbox['systray']
    ),

    Systray(
        background = gruvbox['systray'], icon_size=15
    ),

    Spacer(
        background = gruvbox['systray'],
        length     = 5
    ),

    right_arrow(
        gruvbox['arrow2'],
        gruvbox['systray']
    ),

    #Clipboard(
    #    background  = gruvbox['arrow2'],
    #    foreground  = gruvbox['bartext'],
    #    scroll      = True
    #),

    Memory(
         format      = ' {MemUsed: .0f} /{MemTotal: .0f}',
         measure_mem = 'G',
         background  = gruvbox['arrow2'],
         foreground  = gruvbox['bartext']
    ),

    right_arrow(
        gruvbox['arrow3'],
        gruvbox['arrow2']
    ),

    CPU(
        format     ='  {load_percent}%',
        background = gruvbox['arrow3'],
        foreground = gruvbox['bartext']
    ),

    right_arrow(
        gruvbox['arrow1'],
        gruvbox['arrow3']
    ),

    Clock(
        background = gruvbox['arrow1'],
        foreground = gruvbox['bartext'],
        format     ='  %R'
    ),

    right_arrow(
        gruvbox['background'],
        gruvbox['arrow1']
    ),

    Spacer(length=8),

    TaskList(
        padding          = 4,
        spacing          = 3,
        icon_size        = 12,
        margin           = 1,
        borderwidth      = 1,
        max_title_width  = 300,
        txt_floating     =' 缾 ',
        txt_maximized    = ' 类 ',
        txt_minimized    = ' 絛 ',
        highlight_method = 'block',
        border           = gruvbox['tasklistborder'],
        unfocused_border = gruvbox['tasklistunborder'],
        foreground       = gruvbox['tasklistfg']
    ),

    Spacer(8),

    left_arrow(
        gruvbox['background'],
        gruvbox['arrow1']
        ),

    CurrentLayout(
        background = gruvbox['arrow1'],
        foreground = gruvbox['bartext']
    ),

    left_arrow(
        gruvbox['arrow1'],
        gruvbox['arrow2']
    ),

    WindowCount(
        text_format = '{num} 缾',
        background  = gruvbox['arrow2'],
        foreground  = gruvbox['bartext'],
        show_zero   = True,
    ),

    left_arrow(
        gruvbox['arrow2'],
        gruvbox['groupboxbg']
    ),

    GroupBox(
        disable_drag               = True,
        visible_groups             = ['6', '4', 'Left'],
        active                     = gruvbox['groupboxactive'],
        inactive                   = gruvbox['groupboxinactive'],
        highlight_method           = 'line',
        block_highlight_text_color = gruvbox['groupboxcurrent'],
        borderwidth                = 0,
        highlight_color            = gruvbox['groupboxbg'],
        background                 = gruvbox['groupboxbg']
    ),

    Spacer(
        length     = 5,
        background = gruvbox['groupboxbg']
    ),

    ],  background = gruvbox['background'], size = 24, margin = 8, opacity = 1)

### BAR ON SCREEN 2 ###
bar2 = Bar([
    GroupBox(
        disable_drag               = True,
        visible_groups             = ['Right', '3', '5'],
        active                     = gruvbox['groupboxactive'],
        inactive                   = gruvbox['groupboxinactive'],
        highlight_method           = 'line',
        block_highlight_text_color = gruvbox['groupboxcurrent'],
        borderwidth                = 0,
        highlight_color            = gruvbox['groupboxbg'],
        background                 = gruvbox['groupboxbg']
    ),

    right_arrow(
        gruvbox['arrow2'],
        gruvbox['groupboxbg']
    ),

    WindowCount(
        text_format = '{num} 缾',
        background  = gruvbox['arrow2'],
        foreground  = gruvbox['bartext'],
        show_zero   = True,
    ),

    right_arrow(
        gruvbox['arrow1'],
        gruvbox['arrow2']
    ),

    CurrentLayout(
        background = gruvbox['arrow1'],
        foreground = gruvbox['bartext']
    ),

    right_arrow(
        gruvbox['background'],
        gruvbox['arrow1']
        ),

    Spacer(length=8),

    TaskList(
        padding          = 4,
        spacing          = 3,
        icon_size        = 12,
        margin           = 1,
        borderwidth      = 1,
        max_title_width  = 300,
        txt_floating     = ' 缾 ',
        txt_maximized    = ' 类 ',
        txt_minimized    = ' 絛 ',
        highlight_method = 'block',
        border           = gruvbox['tasklistborder'],
        unfocused_border = gruvbox['tasklistunborder'],
        foreground       = gruvbox['tasklistfg']
    ),

    Spacer(length=8),

    ], background = gruvbox['background'], size = 24, margin = 8, opacity = 1)
