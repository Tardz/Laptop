from libqtile.config import Match, ScratchPad, Group, DropDown
from settings import *

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