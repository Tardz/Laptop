from libqtile import qtile as Qtile
from libqtile.lazy import lazy
from settings import *
import subprocess
import re

@lazy.function
def move_focus_and_mouse(qtile, group):
    """
    Moves focus to correct screen depending on what group is passed
    aswell as moving the mouse.
    """
    global amt_screens
    if amt_screens == 2:
        monitor = check_dict[group][2]
        qtile.cmd_to_screen(monitor)
        if laptop: #Quick fix
            if monitor == 0:
                qtile.cmd_spawn("xdotool mousemove 4300 900")
            elif monitor == 1:
                qtile.cmd_spawn("xdotool mousemove 1500 800")
        else:
            if monitor == 0:
                qtile.cmd_spawn("xdotool mousemove 1000 500")
            elif monitor == 1:
                qtile.cmd_spawn("xdotool mousemove 2900 500")

@lazy.function
def spawn_alttab_once(qtile):
    """
    Bug when spawning alttab from autostart so this is used for
    manual launching.
    """
    if not alttab_spawned:
        qtile.cmd_spawn('alttab -bg "#2e3440" -fg "#d8dee9" -bc "#2e3440" -bw 18 -inact "#3b4252" -frame "#81a1c1"')

@lazy.function
def check(qtile, group_name=None, from_key_press=None):
    """
    Checks if a specified app from the check_dict dictionary is in the passed group,
    if not, launch the specified app else, do nothing.
    """
    if from_key_press:
        qtile.cmd_spawn(["/home/jonalm/scripts/qtile/check_and_launch_app.py", from_key_press[0], from_key_press[1], from_key_press[2]])
    elif group_name and check_dict[group_name][0]:
        info = check_dict[group_name]
        if info != []:
            try:
                command = ""
                if info[1]:
                    command = info[1]

                qtile.cmd_spawn(["/home/jonalm/scripts/qtile/check_and_launch_app.py", info[0], group_name, command])
            except Exception as e:
                pass
                # log.exception(f"Error in check function: {e}")
                # log.debug("END OF ERROR\n")

@lazy.function
def notify(qtile, group_name):
    """
    Notification sent when moving a window between groups.
    """
    try:
        group_name_upper = group_name.upper()

        qtile.cmd_spawn(f'notify-send -u low -t 1000 \'-h\' \'int:transient:1\' "Sent to ""{group_name_upper} "')
    except Exception as e:
        pass
        # log.exception(f"Error in check function: {e}")
        # log.debug("END OF ERROR\n")

@lazy.function
def close_all_windows(qtile):
    """
    Kills all windows.
    """
    for group in qtile.groups:
        for window in group.windows:
            window.kill()

@lazy.function
def get_next_screen_group(qtile):
    """
    Retrieves the next screen group.
    """
    ## NOT WORKING
    qtile.cmd_spawn(["qtile", "cmd-obj", "-o", "cmd", "-f", "next_screen"])
    data = subprocess.check_output(["qtile", "cmd-obj", "-o", "group", "-f", "info"]).decode().strip()

    matches = re.findall(r"'name': '([^']+)'", data)

    if len(matches) >= 2:
        group_name = matches[1]
        return group_name
    else:
        pass
        # log.error("Group not found.")

@lazy.function
def mute_or_unmute(qtile):
    """
    Launches script that either mutes or unmutes depending on the 
    state before execution.
    """
    qtile.cmd_spawn("/home/jonalm/scripts/qtile/mute_or_unmute.sh")

@lazy.function
def show_or_hide_tabs(screen=None, offset=0):
    if screen is None:
        screen = Qtile.current_screen   

    bar = screen.bottom
    if not bar:
        return

    nwindows = len(screen.group.windows) + offset
    if nwindows > 1:
        bar.show()
    else:
        if bar.window:
            bar.show(False)

@lazy.function
def minimize_windows(qtile):
    """
    Minimizes all windows wihtin current group.
    """
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()

@lazy.function
def swap_screens(qtile):
    """
    Swaps groups betwwen screen one and two by using a script.
    """
    qtile.cmd_spawn("/home/jonalm/scripts/qtile/get_next_screen_group.py")
    screen = Qtile.current_screen
    qtile.current_group.toscreen()