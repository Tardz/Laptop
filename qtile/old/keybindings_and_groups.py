from colors import gruvbox
from libqtile.lazy import lazy
from libqtile.extension.dmenu import DmenuRun
from libqtile.config import Match, Key, KeyChord, Click, Drag, ScratchPad, Group, DropDown
from layouts import horizontal_layouts, vertical_layouts

mod1 = "Alt"
mod = "mod4"
myBrowser = "chromium"
myTerm = "alacritty"

### KEYBINDINGS ###
#-START_KEYS
keys = [
        #ESSENTIALS
        #Key([mod], "Return", lazy.spawn(myTerm), desc='Terminal'),
        Key([mod], "Tab", lazy.next_layout(), desc='Toggle through layouts'),
        Key([mod], "q", lazy.window.kill(), desc='Kill active window'),
        Key([mod, "shift"], "r", lazy.restart(), lazy.spawn("/home/jonalm/scripts/term/reset_screens.sh"), desc='Restart Qtile'),
        Key([mod, "shift"], "q", lazy.shutdown(), desc='Shutdown Qtile'),
        
        #SWITCH MONITOR FOCUS AND GROUPS
        Key([mod], "Left", lazy.to_screen(0), desc='Move focus to next monitor'),
        Key([mod], "Right", lazy.to_screen(1), desc='Move focus to next monitor'),
        Key(["mod1", "control"], "Right", lazy.screen.next_group(), desc='Next group right'),
        Key(["mod1", "control"], "Left", lazy.screen.prev_group(), desc='Next group left'),

        #WINDWOW CONTROLS  
        Key([mod], "Down", lazy.layout.down(), desc='Move focus down in current stack pane'),
        Key([mod], "Up", lazy.layout.up(), desc='Move focus up in current stack pane'),
        Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), lazy.layout.section_down(), desc='Move windows down in current stack'),
        Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), lazy.layout.section_up(), desc='Move windows up in current stack'),
        Key([mod, "control"], "Left", lazy.layout.shrink(), lazy.layout.decrease_nmaster(), desc='Shrink window'),
        Key([mod, "control"], "Right", lazy.layout.grow(), lazy.layout.increase_nmaster(), desc='Expand window'),
        Key([mod, "control"], "n", lazy.layout.normalize(), desc='normalize window size ratios'),
        Key([mod, "control"], "m", lazy.layout.maximize(), desc='toggle window between minimum and maximum sizes'),
        Key([mod], "f", lazy.window.toggle_floating(), desc='toggle floating'),
        Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),
        Key([mod], "z", lazy.window.toggle_minimize(), lazy.group.next_window(), desc="Minimize window"),

        #APPS
        Key([mod], "c", lazy.spawn(myBrowser), desc='Chromium'),
        Key([mod], "d", lazy.spawn("/usr/bin/discord"), desc='Discord'),
        Key([mod], "e", lazy.spawn("/usr/bin/emacs"), desc='Emacs'),
        Key([mod], "i", lazy.spawn("/usr/bin/code"), desc='VScode'),
        Key([mod], "m", lazy.spawn("/usr/bin/thunderbird"), desc='Mail'),
        Key([mod], "o", lazy.spawn("/home/jonalm/.webcatalog/microsoftexcelonline/microsoftexcelonline"), desc='Excel'),

        #URL
        Key([mod], "a", lazy.spawn("/home/jonalm/scripts/url/avanza.sh"), desc='Avanza'),
        Key([mod], "v", lazy.spawn("/home/jonalm/scripts/url/ig.sh"), desc='Ig'),
        Key([mod], "y", lazy.spawn("/home/jonalm/scripts/url/youtube.sh"), desc='Youtube'),
        Key([mod], "t", lazy.spawn("/home/jonalm/scripts/url/tradingview.sh"), desc='Tradingview'),
        Key([mod], "b", lazy.spawn("/home/jonalm/scripts/url/swedbank.sh"), desc='Swedbank'),

        #TERM
        Key([mod], "h", lazy.spawn("/home/jonalm/scripts/term/htop.sh"), desc='Htop'),
        Key([mod], "plus", lazy.spawn("/home/jonalm/scripts/term/show_keys.sh"), desc='Keybindings'),

        #ROFI
        Key([mod], "space", lazy.spawn("/home/jonalm/.config/rofi/files/launchers/type-1/launcher.sh"), desc='Rofi drun'),
        Key([mod], "Escape", lazy.spawn("/home/jonalm/.config/rofi/files/powermenu/type-3/powermenu.sh"), desc='Rofi powermenu'),
        Key([mod], "w", lazy.spawn("/home/jonalm/scripts/rofi/config_files.sh"), desc='Rofi config files'),
        Key([mod], "l", lazy.spawn("/home/jonalm/scripts/rofi/search_web.sh"), desc='Rofi web search'),
        #-END_KEYS
        #DMENU
        # Key([mod],               "space",  lazy.run_extension(DmenuRun(
        #     font                = "TerminessTTF Nerd Font",
        #     fontzise            = "13",
        #     dmenu_command       = "dmenu_run",
        #     dmenu_prompt        = ">",
        #     dmenu_height        = 10,
        #     background          = gruvbox["dmenubg"],
        #     foreground          = gruvbox["dmenufg"],
        #     selected_foreground = gruvbox["dmenuselfg"],
        #     selected_background = gruvbox["dmenubg"],
        #     ))),
        ]
        
