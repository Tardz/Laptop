import gi
gi.require_version('Gtk', '3.0')
import subprocess
import os
from gi.repository import Gtk, Gdk, GObject

class cpu_stats_menu(Gtk.Dialog):
    def __init__(self):
        self.pid_file = "/home/jonalm/scripts/qtile/bar_menus/cpu/cpu_stats_pid_file.pid"
        Gtk.Dialog.__init__(self, "Custom Dialog", None, 0)
        self.set_default_size(200, 60)

        x, y = self.get_mouse_position()
        self.move(x, y)

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
        self.stats_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.stats_main_box.set_name("main-box")

        self.tmp()
        self.freq()

        self.stats_main_box.pack_start(self.tmp_background_box, False, False, 0)
        self.stats_main_box.pack_start(self.freq_background_box, False, False, 0)

    def tmp(self):
        self.tmp_background_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.tmp_background_box.set_name("sub-box")
        self.tmp_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.tmp_main_box.set_name("sub-box")

        tmp_right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        tmp_timeout = GObject.timeout_add(3000, self.update_tmp)  # Update label every 5 seconds
        tmp_title = Gtk.Label()
        tmp_title.set_text("Temperature")
        tmp_title.set_name("box-title")
        tmp_title.set_halign(Gtk.Align.START)

        self.tmp_info = Gtk.Label()
        self.tmp_info.set_text(self.get_tmp())
        self.tmp_info.set_name("box-info")
        self.tmp_info.set_halign(Gtk.Align.START)

        tmp_left_box = Gtk.EventBox()
        tmp_left_box.set_name("box-icon")

        tmp_icon = Gtk.Label()
        tmp_icon.set_name("tmp-icon")
        tmp_icon.set_text("")
        tmp_icon.set_halign(Gtk.Align.START)

        tmp_left_box.add(tmp_icon)
        tmp_right_box.add(tmp_title)
        tmp_right_box.add(self.tmp_info)
        
        self.tmp_main_box.pack_start(tmp_left_box, False, False, 0)
        self.tmp_main_box.pack_start(tmp_right_box, False, False, 0)
        self.tmp_background_box.pack_start(self.tmp_main_box, False, False, 0)

    def freq(self):
        self.freq_background_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.freq_background_box.set_name("sub-box")
        self.freq_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.freq_main_box.set_name("sub-box")

        freq_right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        GObject.timeout_add(3000, self.update_freq)
        freq_title = Gtk.Label()
        freq_title.set_text("Frequency")
        freq_title.set_name("box-title")
        freq_title.set_halign(Gtk.Align.START)

        self.freq_info = Gtk.Label()
        self.freq_info.set_text(self.get_freq())
        self.freq_info.set_name("box-info")
        self.freq_info.set_halign(Gtk.Align.START)

        freq_left_box = Gtk.EventBox()
        freq_left_box.set_name("box-icon")

        freq_icon = Gtk.Label()
        freq_icon.set_name("freq-icon")
        freq_icon.set_text("")
        freq_icon.set_halign(Gtk.Align.START)

        freq_left_box.add(freq_icon)
        freq_right_box.add(freq_title)
        freq_right_box.add(self.freq_info)

        self.freq_main_box.pack_start(freq_left_box, False, False, 0)
        self.freq_main_box.pack_start(freq_right_box, False, False, 0)
        self.freq_background_box.pack_start(self.freq_main_box, False, False, 0)

    def css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        provider.load_from_path("/home/jonalm/scripts/qtile/bar_menus/cpu/cpu_stats_menu_styles.css")
        visual = screen.get_rgba_visual()
        self.content_area.set_visual(visual)
        self.set_visual(visual)

    def get_tmp(self):
        cpu_avg_tmp = subprocess.check_output("sensors | grep temp1 | awk '{print $2}'", shell=True, stderr=subprocess.PIPE, text=True).strip()
        return cpu_avg_tmp

    def update_tmp(self):
        self.tmp_info.set_text(self.get_tmp())
        return True

    def get_freq(self):
        cpu_avg_freq = subprocess.check_output("cpupower frequency-info | grep 'current CPU frequency' | grep 'kernel' | awk '{print $4}'", shell=True, stderr=subprocess.PIPE, text=True).strip()
        if "." in cpu_avg_freq:
            return cpu_avg_freq + " GHz"
        else:
            return cpu_avg_freq + " Hz"

    def update_freq(self):
        self.freq_info.set_text(self.get_freq())
        return True

    def get_mouse_position(self):
        from Xlib import display 
        from Xlib.ext import randr
        try:
            d = display.Display()
            s = d.screen()
            root = s.root
            root.change_attributes(event_mask=0x10000)
            pointer = root.query_pointer()
            x = pointer.root_x - 160

            res = randr.get_screen_resources(s.root)
            screen_number = 0
            for output in res.outputs:
                params = randr.get_output_info(s.root, output, res.config_timestamp)
                data = params._data
                if data["connection"] == 0:
                    screen_number += 1

            if screen_number > 1:
                return x, 172
            else:
                return x, 5
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

pid_file = "/home/jonalm/scripts/qtile/bar_menus/cpu/cpu_stats_pid_file.pid"
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
