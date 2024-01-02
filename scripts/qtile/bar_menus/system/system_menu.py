import gi
gi.require_version('Gtk', '3.0')
import os
import sys
import signal
import getpass
import subprocess
from gi.repository import Gtk, Gdk, GLib

class SystemMenu(Gtk.Dialog):
    def __init__(self, pid_file_path):
        Gtk.Dialog.__init__(self, "Sound Control", None, 0)

        signal.signal(signal.SIGTERM, self.handle_sigterm)

        self.x, self.y = 1050, 600
        self.move(1050, 600)

        self.window_width = 500
        self.window_height = 120

        self.set_size_request(self.window_width, self.window_height)

        self.pid_file_path = pid_file_path
        self.ignore_focus_lost = False
        self.active_option = "Turn off"
        self.active_option_number = 0

        self.content_area = self.get_content_area()

        self.content_area.get_style_context().add_class('content-area')
        self.get_style_context().add_class('root')

        self.css()
        self.title()
        self.options()

        self.connect("focus-out-event", self.on_focus_out)
        self.connect("key-press-event", self.on_key_press)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.main_box.pack_start(self.options_box, True, True, 0)

        self.content_area.pack_start(self.title_and_uptime_box, True, True, 0)   
        self.content_area.pack_start(self.main_box, True, True, 0)   

        self.show_all()

    def title(self):
        self.title_and_uptime_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self.title_and_uptime_box.get_style_context().add_class('title-and-uptime-root-box')
      
        self.title_box = Gtk.EventBox()
        self.title_box.get_style_context().add_class('title-box')
        self.title_box.set_name('title-box-turn-off')
        self.title_text = Gtk.Label()
        self.title_text.get_style_context().add_class('title')
        self.title_text.set_text(self.active_option)
        self.title_box.add(self.title_text)

        uptime_icon_box = Gtk.EventBox()
        uptime_icon_box.set_halign(Gtk.Align.END)
        uptime_icon_box.get_style_context().add_class('uptime-icon-box')
        uptime_icon = Gtk.Label()
        uptime_icon.get_style_context().add_class('uptime-icon')
        uptime_icon.set_text("")
        uptime_icon_box.add(uptime_icon)

        uptime_box = Gtk.EventBox()
        uptime_box.set_halign(Gtk.Align.END)
        uptime_box.get_style_context().add_class('uptime-box')
        uptime = Gtk.Label()
        uptime.get_style_context().add_class('uptime')
        uptime.set_text(self.get_uptime())
        uptime_box.add(uptime)

        user_icon_box = Gtk.EventBox()
        user_icon_box.set_halign(Gtk.Align.END)
        user_icon_box.get_style_context().add_class('user-icon-box')
        user_icon = Gtk.Label()
        user_icon.get_style_context().add_class('user-icon')
        user_icon.set_text("")
        user_icon_box.add(user_icon)

        username_box = Gtk.EventBox()
        username_box.set_halign(Gtk.Align.END)
        username_box.get_style_context().add_class('username-box')
        username = Gtk.Label()
        username.get_style_context().add_class('username')
        username.set_text(self.get_username())
        username_box.add(username)

        self.title_and_uptime_box.pack_start(self.title_box, False, True, 0)
        self.title_and_uptime_box.pack_start(user_icon_box, True, True, 0)
        self.title_and_uptime_box.pack_start(username_box, False, True, 0)
        self.title_and_uptime_box.pack_start(uptime_icon_box, False, True, 0)
        self.title_and_uptime_box.pack_start(uptime_box, False, True, 0)

    def options(self):
        self.options_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.options_box.get_style_context().add_class('options-root-box')

        turn_off_box = Gtk.EventBox()
        turn_off_box.get_style_context().add_class('options-box')
        turn_off_box.set_name("turn-off-box-active")
        turn_off_icon = Gtk.Label()
        turn_off_icon.get_style_context().add_class('options-icon')
        turn_off_icon.set_name("icon-active")
        turn_off_icon.set_text("")
        turn_off_box.add(turn_off_icon)

        reboot_box = Gtk.EventBox()
        reboot_box.get_style_context().add_class('options-box')
        reboot_icon = Gtk.Label()
        reboot_icon.get_style_context().add_class('options-icon')
        reboot_icon.set_name("reboot-inactive")
        reboot_icon.set_text("")
        reboot_box.add(reboot_icon)

        sleep_box = Gtk.EventBox()
        sleep_box.get_style_context().add_class('options-box')
        sleep_icon = Gtk.Label()
        sleep_icon.get_style_context().add_class('options-icon')
        sleep_icon.set_name("sleep-inactive")
        sleep_icon.set_text("")
        sleep_box.add(sleep_icon)

        hibernate_box = Gtk.EventBox()
        hibernate_box.get_style_context().add_class('options-box')
        hibernate_icon = Gtk.Label()
        hibernate_icon.get_style_context().add_class('options-icon')
        hibernate_icon.set_name("hibernate-inactive")
        hibernate_icon.set_text("")
        hibernate_box.add(hibernate_icon)

        logout_box = Gtk.EventBox()
        logout_box.get_style_context().add_class('options-box')
        logout_icon = Gtk.Label()
        logout_icon.get_style_context().add_class('options-icon')
        logout_icon.set_name("logout-inactive")
        logout_icon.set_text("")
        logout_box.add(logout_icon)

        self.options_box.pack_start(turn_off_box, True, True, 0)
        self.options_box.pack_start(reboot_box, True, True, 0)
        self.options_box.pack_start(sleep_box, True, True, 0)
        self.options_box.pack_start(hibernate_box, True, True, 0)
        self.options_box.pack_start(logout_box, True, True, 0)

        turn_off_option = {
            'text': 'Turn off',
            'title_box': 'title-box-turn-off',
            'command': 'systemctl poweroff',
            'box': turn_off_box,
            'active_box_name': 'turn-off-box-active',
            'inactive_box_name': 'box-inactive',
            'icon': turn_off_icon,
            'active_icon_name': 'icon-active',
            'inactive_icon_name': 'turn-off-inactive'
        }

        reboot_option = {
            'text': 'Reboot',
            'title_box': 'title-box-reboot',
            'command': 'systemctl reboot',
            'box': reboot_box,
            'active_box_name': 'reboot-box-active',
            'inactive_box_name': 'box-inactive',
            'icon': reboot_icon,
            'active_icon_name': 'icon-active',
            'inactive_icon_name': 'reboot-inactive'
        }

        sleep_option = {
            'text': 'Sleep',
            'title_box': 'title-box-sleep',
            'command': 'systemctl suspend',
            'box': sleep_box,
            'active_box_name': 'sleep-box-active',
            'inactive_box_name': 'box-inactive',
            'icon': sleep_icon,
            'active_icon_name': 'sleep-active',
            'inactive_icon_name': 'sleep-inactive'
        }

        hibernate_option = {
            'text': 'Hibernate',
            'title_box': 'title-box-hibernate',
            'command': 'systemctl hibernate',
            'box': hibernate_box,
            'active_box_name': 'hibernate-box-active',
            'inactive_box_name': 'box-inactive',
            'icon': hibernate_icon,
            'active_icon_name': 'icon-active',
            'inactive_icon_name': 'hibernate-inactive'
        }

        logout_option = {
            'text': 'Logout',
            'title_box': 'title-box-logout',
            'command': 'qtile stop',
            'box': logout_box,
            'active_box_name': 'logout-box-active',
            'inactive_box_name': 'box-inactive',
            'icon': logout_icon,
            'active_icon_name': 'icon-active',
            'inactive_icon_name': 'logout-inactive'
        }

        self.option_dict = {
            "0": turn_off_option,
            "1": reboot_option,
            "2": sleep_option,
            "3": hibernate_option,
            "4": logout_option
        }

    def css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        provider.load_from_path("/home/jonalm/scripts/qtile/bar_menus/system/system_menu_styles.css")
        visual = screen.get_rgba_visual()
        self.content_area.set_visual(visual)
        self.set_visual(visual)

    def next_active_option(self, prev=False, specified_option=-1):
        prev_option = self.option_dict[str(self.active_option_number)]
        prev_option['box'].set_name(prev_option['inactive_box_name'])
        prev_option['icon'].set_name(prev_option['inactive_icon_name'])

        if specified_option == -1:
            if prev:
                self.active_option_number -= 1
            else:
                self.active_option_number += 1

            if self.active_option_number == len(self.option_dict):
                self.active_option_number = 0
            elif self.active_option_number == -1:
                self.active_option_number = len(self.option_dict) - 1
        else:
            self.active_option_number = specified_option

        active_option = self.option_dict[str(self.active_option_number)]
        active_option['box'].set_name(active_option['active_box_name'])
        active_option['icon'].set_name(active_option['active_icon_name'])
        self.title_box.set_name(active_option['title_box'])
        self.title_text.set_text(active_option['text'])

        if specified_option != -1:
            GLib.timeout_add(1000, self.run_option_command())

    def run_option_command(self):
        subprocess.run(self.option_dict[str(self.active_option_number)]['command'], shell=True)
        self.exit_remove_pid()

    def get_uptime(self):
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            return self.format_uptime(uptime_seconds)

    def format_uptime(self, seconds):
        days, remainder = divmod(seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        if days != 0:
            days = f"{int(days)}d "
        else:
            days = ""
        if hours != 0:
            hours = f"{int(hours)}h "
        else:
            hours = ""
        minutes = f"{int(minutes)}m"

        return f"{days}{hours}{minutes}"

    def get_username(self):
        return getpass.getuser()

    def on_focus_out(self, widget, event, escape=False):
        if not self.ignore_focus_lost or escape:
            self.exit_remove_pid()

    def on_key_press(self, widget, event):
        keyval = event.keyval
        char = chr(keyval)
        
        if keyval == Gdk.KEY_Escape:
            self.on_focus_out(widget, event, True)
        elif event.keyval == Gdk.KEY_Left:
            self.next_active_option(prev=True)
        elif event.keyval == Gdk.KEY_Right:
            self.next_active_option()
        elif event.keyval == Gdk.KEY_Return or event.keyval == Gdk.KEY_KP_Enter:
            subprocess.run(self.option_dict[str(self.active_option_number)]["command"], shell=True) 
            self.exit_remove_pid()
        elif char == 'u':
            self.next_active_option(specified_option=0)
        elif char == 'r':
            self.next_active_option(specified_option=1)
        elif char == 's':
            self.next_active_option(specified_option=2)
        elif char == 'h':
            self.next_active_option(specified_option=3)

    def handle_sigterm(self, signum, frame):
        self.exit_remove_pid() 

    def exit_remove_pid(self):
        try:
            with open(self.pid_file_path, "r") as file:
                pid = int(file.read().strip())
            try:
                os.remove(self.pid_file_path)
                os.kill(pid, 15)
            except ProcessLookupError:
                pass
        finally:
            sys.exit(0)

if __name__ == '__main__':
    pid_file_path = "/home/jonalm/scripts/qtile/bar_menus/system/system_menu_pid_file.pid"
    dialog = None

    try:
        if os.path.isfile(pid_file_path):
            with open(pid_file_path, "r") as file:
                pid = int(file.read().strip())
            try:
                os.remove(pid_file_path)
                os.kill(pid, 15)            
            except ProcessLookupError:
                pass
        else:
            with open(pid_file_path, "w") as file:
                file.write(str(os.getpid()))

            dialog = SystemMenu(pid_file_path)
            Gtk.main()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sys.exit(0)