### GROUP SETTINGS ###
#CIRCLE: 
# matches=[Match(wm_class='chromium')]
groups = [
        Group('Left',  label = "", layouts = horizontal_layouts),
        Group('4',     label = "", layouts = horizontal_layouts),
        Group('6',     label = "", layouts = horizontal_layouts),
        Group('3',     label = "", layouts = horizontal_layouts),
        Group('5',     label = "", layouts = horizontal_layouts),
        Group('Right', label = "", layouts = horizontal_layouts),
]

focus_value = True

### SCRATCHPAD ###
groups.append(ScratchPad('2', [
    DropDown('terminal', 'alacritty', warp_pointer=True, width=0.5, height=0.5, x=0.25, y=0.2, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('mixer', 'pavucontrol', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('net', 'nm-connection-editor', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('bluetooth', 'blueman-manager', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('filemanager', 'pcmanfm', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = focus_value),
    DropDown('music', 'spotify', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('todo', 'ticktick', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = focus_value),
    DropDown('passwords', '/home/jonalm/.webcatalog/LastPass/LastPass', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('drive', '/home/jonalm/.webcatalog/GoogleDrive/GoogleDrive', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=1, on_focus_lost_hide = focus_value),
    DropDown('github', '/home/jonalm/.webcatalog/GitHub/GitHub', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = focus_value),
    DropDown('githubPushLabb', '/home/jonalm/scripts/term/gitpushlabb.sh', warp_pointer=True, width=0.6, height=0.7, x=0.2, y=0.12, opacity=0.95, on_focus_lost_hide = focus_value),
    DropDown('githubPush', '/home/jonalm/scripts/term/gitpush.sh', warp_pointer=True, width=0.4, height=0.4, x=0.3, y=0.25, opacity=1, on_focus_lost_hide = focus_value)
]))

### MOVE WINDOW TO WORKSPACE ###
for i in groups:
    keys.extend([
        #WINDOWS
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name), desc="move focused window to group {}".format(i.name)),
        # Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name)),
        #SCRATCHPAD
        Key([mod], "Return", lazy.group['2'].dropdown_toggle('terminal')),
        Key([mod], "period", lazy.group['2'].dropdown_toggle('mixer')),
        Key([mod], "comma", lazy.group['2'].dropdown_toggle('net')),
        Key([mod], "n", lazy.group['2'].dropdown_toggle('filemanager')),
        Key([mod], "s", lazy.group['2'].dropdown_toggle('music')),
        Key([mod], "r", lazy.group['2'].dropdown_toggle('todo')), 
        Key([mod], "x", lazy.group['2'].dropdown_toggle('bluetooth')),
        Key([mod], "p", lazy.group['2'].dropdown_toggle('passwords')),
        Key([mod], "u", lazy.group['2'].dropdown_toggle('drive')),

        KeyChord([mod], "g",[
            Key([], "p", lazy.group['2'].dropdown_toggle('githubPush')),
            Key([], "g", lazy.group['2'].dropdown_toggle('github')),
            Key([], "o", lazy.group['2'].dropdown_toggle('githubPushLabb'))
            ]),
    ])

#DRAG FLOATING LAYOUTS
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position() ),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
    ]
