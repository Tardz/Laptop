from libqtile.widget.textbox import TextBox

def lower_left_triangle(bg_color, fg_color):
    return TextBox(
        text='\u25e2',
        padding=-8,
        fontsize=50,
        background=bg_color,
        foreground=fg_color
        )

def left_arrow(bg_color, fg_color):
    return TextBox(
        text='\uE0B2',
        padding=0,
        fontsize=34,
        background=bg_color,
        foreground=fg_color
        )

def right_arrow(bg_color, fg_color):
    return TextBox(
        text='\uE0B0',
        padding=0,
        fontsize=34,
        background=bg_color,
        foreground=fg_color
        )

def upper_left_triangle(bg_color, fg_color):
    return TextBox(
        text="\u25E4",
        padding=-10,
        fontsize=100,
        background=bg_color,
        foreground=fg_color
        )

def upper_right_triangle(bg_color, fg_color):
    return TextBox(
        text="\u25E5",
        padding=-10,
        fontsize=100,
        background=bg_color,
        foreground=fg_color
        )

