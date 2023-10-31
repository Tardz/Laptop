import gi
gi.require_version('Gtk', '3.0')
import subprocess
import os
from Xlib import display 
from gi.repository import Gtk, Gdk, GLib

class cpu_stats_menu(Gtk.Dialog):
    def __init__(self):
        self.pid_file = "/home/jonalm/scripts/qtile/bar_menus/power_managment_pid_file.pid"
        Gtk.Dialog.__init__(self, "Custom Dialog", None, 0)
        self.set_default_size(400, 60)

        x, y = self.get_mouse_position()

        if x and y:
            self.move(x - 190, y - 50)

        self.connect("focus-out-event", self.on_focus_out)
        self.connect("key-press-event", self.on_escape_press)

        self.content_area = self.get_content_area()

        self.css()
        self.stats()

        self.content_area.pack_start(self.stats_main_box, True, True, 0)
        self.content_area.set_name("root")
        self.set_name("root")
        
        self.show_all()

    def stats(self):
        self.stats_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.stats_main_box.set_name("root")

        cpu_tmp_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        cpu_tmp_box.set_name("main-box")

        cpu_tmp_icon_box = Gtk.EventBox()
        cpu_tmp_icon_box.set_name("box-icon")

        cpu_tmp_icon = Gtk.Label()
        cpu_tmp_icon.set_text("")
        cpu_tmp_icon.set_name("icon")
        cpu_tmp_icon.set_halign(Gtk.Align.START)

        cpu_tmp_info = Gtk.Label()
        cpu_tmp_info.get_style_context().add_class("box-title")
        cpu_tmp_info.set_text("Info")
        cpu_tmp_info.set_name("box-info")
        cpu_tmp_info.set_halign(Gtk.Align.START)

        cpu_tmp_icon_box.add(cpu_tmp_icon)

        cpu_tmp_box.pack_start(cpu_tmp_icon_box, False, False, 0)
        cpu_tmp_box.pack_start(cpu_tmp_info, False, False, 0)

        self.stats_main_box.pack_start(cpu_tmp_box, False, False, 0)
    
    def css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        provider.load_from_path("/home/jonalm/scripts/qtile/bar_menus/cpu_stats_menu_styles.css")
        visual = screen.get_rgba_visual()
        self.content_area.set_visual(visual)
        self.set_visual(visual)

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

    def on_focus_out(self, widget, event):
        self.exit_remove_pid()

    def on_escape_press(self, widget, event):
        keyval = event.keyval
        if keyval == Gdk.KEY_Escape or keyval == Gdk.KEY_Escape_L:
            self.on_focus_out(widget, event)

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

pid_file = "/home/jonalm/scripts/qtile/bar_menus/cpu_stats_pid_file.pid"
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
        dialog = cpu_stats_menu()    
        Gtk.main()
except Exception as e:
    print(f"An error occurred: {e}")
