from colors import gruvbox
from libqtile.bar import Bar
from libqtile.widget.cpu import CPU
from libqtile.widget.clock import Clock
from libqtile.widget.spacer import Spacer
from libqtile.widget.memory import Memory
from libqtile.widget.battery import Battery
from libqtile.widget.systray import Systray
from unicodes import right_arrow, left_arrow, upper_left_triangle, upper_right_triangle
from libqtile.widget.groupbox import GroupBox
from libqtile.widget.tasklist import TaskList
from libqtile.widget.clipboard import Clipboard
from libqtile.widget.quick_exit import QuickExit
from libqtile.widget.window_count import WindowCount
from libqtile.widget.currentlayout import CurrentLayout

### WIDGET SETTINGS ###
widget_defaults = dict(font ='ttf-font-awesome', fontsize = 23, padding = 18,)

### BAR ON SCREEN 1 ###
bar = Bar([
    QuickExit( countdown_format = '', countdown_start  = 1, default_text = '', 
              background = gruvbox['arrow2'], foreground       = gruvbox['bartext']),

    Spacer(background = gruvbox['arrow2'], length = 4),

    upper_right_triangle(gruvbox['arrow2'], gruvbox['systray']),
    
    Systray(background = gruvbox['systray'], icon_size=28),
    
    Spacer(background = gruvbox['systray'], length = 15),

    upper_left_triangle(gruvbox['arrow2'], gruvbox['systray']),
    
    Battery(format = '󰂂 {percent:2.0%} 󱐋 {watt:.2f} W', update_interval = 3, 
            background  = gruvbox['arrow2'], foreground  = gruvbox['bartext']),
    
    upper_left_triangle(gruvbox['arrow3'], gruvbox['arrow2']),
    
    CPU(format ='  {load_percent}%', background = gruvbox['arrow3'], foreground = gruvbox['bartext']),
    
    upper_left_triangle(gruvbox['arrow1'], gruvbox['arrow3']),
    
    Clock(background = gruvbox['arrow1'], foreground = gruvbox['bartext'], format ='  %R'),
    
    upper_left_triangle(gruvbox['background'], gruvbox['arrow1']),

    Spacer(length=8),

    TaskList(
        padding          = 4,
        spacing          = 6,
        icon_size        = 22,
        margin           = 1,
        borderwidth      = 2,
        max_title_width  = 300,
        txt_floating     = ' 缾 ',
        txt_maximized    = ' 类 ',
        txt_minimized    = ' 絛 ',
        highlight_method = 'block',
        border           = gruvbox['tasklistborder'],
        unfocused_border = gruvbox['tasklistunborder'],
        foreground       = gruvbox['tasklistfg']
    ),

    Spacer(8),

    upper_right_triangle(gruvbox['background'], gruvbox['arrow1']),

    CurrentLayout(background = gruvbox['arrow1'], foreground = gruvbox['bartext']),

    upper_right_triangle(gruvbox['arrow1'], gruvbox['arrow2']),

    WindowCount(text_format = '{num} 缾', background = gruvbox['arrow2'], 
                foreground = gruvbox['bartext'], show_zero = True,),

    upper_right_triangle(gruvbox['arrow2'], gruvbox['groupboxbg']),

    GroupBox(
        disable_drag               = True,
        visible_groups             = ['1', '2', '3', '4'],
        active                     = gruvbox['groupboxactive'],
        inactive                   = gruvbox['groupboxinactive'],
        highlight_method           = 'line',
        block_highlight_text_color = gruvbox['groupboxcurrent'],
        borderwidth                = 0,
        highlight_color            = gruvbox['groupboxbg'],
        background                 = gruvbox['groupboxbg']
    ),

    Spacer(length = 5, background = gruvbox['groupboxbg']),

    ], background = gruvbox['background'], size = 38, margin = 0, opacity = 1)