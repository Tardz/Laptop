from colors import gruvbox
from libqtile.bar import Bar
from libqtile.widget.cpu import CPU
from libqtile.widget.clock import Clock
from libqtile.widget.spacer import Spacer
from libqtile.widget.memory import Memory
from libqtile.widget.battery import Battery
from libqtile.widget.systray import Systray
from unicodes import right_arrow, left_arrow, upper_left_triangle
from libqtile.widget.groupbox import GroupBox
from libqtile.widget.tasklist import TaskList
from libqtile.widget.clipboard import Clipboard
from libqtile.widget.quick_exit import QuickExit
from libqtile.widget.window_count import WindowCount
from libqtile.widget.currentlayout import CurrentLayout
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration

colors = [
    ["#2e3440", "#2e3440"],  # 0 background
    ["#d8dee9", "#d8dee9"],  # 1 foreground
    ["#3b4252", "#3b4252"],  # 2 background lighter
    ["#bf616a", "#bf616a"],  # 3 red
    ["#a3be8c", "#a3be8c"],  # 4 green
    ["#ebcb8b", "#ebcb8b"],  # 5 yellow
    ["#81a1c1", "#81a1c1"],  # 6 blue
    ["#b48ead", "#b48ead"],  # 7 magenta
    ["#88c0d0", "#88c0d0"],  # 8 cyan
    ["#e5e9f0", "#e5e9f0"],  # 9 white
    ["#4c566a", "#4c566a"],  # 10 grey
    ["#d08770", "#d08770"],  # 11 orange
    ["#8fbcbb", "#8fbcbb"],  # 12 super cyan
    ["#5e81ac", "#5e81ac"],  # 13 super blue
    ["#242831", "#242831"],  # 14 super dark background
]

### WIDGET SETTINGS ###
widget_defaults = dict(font ='TerminessTTF Nerd Font', fontsize = 23, padding = 18,)


### BAR ON SCREEN 1 ###
# - powerbutton
bar = Bar([
    Spacer(length = 4, background = gruvbox['systray']),

    QuickExit(countdown_format = '', countdown_start = 1, default_text = '',
              background = gruvbox['systray'], foreground = gruvbox['bartext']),

    Spacer(length = 5, background = gruvbox['systray']),

    right_arrow(gruvbox['arrow2'], gruvbox['systray']),

    Spacer(background = gruvbox['arrow2'], length = 4),

    Battery(format = '󰂂 {percent:2.0%} 󱐋 {watt:.2f} W', update_interval = 3, 
            background = gruvbox['arrow2'], foreground = gruvbox['bartext']),

    right_arrow(gruvbox['arrow3'], gruvbox['arrow2']),

    CPU(format = '  {load_percent}%', update_interval = 3,
        background = gruvbox['arrow3'], foreground = gruvbox['bartext']),

    right_arrow(gruvbox['arrow1'], gruvbox['arrow3']),

    Clock(background = gruvbox['arrow1'], foreground = gruvbox['bartext'], format = '  %R'),

    right_arrow(gruvbox['background'], gruvbox['arrow1']),
    
    Spacer(length=15),

    TaskList(padding = 4, spacing = 6, icon_size = 22, margin = 1, borderwidth = 2,
             max_title_width = 500, txt_floating = ' 缾 ', txt_maximized = ' 类 ', 
             txt_minimized = ' 絛 ', highlight_method = 'block', border = gruvbox['tasklistborder'],
             unfocused_border = gruvbox['tasklistunborder'], foreground = gruvbox['tasklistfg']),

    Spacer(length = 15),

    left_arrow(gruvbox['background'], gruvbox['arrow1']),


    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=28,
        padding=0,
    ),
    CurrentLayout(background = gruvbox['arrow1'], foreground = gruvbox['bartext']),
    widget.TextBox(
        text="",
        foreground=colors[14],
        background=colors[0],
        fontsize=30,
        padding=0,
        ),

    left_arrow(gruvbox['arrow1'], gruvbox['arrow2']),

    WindowCount(text_format = '{num} 缾', background = gruvbox['arrow2'], foreground = gruvbox['bartext'], show_zero = True),

    left_arrow(gruvbox['arrow2'], gruvbox['groupboxbg']),

    GroupBox(disable_drag = True, visible_groups = ['1', '2', '3', '4'], active = gruvbox['groupboxactive'],
             inactive = gruvbox['groupboxinactive'], highlight_method = 'line', block_highlight_text_color = gruvbox['groupboxcurrent'],
             borderwidth = 0, highlight_color = gruvbox['groupboxbg'], background = gruvbox['groupboxbg']),

    Spacer(length = 5, background = gruvbox['groupboxbg']),

    ], background = gruvbox['background'], size = 38, margin=[0, 0, 21, 0], border_width=[0, 0, 3, 0], opacity = 1)