import gi
gi.require_version('Gtk', '3.0')
import subprocess
import os
from Xlib import display 
from gi.repository import Gtk, Gdk

class CustomDialog(Gtk.Dialog):
    def __init__(self):
        self.pid_file = "/home/jonalm/scripts/qtile/bar_menus/power_managment_pid_file.pid"
        Gtk.Dialog.__init__(self, "Custom Dialog", None, 0)
        self.set_default_size(100, 40)

        x, y = self.get_mouse_position()

        if x is not None and y is not None:
            self.move(x - 225, y - 50)

        self.connect("focus-out-event", self.on_focus_out)

        option = self.read_option_from_file()

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        automatic_button = Gtk.Button("Automatic")
        automatic_button.connect("clicked", self.on_automatic_button_clicked)
        style = automatic_button.get_style_context()
        style.add_class("Automatic")
        automatic_button.set_hexpand(True)
        automatic_button.set_vexpand(True)

        powersave_button = Gtk.Button("Powersave")
        powersave_button.connect("clicked", self.on_powersave_button_clicked)
        style = powersave_button.get_style_context()
        style.add_class("powersave")
        powersave_button.set_hexpand(True)
        powersave_button.set_vexpand(True)
        
        performance_button = Gtk.Button("Performance")
        performance_button.connect("clicked", self.on_performance_button_clicked)
        style = performance_button.get_style_context()
        style.add_class("performance")
        performance_button.set_hexpand(True)
        performance_button.set_vexpand(True)

        if option == "nor":
            self.set_button_style(automatic_button, "#4f586e")
        elif option == "powersave":
            self.set_button_style(powersave_button, "#4f586e")
        elif option == "performance":
            self.set_button_style(performance_button, "#4f586e")

        hbox.pack_start(automatic_button, True, True, 0)
        hbox.pack_start(powersave_button, True, True, 0)
        hbox.pack_start(performance_button, True, True, 0)
        
        content_area = self.get_content_area()
        # background_color = Gdk.RGBA()
        # background_color.parse("#a3be8c")
        # content_area.override_background_color(Gtk.StateType.NORMAL, background_color)        
        
        content_area.add(hbox)
        self.show_all()

    def get_mouse_position(self):
        try:
            d = display.Display()
            s = d.screen()
            root = s.root
            root.change_attributes(event_mask=0x10000)
            pointer = root.query_pointer()
            x, y = pointer.root_x, pointer.root_y
            return x, y
        except Exception:
            return None, None

    def read_option_from_file(self):
        try:
            with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor", "r") as file:
                option = file.read().strip()
                return option
        except FileNotFoundError:
            return ""
        
    def set_button_style(self, button, color):
        css = f"button {{ background-color: {color}; }}"
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css.encode())
        context = button.get_style_context()
        context.add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def on_automatic_button_clicked(self, button):
        subprocess.call(["sudo auto-cpufreq --force=reset"], shell=True)
        self.exit_remove_pid()        

    def on_powersave_button_clicked(self, button):
        subprocess.call(["sudo auto-cpufreq --force=powersave"], shell=True)
        self.exit_remove_pid()

    def on_performance_button_clicked(self, button):
        subprocess.call(["sudo auto-cpufreq --force=performance"], shell=True)
        subprocess.call(["notify-send -a $current_time -u low -t 3000 'Search option added' 'Option: <span foreground='#a3be8c' size='medium'>$WebName</span>'"], shell=True)
        self.exit_remove_pid()

    def on_focus_out(self, widget, event):
        self.exit_remove_pid()

    def exit_remove_pid(self):
        pid = None
        try:
            with open(self.pid_file, "r") as file:
                pid = int(file.read().strip())
            try:
                os.remove(self.pid_file)
                os.kill(pid, 15)
            except ProcessLookupError:
                pass
        finally:
            exit(0)

pid_file = "/home/jonalm/scripts/qtile/bar_menus/power_managment_pid_file.pid"
dialog = None

try:
    if os.path.isfile(pid_file):
        with open(pid_file, "r") as file:
            pid = int(file.read().strip())
        try:
            os.remove(pid_file)
            os.kill(pid, 15)            
        except ProcessLookupError:
            pass
    else:
        with open(pid_file, "w") as file:
            file.write(str(os.getpid()))
        dialog = CustomDialog()    
        Gtk.main()
except Exception as e:
    print(f"An error occurred: {e}")
