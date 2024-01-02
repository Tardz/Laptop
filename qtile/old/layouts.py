from colors import gruvbox
from libqtile.config import Match
from libqtile.layout.stack import Stack
from libqtile.layout.xmonad import MonadTall
from libqtile.layout.xmonad import MonadWide
from libqtile.layout.floating import Floating

mod = "mod4"

### LAYOUT SETTINGS ###
layouts = [
    MonadWide(
        border_normal       = gruvbox['windowoutline'],
        border_focus        = gruvbox['windowfocus1'],
        border_width        = 2,
        num_stacks          = 1,
        margin              = 8,
    ),
    Stack(
        border_normal       = gruvbox['windowoutline'],
        border_focus        = gruvbox['windowfocus1'],
        border_width        = 2,
        num_stacks          = 1,
        margin              = 8,
    ),
    MonadTall(
        border_normal       = gruvbox['windowoutline'],
        border_focus        = gruvbox['windowfocus0'],
        margin              = 8,
        border_width        = 2,
        single_border_width = 2,
        single_margin       = 8,
    )
]

horizontal_layouts = [
    Stack(
        border_normal       = gruvbox['windowoutline'],
        border_focus        = gruvbox['windowfocus1'],
        border_width        = 2,
        num_stacks          = 1,
        margin              = 8,
    ),
    MonadTall(
        border_normal       = gruvbox['windowoutline'],
        border_focus        = gruvbox['windowfocus0'],
        margin              = 8,
        border_width        = 2,
        single_border_width = 2,
        single_margin       = 8,
    )
]

vertical_layouts = [
    MonadWide(
        border_normal       = gruvbox['windowoutline'],
        border_focus        = gruvbox['windowfocus1'],
        border_width        = 2,
        num_stacks          = 1,
        margin              = 8,
    ),
    Stack(
        border_normal       = gruvbox['windowoutline'],
        border_focus        = gruvbox['windowfocus1'],
        border_width        = 2,
        num_stacks          = 1,
        margin              = 8,
    )
]

### FLOATING LAYOUT SETTINGS AND ASSIGNED APPS ###
floating_layout = Floating(
    border_normal = gruvbox['windowoutline'],
    border_focus  = gruvbox['windowfocus1'],
    border_width  = 3,
    float_rules   = [
        *Floating.default_float_rules,
        Match(wm_class = "nitrogen"            ),
        Match(wm_class = "pavucontrol"         ),
        Match(wm_class = "nm-connection-editor"),
        Match(wm_class = "yad"),
        Match(wm_class = "qalculate-qt"),
        Match(wm_class = "se-liu-davhe786_jonal155-Run"),
        ])