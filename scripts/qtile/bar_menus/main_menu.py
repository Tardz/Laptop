import gi
gi.require_version('Gtk', '3.0')
import subprocess
import os
from Xlib import display 
from gi.repository import Gtk, Gdk, Gio, GObject
import time

class SoundControlDialog(Gtk.Dialog):
    def __init__(self):
        self.pid_file = "/home/jonalm/scripts/qtile/bar_menus/power_managment_pid_file.pid"
        Gtk.Dialog.__init__(self, "Sound Control", None, 0)
        self.set_default_size(400, 50)
        self.move(7, 4)

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
        content_area.set_margin_top(10)
        content_area.set_margin_bottom(10)
        content_area.set_margin_start(10)
        content_area.set_margin_end(10)        
        self.set_name("content-area")
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
        self.top_box.pack_start(self.rofi_box, False, False, 0)
    
    def toggles(self):
        self.toggle_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.toggle_box.set_margin_top(10)
        self.toggle_box.set_margin_bottom(10)
        self.toggle_box.set_margin_start(10)
        self.toggle_box.set_margin_end(10)
        self.toggle_box.set_name("toggle-box")

        self.wifi_toggle()
        self.bluetooth_toggle()
        self.redshift_toggle()

    def wifi_toggle(self):
        wifi_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        wifi_main_box.set_margin_top(10)
        wifi_main_box.set_margin_bottom(10)
        wifi_main_box.set_margin_start(10)
        wifi_main_box.set_margin_end(10)

        wifi_right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        wifi_title = Gtk.Label()
        wifi_title.set_text("Wifi")
        wifi_title.set_name("toggle-title")
        wifi_title.set_halign(Gtk.Align.START)
        wifi_title.set_margin_bottom(5)
        wifi_title.set_margin_start(12)
        wifi_title.set_margin_top(4)


        self.wifi_timeout = GObject.timeout_add(3000, self.update_wifi_ssid)  # Update label every 5 seconds
        self.wifi_ssid = Gtk.Label()
        self.wifi_ssid.set_text(self.get_wifi_ssid())
        self.wifi_ssid.set_name("toggle-desc")
        self.wifi_ssid.set_halign(Gtk.Align.START)
        self.wifi_ssid.set_margin_start(12)

        wifi_left_box = Gtk.EventBox()

        self.wifi_icon = Gtk.Label()
        self.wifi_icon.set_text("")
        self.wifi_icon.set_halign(Gtk.Align.START)
        self.wifi_icon.set_margin_top(12)
        self.wifi_icon.set_margin_bottom(12)
        self.wifi_icon.set_margin_start(13)
        self.wifi_icon.set_margin_end(13)

        if self.get_wifi_on():
            wifi_left_box.set_name("toggle-box-enabled")
            self.wifi_icon.set_name("toggle-label-enabled")
        else:
            wifi_left_box.set_name("toggle-box-disabled")
            self.wifi_icon.set_name("toggle-label-disabled")

        wifi_right_box.add(wifi_title)
        wifi_right_box.add(self.wifi_ssid)
        wifi_left_box.add(self.wifi_icon)
        wifi_main_box.pack_start(wifi_left_box, False, False, 0)
        wifi_main_box.pack_start(wifi_right_box, False, False, 0)
        self.toggle_box.pack_start(wifi_main_box, False, False, 0)

        wifi_left_box.connect("button-press-event", self.wifi_clicked)

    def bluetooth_toggle(self):
        bluetooth_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        bluetooth_main_box.set_margin_top(10)
        bluetooth_main_box.set_margin_bottom(10)
        bluetooth_main_box.set_margin_start(10)
        bluetooth_main_box.set_margin_end(10)

        bluetooth_right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        bluetooth_title = Gtk.Label()
        bluetooth_title.set_text("Bluetooth")
        bluetooth_title.set_name("toggle-title")
        bluetooth_title.set_halign(Gtk.Align.START)
        bluetooth_title.set_margin_bottom(5)
        bluetooth_title.set_margin_start(12)
        bluetooth_title.set_margin_top(4)

        # process = subprocess.Popen(['python3', '/home/jonalm/scripts/qtile/get_wifi_ssid.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # stdout = process.communicate()
        # ssid = stdout[0].strip()

        self.bluetooth_timeout = GObject.timeout_add(3000, self.update_bluetooth_device)  # Update label every 5 seconds
        self.bluetooth_device = Gtk.Label()
        self.bluetooth_device.set_text("No device")
        self.bluetooth_device.set_name("toggle-desc")
        self.bluetooth_device.set_halign(Gtk.Align.START)
        self.bluetooth_device.set_margin_start(12)
    
        bluetooth_left_box = Gtk.EventBox()

        self.bluetooth_icon = Gtk.Label()
        self.bluetooth_icon.set_text("")
        self.bluetooth_icon.set_halign(Gtk.Align.START)
        self.bluetooth_icon.set_margin_top(12)
        self.bluetooth_icon.set_margin_bottom(12)
        self.bluetooth_icon.set_margin_start(15)
        self.bluetooth_icon.set_margin_end(15)

        if self.get_bluetooth_on():
            bluetooth_left_box.set_name("toggle-box-enabled")
            self.bluetooth_icon.set_name("toggle-label-enabled")
        else:
            bluetooth_left_box.set_name("toggle-box-disabled")
            self.bluetooth_icon.set_name("toggle-label-disabled")

        bluetooth_right_box.add(bluetooth_title)
        bluetooth_right_box.add(self.bluetooth_device)
        bluetooth_left_box.add(self.bluetooth_icon)
        bluetooth_main_box.pack_start(bluetooth_left_box, False, False, 0)
        bluetooth_main_box.pack_start(bluetooth_right_box, False, False, 0)
        self.toggle_box.pack_start(bluetooth_main_box, False, False, 0)

        bluetooth_left_box.connect("button-press-event", self.bluetooth_clicked)

    def redshift_toggle(self):
        redshift_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        redshift_main_box.set_margin_top(10)
        redshift_main_box.set_margin_bottom(10)
        redshift_main_box.set_margin_start(10)
        redshift_main_box.set_margin_end(10)

        redshift_right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        redshift_title = Gtk.Label()
        redshift_title.set_text("Redshift")
        redshift_title.set_name("toggle-title")
        redshift_title.set_halign(Gtk.Align.START)
        redshift_title.set_margin_bottom(5)
        redshift_title.set_margin_start(12)
        redshift_title.set_margin_top(4)

        self.redshift_desc = Gtk.Label()
        if self.get_redshift_on():
            self.redshift_desc.set_text("On")
        else:
            self.redshift_desc.set_text("Off")
        self.redshift_desc.set_name("toggle-desc")
        self.redshift_desc.set_halign(Gtk.Align.START)
        self.redshift_desc.set_margin_start(12)

        redshift_left_box = Gtk.EventBox()

        self.redshift_icon = Gtk.Label()
        self.redshift_icon.set_text("")
        self.redshift_icon.set_halign(Gtk.Align.START)
        self.redshift_icon.set_margin_top(12)
        self.redshift_icon.set_margin_bottom(12)
        self.redshift_icon.set_margin_start(19)
        self.redshift_icon.set_margin_end(19)

        if self.get_redshift_on():
            redshift_left_box.set_name("toggle-box-enabled")
            self.redshift_icon.set_name("toggle-label-enabled")
        else:
            redshift_left_box.set_name("toggle-box-disabled")
            self.redshift_icon.set_name("toggle-label-disabled")

        redshift_left_box.add(self.redshift_icon)
        redshift_right_box.add(redshift_title)
        redshift_right_box.add(self.redshift_desc)
        redshift_main_box.pack_start(redshift_left_box, False, False, 0)
        redshift_main_box.pack_start(redshift_right_box, False, False, 0)
        self.toggle_box.pack_start(redshift_main_box, False, False, 0)
        
        redshift_left_box.connect("button-press-event", self.redshift_clicked)
    
    def rofi(self):
        self.rofi_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        self.rofi_box.set_margin_top(10)
        self.rofi_box.set_margin_bottom(10)
        self.rofi_box.set_margin_start(10)
        self.rofi_box.set_margin_end(10)

        
        rofi_left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)

        app_launcher_box = Gtk.EventBox()
        app_launcher_icon = Gtk.Label()
        app_launcher_icon.set_text("")
        app_launcher_icon.set_name("rofi-icons")
        app_launcher_icon.set_halign(Gtk.Align.START)
        app_launcher_icon.set_margin_top(26)
        app_launcher_icon.set_margin_bottom(26)
        app_launcher_icon.set_margin_start(36)
        app_launcher_icon.set_margin_end(36)
        app_launcher_box.add(app_launcher_icon)
        app_launcher_box.set_name("rofi-icons")

        search_box = Gtk.EventBox()
        search_icon = Gtk.Label()
        search_icon.set_text("")
        search_icon.set_name("rofi-icons")
        search_icon.set_halign(Gtk.Align.START)
        search_icon.set_margin_top(26)
        search_icon.set_margin_bottom(26)
        search_icon.set_margin_start(36)
        search_icon.set_margin_end(36)
        search_box.add(search_icon)
        search_box.set_name("rofi-icons")

        config_box = Gtk.EventBox()
        config_icon = Gtk.Label()
        config_icon.set_text("")
        config_icon.set_name("rofi-icons")
        config_icon.set_halign(Gtk.Align.START)
        config_icon.set_margin_top(26)
        config_icon.set_margin_bottom(26)
        config_icon.set_margin_start(36)
        config_icon.set_margin_end(36)
        config_box.add(config_icon)
        config_box.set_name("rofi-icons")

        rofi_right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
      
        power_menu_box = Gtk.EventBox()
        power_menu_icon = Gtk.Label()
        power_menu_icon.set_text("")
        power_menu_icon.set_name("rofi-icons")
        power_menu_icon.set_halign(Gtk.Align.START)
        power_menu_icon.set_margin_top(26)
        power_menu_icon.set_margin_bottom(26)
        power_menu_icon.set_margin_start(36)
        power_menu_icon.set_margin_end(36)
        power_menu_box.add(power_menu_icon)
        power_menu_box.set_name("rofi-icons")

        automation_box = Gtk.EventBox()
        automation_icon = Gtk.Label()
        automation_icon.set_text("")
        automation_icon.set_name("rofi-icons")
        automation_icon.set_halign(Gtk.Align.START)
        automation_icon.set_margin_top(26)
        automation_icon.set_margin_bottom(26)
        automation_icon.set_margin_start(36)
        automation_icon.set_margin_end(36)
        automation_box.add(automation_icon)
        automation_box.set_name("rofi-icons")

        keyboard_shortcuts_box = Gtk.EventBox()
        keyboard_shortcuts_icon = Gtk.Label()
        keyboard_shortcuts_icon.set_text("")
        keyboard_shortcuts_icon.set_name("rofi-icons")
        keyboard_shortcuts_icon.set_halign(Gtk.Align.START)
        keyboard_shortcuts_icon.set_margin_top(26)
        keyboard_shortcuts_icon.set_margin_bottom(26)
        keyboard_shortcuts_icon.set_margin_start(36)
        keyboard_shortcuts_icon.set_margin_end(36)
        keyboard_shortcuts_box.add(keyboard_shortcuts_icon)
        keyboard_shortcuts_box.set_name("rofi-icons")

        rofi_left_box.pack_start(app_launcher_box, False, False, 0)
        rofi_left_box.pack_start(search_box, False, False, 0)
        rofi_left_box.pack_start(config_box, False, False, 0)
        rofi_right_box.pack_start(power_menu_box, False, False, 0)
        rofi_right_box.pack_start(automation_box, False, False, 0)
        rofi_right_box.pack_start(keyboard_shortcuts_box, False, False, 0)
        self.rofi_box.pack_start(rofi_left_box, False, False, 0)
        self.rofi_box.pack_start(rofi_right_box, False, False, 0)

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

        #slider-box {
            border-radius: 5px;
            background: #4f586e;
        }

        #toggle-box {
            border-radius: 5px;
            background: #4f586e;
        }

        #toggle-label-enabled {
            color: black;
            font-size: 20;
            font-family: 'Font Awesome 6 Free Solid';
        }

        #toggle-label-disabled {
            color: white;
            font-size: 20;
            font-family: 'Font Awesome 6 Free Solid';
        }

        #toggle-box-enabled {
            border-radius: 5px;
            background: #81a1c1;
        }
        
        #toggle-box-disabled {
            border-radius: 5px;
            background: #2e3440;
        }

        #toggle-title {
            color: white;
            font-size: 19;
            font-family: FiraCode Nerd Font;
            font-weight: bold;
        }
        
        #toggle-desc {
            color: white;
            font-size: 19;
            font-family: FiraCode Nerd Font;
        }

        #toggle-bluetooth-label {
            color: white;
            font-size: 24;
            font-family: 'Font Awesome 6 Free Solid';
            font-weight: bold;
        }

        #rofi-icons {
            border-radius: 5px;
            background: #4f586e;
            color: black;
            font-size: 26;
            font-family: 'Font Awesome 6 Free Solid';
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
    
    def get_wifi_ssid(self):
        process = subprocess.Popen(['python3', '/home/jonalm/scripts/qtile/get_wifi_ssid.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout = process.communicate()
        ssid = stdout[0].strip()
        print(ssid)
        if ssid == "lo":
            return "Disconnected"
        else:
            return ssid
        
    def update_wifi_ssid(self):
        self.wifi_ssid.set_text(self.get_wifi_ssid())
        return True
    
    def get_bluetooth_device(self):
        pass

    def update_bluetooth_device(self):
        pass

    def on_response(self, dialog, response_id):
        if response_id == Gtk.ResponseType.OK:
            volume = dialog.volume_adjustment.get_value()
            print(f"Volume changed to {volume}%")
        dialog.destroy()
    
    def get_wifi_on(self):
        wifi_state = subprocess.check_output(["nmcli",  "radio", "wifi"]).strip().decode("utf-8")
        if wifi_state == "enabled":
            return True
        elif wifi_state == "disabled":
            return False
    
    def wifi_clicked(self, widget, event):
        if self.get_wifi_on():
            subprocess.run(["nmcli",  "radio", "wifi", "off"])
            widget.set_name("toggle-box-disabled")
            self.wifi_icon.set_name("toggle-label-disabled")
            self.wifi_ssid.set_text("Off")
        else:
            subprocess.run(["nmcli",  "radio", "wifi", "on"])
            widget.set_name("toggle-box-enabled")
            self.wifi_icon.set_name("toggle-label-enabled")
        
    def get_bluetooth_on(self):
        try:
            bluetooth_state = subprocess.check_output("systemctl status bluetooth | grep Running", shell=True, stderr=subprocess.PIPE, text=True).strip()
            if not bluetooth_state:
                return False
            else:
                return True
        except subprocess.CalledProcessError:
            print("Error: Unable to determine Bluetooth state")

    def bluetooth_clicked(self, widget, event):
        if self.get_bluetooth_on():
            subprocess.run(["sudo", "systemctl",  "stop", "bluetooth"])
            widget.set_name("toggle-box-disabled")
            self.bluetooth_icon.set_name("toggle-label-disabled")
            self.bluetooth_device.set_text("Off")
        else:
            subprocess.run(["sudo", "systemctl",  "start", "bluetooth"])
            widget.set_name("toggle-box-enabled")
            self.bluetooth_icon.set_name("toggle-label-enabled")
            self.bluetooth_device.set_text("No device")

    def get_redshift_on(self):
        try:
            redshift_state = subprocess.check_output("xrandr --verbose | grep Gamma", shell=True, stderr=subprocess.PIPE, text=True).strip()
            start_index = redshift_state.find("Gamma: ")
            gamma_values = None
            if start_index != -1:
                gamma_values = redshift_state[start_index + len("Gamma: "):].strip()
            if gamma_values == "1.0:1.1:1.1":
                return False
            else:
                return True
        except subprocess.CalledProcessError:
            print("Error: Unable to determine Bluetooth state")

    def redshift_clicked(self, widget, event):
        if self.get_redshift_on() == True:
            subprocess.run("redshift -P -O 5700", shell=True)
            widget.set_name("toggle-box-disabled")
            self.redshift_icon.set_name("toggle-label-disabled")
            self.redshift_desc.set_text("Off")
        else:
            subprocess.run("redshift -P -O 4500", shell=True)
            widget.set_name("toggle-box-enabled")
            self.redshift_icon.set_name("toggle-label-enabled")
            self.redshift_desc.set_text("On")

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

