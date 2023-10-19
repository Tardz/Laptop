
def lower_left_triangle(bg_color, fg_color):
    return TextBox(
        text='\u25e2',
        padding=-8,
        fontsize=50,
        background=bg_color,
        foreground=fg_color
        )
def left_circle():
    return TextBox(
        text = "",
        foreground = widget_background_color,
        background = bar_background_color,
        fontsize = circle_size,
        padding = circle_padding,
    )

def right_circle():
    return TextBox(
        text="",
        foreground = widget_background_color,
        background = bar_background_color,
        fontsize = circle_size,
        padding = circle_padding,
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


# seperator(1),
# widget.CurrentLayoutIcon(
#     custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
#     foreground = layouticon_Background,
#     background = layouticon_Background,
#     padding = layouticon_padding,
#     scale = layouticon_scale,
# ),


    #DropDown('passwords', '/home/jonalm/.webcatalog/LastPass/LastPass', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=1, on_focus_lost_hide = focus_value),
    #DropDown('drive', '/home/jonalm/.webcatalog/GoogleDrive/GoogleDrive', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=1, on_focus_lost_hide = focus_value),
    #DropDown('github', '/home/jonalm/.webcatalog/GitHub/GitHub', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = focus_value),
    #DropDown('githubPushLabb', '/home/jonalm/scripts/term/gitpushlabb.sh', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = focus_value),
    #DropDown('githubPush', '/home/jonalm/scripts/term/gitpush.sh', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = focus_value)

    #Key([], "XF86Launch3", lazy.spawn("asusctl led-mode -n"), desc='Aurora key'),
    #Key([], "XF86Launch4", lazy.spawn("asusctl profile -n"), desc='Aurora key'),