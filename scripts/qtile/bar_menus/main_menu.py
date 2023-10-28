import gi
gi.require_version('Gtk', '3.0')
import subprocess
import os
from Xlib import display 
from gi.repository import Gtk, Gdk, Gio

class SoundControlDialog(Gtk.Dialog):
    def __init__(self):
        self.pid_file = "/home/jonalm/scripts/qtile/bar_menus/power_managment_pid_file.pid"
        Gtk.Dialog.__init__(self, "Sound Control", None, 0)
        self.set_default_size(400, 50)
        self.move(10, 5)

        self.get_input_data()
        self.css()
        self.volume()
        self.display_brightness()
        self.keyboard_brightness()
        self.top()
        self.get_input_data()

        self.connect("focus-out-event", self.on_focus_out)
        self.connect("response", self.on_response)

        content_area = self.get_content_area()
        content_area.set_name("content-area")

        content_area.pack_start(self.top_box, True, True, 0)
        content_area.pack_start(self.volume_box, True, True, 0)
        content_area.pack_start(self.display_box, True, True, 0)
        content_area.pack_start(self.keyboard_box, True, True, 0)

        self.show_all()

    def top(self):
        self.top_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.toggles()
        self.rofi()
        
        self.top_box.pack_start(self.toggle_box, False, False, 0)
    
    def toggles(self):
        self.toggle_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.wifi_toggle()
        self.bluetooth_toggle()

    def wifi_toggle(self):
        wifi_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        wifi_box.set_name("toggle-box")
        wifi_box.set_margin_top(10)
        wifi_box.set_margin_bottom(10)
        wifi_box.set_margin_start(10)
        wifi_box.set_margin_end(10)

        wifi_label = Gtk.Label()
        wifi_label.set_text("")
        wifi_label.set_name("toggle-wifi-label")
        wifi_label.set_halign(Gtk.Align.START)
        wifi_label.set_margin_top(16)
        wifi_label.set_margin_bottom(16)
        wifi_label.set_margin_start(16)
        wifi_label.set_margin_end(16)

        wifi_box.pack_start(wifi_label, False, False, 0)
        self.toggle_box.pack_start(wifi_box, False, False, 0)
    
    def bluetooth_toggle(self):
        bluetooth_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        bluetooth_box.set_name("toggle-box")
        bluetooth_box.set_margin_top(10)
        bluetooth_box.set_margin_bottom(10)
        bluetooth_box.set_margin_start(10)
        bluetooth_box.set_margin_end(10)

        bluetooth_label = Gtk.Label()
        bluetooth_label.set_text("")
        bluetooth_label.set_name("toggle-bluetooth-label")
        bluetooth_label.set_halign(Gtk.Align.START)
        bluetooth_label.set_margin_top(16)
        bluetooth_label.set_margin_bottom(12)
        bluetooth_label.set_margin_start(16)
        bluetooth_label.set_margin_end(16)

        bluetooth_box.pack_start(bluetooth_label, False, False, 0)

        self.toggle_box.pack_start(bluetooth_box, False, False, 0)
    
    def rofi(self):
        self.rofi_left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.rofi_right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

    def volume(self):
        self.volume_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.volume_box.set_name("slider-box")
        self.volume_box.set_margin_top(10)
        self.volume_box.set_margin_bottom(10)
        self.volume_box.set_margin_start(10)
        self.volume_box.set_margin_end(10)

        volume_label = Gtk.Label()
        volume_label.set_text("Volume")
        volume_label.set_name("label")
        volume_label.set_halign(Gtk.Align.START)
        volume_label.set_margin_top(10)
        volume_label.set_margin_bottom(5)
        volume_label.set_margin_start(14)
        self.volume_box.pack_start(volume_label, False, False, 0)
        
        volume_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        volume_icon = Gtk.Label("")
        volume_icon.set_name("volume-icon")
        volume_icon.set_margin_start(18)
        volume_icon.set_margin_end(0)
        volume_hbox.pack_start(volume_icon, False, False, 0)

        volume_adjustment = Gtk.Adjustment(value=self.current_volume, lower=0, upper=100, step_increment=1, page_increment=10)
        volume_scale = Gtk.HScale.new(volume_adjustment)

        volume_scale.set_digits(0)
        volume_scale.set_margin_end(10)
        volume_scale.set_draw_value(False)
        volume_hbox.pack_start(volume_scale, True, True, 0)

        self.volume_box.pack_start(volume_hbox, False, False, 0)

        volume_scale.connect("value-changed", self.on_volume_changed)

    def display_brightness(self):
        self.display_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.display_box.set_name("slider-box")
        self.display_box.set_margin_top(10)
        self.display_box.set_margin_bottom(10)
        self.display_box.set_margin_start(10)
        self.display_box.set_margin_end(10)

        display_label = Gtk.Label()
        display_label.set_text("Display")
        display_label.set_name("label")
        display_label.set_halign(Gtk.Align.START)
        display_label.set_margin_top(10)
        display_label.set_margin_bottom(5)
        display_label.set_margin_start(14)
        self.display_box.pack_start(display_label, False, False, 0)
        
        display_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        display_icon = Gtk.Label("")
        display_icon.set_name("icons")
        display_icon.set_margin_start(15)
        display_icon.set_margin_end(4)
        display_hbox.pack_start(display_icon, False, False, 0)

        display_adjustment = Gtk.Adjustment(value=self.current_display_brightness, lower=0, upper=100, step_increment=1, page_increment=10)
        display_scale = Gtk.HScale.new(display_adjustment)

        display_scale.set_digits(0)
        display_scale.set_margin_end(10)
        display_scale.set_draw_value(False)
        display_hbox.pack_start(display_scale, True, True, 0)

        self.display_box.pack_start(display_hbox, False, False, 0)
        
        display_scale.connect("value-changed", self.on_display_changed)
    
    def keyboard_brightness(self):
        self.keyboard_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.keyboard_box.set_name("slider-box")
        self.keyboard_box.set_margin_top(10)
        self.keyboard_box.set_margin_bottom(10)
        self.keyboard_box.set_margin_start(10)
        self.keyboard_box.set_margin_end(10)

        keyboard_label = Gtk.Label()
        keyboard_label.set_text("Keyboard")
        keyboard_label.set_name("label")
        keyboard_label.set_halign(Gtk.Align.START)
        keyboard_label.set_margin_top(10)
        keyboard_label.set_margin_bottom(5)
        keyboard_label.set_margin_start(14)
        self.keyboard_box.pack_start(keyboard_label, False, False, 0)
        
        keyboard_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        keyboard_icon = Gtk.Label("")
        keyboard_icon.set_name("icons")
        keyboard_icon.set_margin_start(15)
        keyboard_icon.set_margin_end(14)
        keyboard_hbox.pack_start(keyboard_icon, False, False, 0)

        keyboard_adjustment = Gtk.Adjustment(value=self.current_keyboard_brightness, lower=0, upper=4, step_increment=1, page_increment=1)
        keyboard_scale = Gtk.HScale.new(keyboard_adjustment)

        keyboard_scale.set_digits(0)
        keyboard_scale.set_margin_end(10)
        keyboard_scale.set_draw_value(False)
        keyboard_hbox.pack_start(keyboard_scale, True, True, 0)

        self.keyboard_box.pack_start(keyboard_hbox, False, False, 0)
        
        keyboard_scale.connect("value-changed", self.on_keyboard_changed)

    def css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        css = b"""
        #content-area {
            border-color: red;
            background: #2e3440;
        }

        #toggle-box {
            border-radius: 5px;
            background: #4f586e;
        }

        #slider-box {
            border-radius: 5px;
            background: #4f586e;
        }

        #toggle-wifi-label {
            color: white;
            font-size: 20;
            font-family: 'Font Awesome 6 Free Solid';
            font-weight: bold;
        }
        
        #toggle-bluetooth-label {
            color: white;
            font-size: 24;
            font-family: 'Font Awesome 6 Free Solid';
            font-weight: bold;
        }

        #icons {
            color: white;
            font-size: 24;
            font-family: 'Font Awesome 6 Free Solid';
            font-weight: bold;
        }

        #volume-icon {
            color: white;
            font-size: 22;
            font-family: 'Font Awesome 6 Free Solid';
            font-weight: bold;
        }

        #label {
            color: white;
            font-size: 19;
            font-family: FiraCode Nerd Font;
            font-weight: bold;
        }

        scale trough {
            border-radius: 6;
            min-width: 10px;                                                                               
            min-height: 18px;          
        }   
        
        scale trough highlight {
            background: white;
            border-radius: 6;
            min-width: 10px;                                                                               
            min-height: 18px;          
        }   

        scale trough slider {
            background: #d9dedf;
            border-radius: 6;
            min-width: 18px;                                                                               
            min-height: 19px;          
        }   
        """
        provider.load_from_data(css)

    def get_input_data(self):
        self.current_volume = subprocess.check_output("pactl get-sink-volume @DEFAULT_SINK@ | awk -F'/' '{print $2}' | awk -F'%' '{print $1}'", shell=True, text=True).strip()
        self.current_volume = float(self.current_volume)    

        self.current_display_brightness = subprocess.check_output("brillo", shell=True, text=True).strip()
        self.current_display_brightness = float(self.current_display_brightness)

        self.current_keyboard_brightness = subprocess.check_output("brightnessctl --device='asus::kbd_backlight' get", shell=True, text=True).strip()
        self.current_keyboard_brightness = float(self.current_keyboard_brightness)

    def on_response(self, dialog, response_id):
        if response_id == Gtk.ResponseType.OK:
            volume = dialog.volume_adjustment.get_value()
            print(f"Volume changed to {volume}%")
        dialog.destroy()

    def on_volume_changed(self, scale):
        volume = int(scale.get_value())
        subprocess.run([f"pactl set-sink-volume @DEFAULT_SINK@ {volume}%"], shell=True, check=False)

    def on_display_changed(self, scale):
        display_brightness = int(scale.get_value())
        subprocess.run([f"brillo -S {display_brightness}%"], shell=True, check=False)

    def on_keyboard_changed(self, scale):
        keyboard_brightness = int(scale.get_value())
        subprocess.run([f"brightnessctl --device='asus::kbd_backlight' set {keyboard_brightness}"], shell=True, check=False)
   
    def on_focus_out(self, widget, event):
        self.exit_remove_pid()

    def exit_remove_pid(self):
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
        dialog = SoundControlDialog()
        Gtk.main()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    exit(0)

