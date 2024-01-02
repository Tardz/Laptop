import gi
gi.require_version('Gtk', '3.0')
import subprocess
import os
import asyncio
from Xlib import display 
from gi.repository import Gtk, Gdk, Gio, GObject, GLib
from dbus.mainloop.glib import DBusGMainLoop

class MainMenu(Gtk.Dialog):
    def __init__(self):
        self.pid_file = "/home/jonalm/scripts/qtile/bar_menus/main/main_pid_file.pid"
        Gtk.Dialog.__init__(self, "Sound Control", None, 0)
        self.set_default_size(100, 50)
        self.move(9, 4)

        self.ignore_focus_lost = False
        self.previous_css_class = None
        self.wifi_list_active = False
        self.first_wifi_scan = True

        self.content_area = self.get_content_area()
        self.content_area.set_size_request(100, 50)
        self.content_area.set_name("content-area")
        self.set_name("root")

        fixed = Gtk.Fixed()
        self.get_content_area().add(fixed)

        self.get_slider_data()
        self.css()
        self.bottom()
        self.top()

        self.connect("focus-out-event", self.on_focus_out)
        self.connect("key-press-event", self.on_escape_press)
        self.connect("response", self.on_response)

        self.content_area.pack_start(self.top_box, False, False, 0)
        self.content_area.pack_start(self.bottom_box, False, False, 0)

        self.show_all()
        self.top_box.pack_start(self.wifi_list_box, False, False, 0)
        
        # self.animate_opening(fixed)

    def animate_opening(self, container):
        container.set_opacity(0.0)
        self.show_all()

        def animation_tick():
            opacity = container.get_opacity()
            opacity += 0.05 
            if opacity >= 1.0:
                container.set_opacity(1.0)
                return False 
            container.set_opacity(opacity)
            return True

        GObject.timeout_add(5000, animation_tick)

    def top(self):
        self.top_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.toggles()
        self.rofi()
        self.wifi_list()
        
        self.top_box.pack_start(self.toggle_box, True, True, 0)
        self.top_box.pack_start(self.rofi_box, True, True, 0)

    def bottom(self):
        self.bottom_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.volume()
        self.display_brightness()
        
        self.bottom_box.pack_start(self.volume_box, True, False, 0)
        self.bottom_box.pack_start(self.display_box, True, False, 0)
    
    def toggles(self):
        self.toggle_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.toggle_box.set_name("toggle-boxes")

        self.wifi_toggle()
        self.bluetooth_toggle()
        self.redshift_toggle()

    def wifi_toggle(self):
        wifi_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        wifi_main_box.set_name("toggle-box")

        wifi_right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        wifi_right_box.connect("button-press-event", self.show_wifi_list)
        wifi_right_box.set_name("toggle-right-box")
        wifi_right_box.connect("enter-notify-event", self.on_icon_hover)
        wifi_right_box.connect("leave-notify-event", self.on_icon_leave)

        wifi_title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        wifi_title = Gtk.Label()
        wifi_title.set_text("Wifi")
        wifi_title.set_name("toggle-title")
        wifi_title.set_halign(Gtk.Align.START)

        wifi_list_button = Gtk.EventBox()

        self.wifi_list_button_icon = Gtk.Label()
        self.wifi_list_button_icon.set_text("")
        self.wifi_list_button_icon.set_name("toggle-list-button-disabled")

        self.wifi_timeout = GObject.timeout_add(3000, self.update_wifi_ssid)  # Update label every 5 seconds
        self.wifi_ssid = Gtk.Label()
        self.wifi_ssid.set_text(self.get_wifi_ssid())
        self.wifi_ssid.set_name("toggle-desc")
        self.wifi_ssid.set_halign(Gtk.Align.START)

        wifi_left_box = Gtk.EventBox()

        self.wifi_icon = Gtk.Label()
        self.wifi_icon.set_text("")
        self.wifi_icon.set_halign(Gtk.Align.START)
        self.wifi_icon.set_margin_top(12)
        self.wifi_icon.set_margin_bottom(12)
        self.wifi_icon.set_margin_start(13)
        self.wifi_icon.set_margin_end(13)

        if self.get_wifi_on():
            wifi_left_box.set_name("toggle-left-box-enabled")
            self.wifi_icon.set_name("toggle-icon-enabled")
        else:
            wifi_left_box.set_name("toggle-left-box-disabled")
            self.wifi_icon.set_name("toggle-icon-disabled")

        wifi_list_button.add(self.wifi_list_button_icon)
        wifi_title_box.pack_start(wifi_title, False, False, 0)
        wifi_title_box.pack_start(wifi_list_button, False, False, 0)
        wifi_right_box.add(wifi_title_box)
        wifi_right_box.add(self.wifi_ssid)
        wifi_left_box.add(self.wifi_icon)
        wifi_main_box.pack_start(wifi_left_box, False, False, 0)
        wifi_main_box.pack_start(wifi_right_box, False, False, 0)
        self.toggle_box.pack_start(wifi_main_box, False, False, 0)

        wifi_left_box.connect("button-press-event", self.wifi_clicked)

    def bluetooth_toggle(self):
        self.bluetooth_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.bluetooth_main_box.set_name("toggle-box")

        bluetooth_right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        bluetooth_title = Gtk.Label()
        bluetooth_title.set_text("Bluetooth")
        bluetooth_title.set_name("toggle-title")
        bluetooth_title.set_halign(Gtk.Align.START)

        self.bluetooth_timeout = GObject.timeout_add(3000, self.update_bluetooth_device)  # Update label every 5 seconds
        self.bluetooth_device = Gtk.Label()
        self.bluetooth_device.set_text("No device")
        self.bluetooth_device.set_name("toggle-desc")
        self.bluetooth_device.set_halign(Gtk.Align.START)
    
        bluetooth_left_box = Gtk.EventBox()

        self.bluetooth_icon = Gtk.Label()
        self.bluetooth_icon.set_text("")
        self.bluetooth_icon.set_halign(Gtk.Align.START)
        self.bluetooth_icon.set_margin_top(12)
        self.bluetooth_icon.set_margin_bottom(12)
        self.bluetooth_icon.set_margin_start(15)
        self.bluetooth_icon.set_margin_end(15)

        if self.get_bluetooth_on():
            bluetooth_left_box.set_name("toggle-left-box-enabled")
            self.bluetooth_icon.set_name("toggle-icon-enabled")
        else:
            bluetooth_left_box.set_name("toggle-left-box-disabled")
            self.bluetooth_icon.set_name("toggle-icon-disabled")

        bluetooth_right_box.add(bluetooth_title)
        bluetooth_right_box.add(self.bluetooth_device)
        bluetooth_left_box.add(self.bluetooth_icon)
        self.bluetooth_main_box.pack_start(bluetooth_left_box, False, False, 0)
        self.bluetooth_main_box.pack_start(bluetooth_right_box, False, False, 0)
        self.toggle_box.pack_start(self.bluetooth_main_box, False, False, 0)

        bluetooth_left_box.connect("button-press-event", self.bluetooth_clicked)

    def redshift_toggle(self):
        self.redshift_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.redshift_main_box.set_name("toggle-box")

        redshift_right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        redshift_title = Gtk.Label()
        redshift_title.set_text("Redshift")
        redshift_title.set_name("toggle-title")
        redshift_title.set_halign(Gtk.Align.START)

        self.redshift_desc = Gtk.Label()
        if self.get_redshift_on():
            self.redshift_desc.set_text("On")
        else:
            self.redshift_desc.set_text("Off")
        self.redshift_desc.set_name("toggle-desc")
        self.redshift_desc.set_halign(Gtk.Align.START)

        redshift_left_box = Gtk.EventBox()

        self.redshift_icon = Gtk.Label()
        self.redshift_icon.set_text("")
        self.redshift_icon.set_halign(Gtk.Align.START)
        self.redshift_icon.set_margin_top(12)
        self.redshift_icon.set_margin_bottom(12)
        self.redshift_icon.set_margin_start(19)
        self.redshift_icon.set_margin_end(19)

        if self.get_redshift_on():
            redshift_left_box.set_name("toggle-left-box-enabled")
            self.redshift_icon.set_name("toggle-icon-enabled")
        else:
            redshift_left_box.set_name("toggle-left-box-disabled")
            self.redshift_icon.set_name("toggle-icon-disabled")

        redshift_left_box.add(self.redshift_icon)
        redshift_right_box.add(redshift_title)
        redshift_right_box.add(self.redshift_desc)
        self.redshift_main_box.pack_start(redshift_left_box, False, False, 0)
        self.redshift_main_box.pack_start(redshift_right_box, False, False, 0)
        self.toggle_box.pack_start(self.redshift_main_box, False, False, 0)
        
        redshift_left_box.connect("button-press-event", self.redshift_clicked)
    
    def rofi(self):
        self.rofi_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        self.rofi_box.set_name("rofi-box")

        rofi_left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)

        app_launcher_icon = Gtk.Label()
        app_launcher_icon.set_text("")
        app_launcher_icon.get_style_context().add_class("rofi-icon")
        app_launcher_icon.set_name("rofi-app-launcher-icon")
        app_launcher_icon.set_halign(Gtk.Align.START)
        app_launcher_box = Gtk.EventBox()
        app_launcher_box.set_name("rofi-icons")
        app_launcher_box.connect("enter-notify-event", self.on_icon_hover)
        app_launcher_box.connect("leave-notify-event", self.on_icon_leave)
        app_launcher_box.connect("button-press-event", self.app_launcher_clicked)
        app_launcher_box.add(app_launcher_icon)

        search_icon = Gtk.Label()
        search_icon.set_text("")
        search_icon.get_style_context().add_class("rofi-icon")
        search_icon.set_name("rofi-search-icon")
        search_icon.set_halign(Gtk.Align.START)
        search_box = Gtk.EventBox()
        search_box.set_name("rofi-icons")
        search_box.connect("enter-notify-event", self.on_icon_hover)
        search_box.connect("leave-notify-event", self.on_icon_leave)
        search_box.connect("button-press-event", self.search_clicked)
        search_box.add(search_icon)

        config_icon = Gtk.Label()
        config_icon.set_text("")
        config_icon.get_style_context().add_class("rofi-icon")
        config_icon.set_name("rofi-config-icon")
        config_icon.set_halign(Gtk.Align.START)
        config_box = Gtk.EventBox()
        config_box.set_name("rofi-icons")
        config_box.connect("enter-notify-event", self.on_icon_hover)
        config_box.connect("leave-notify-event", self.on_icon_leave)
        config_box.connect("button-press-event", self.config_clicked)
        config_box.add(config_icon)

        rofi_right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
      
        power_menu_icon = Gtk.Label()
        power_menu_icon.set_text("")
        power_menu_icon.get_style_context().add_class("rofi-icon")
        power_menu_icon.set_name("rofi-power-menu-icon")
        power_menu_icon.set_halign(Gtk.Align.START)
        power_menu_box = Gtk.EventBox()
        power_menu_box.set_name("rofi-icons")
        power_menu_box.connect("enter-notify-event", self.on_icon_hover)
        power_menu_box.connect("leave-notify-event", self.on_icon_leave)
        power_menu_box.connect("button-press-event", self.power_menu_clicked)
        power_menu_box.add(power_menu_icon)

        automation_icon = Gtk.Label()
        automation_icon.set_text("")
        automation_icon.get_style_context().add_class("rofi-icon")
        automation_icon.set_name("rofi-automation-icon")
        automation_icon.set_halign(Gtk.Align.START)
        automation_box = Gtk.EventBox()
        automation_box.set_name("rofi-icons")
        automation_box.connect("enter-notify-event", self.on_icon_hover)
        automation_box.connect("leave-notify-event", self.on_icon_leave)
        automation_box.connect("button-press-event", self.automation_clicked)
        automation_box.add(automation_icon)

        keyboard_shortcuts_icon = Gtk.Label()
        keyboard_shortcuts_icon.set_text("")
        keyboard_shortcuts_icon.get_style_context().add_class("rofi-icon")
        keyboard_shortcuts_icon.set_name("rofi-keyboard-shortcuts-icon")
        keyboard_shortcuts_icon.set_halign(Gtk.Align.START)
        keyboard_shortcuts_box = Gtk.EventBox()
        keyboard_shortcuts_box.set_name("rofi-icons")
        keyboard_shortcuts_box.connect("enter-notify-event", self.on_icon_hover)
        keyboard_shortcuts_box.connect("leave-notify-event", self.on_icon_leave)
        keyboard_shortcuts_box.connect("button-press-event", self.keyboard_shortcut_clicked)
        keyboard_shortcuts_box.add(keyboard_shortcuts_icon)

        rofi_left_box.pack_start(app_launcher_box, False, False, 0)
        rofi_left_box.pack_start(search_box, False, False, 0)
        rofi_left_box.pack_start(config_box, False, False, 0)

        rofi_right_box.pack_start(power_menu_box, False, False, 0)
        rofi_right_box.pack_start(automation_box, False, False, 0)
        rofi_right_box.pack_start(keyboard_shortcuts_box, False, False, 0)
        
        self.rofi_box.pack_start(rofi_left_box, False, False, 0)
        self.rofi_box.pack_start(rofi_right_box, False, False, 0)

    def wifi_list(self):
        self.wifi_list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        
        self.list_box = Gtk.ListBox()
        self.list_box.set_name("list")
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_name("list-box")
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC) 
        scrolled_window.add(self.list_box)  

        self.wifi_list_box.pack_start(scrolled_window, True, True, 0)

        self.fetch_networks()
        GLib.timeout_add(5000, self.fetch_networks)

    def volume(self):
        self.volume_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.volume_box.set_name("slider-box")

        volume_label = Gtk.Label()
        volume_label.set_text("Volume")
        volume_label.set_name("slider-title")
        volume_label.set_halign(Gtk.Align.START)
        self.volume_box.pack_start(volume_label, False, False, 0)
        
        volume_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        volume_adjustment = Gtk.Adjustment(value=self.current_volume, lower=0, upper=100, step_increment=1, page_increment=10)
        volume_scale = Gtk.HScale.new(volume_adjustment)
        volume_scale.set_digits(0)
        volume_scale.set_draw_value(False)

        volume_hbox.pack_start(volume_scale, True, True, 0)
        self.volume_box.pack_start(volume_hbox, False, False, 0)

        volume_scale.connect("value-changed", self.on_volume_changed)

    def display_brightness(self):
        self.display_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.display_box.set_name("slider-box")

        display_label = Gtk.Label()
        display_label.set_text("Display")
        display_label.set_name("slider-title")
        display_label.set_halign(Gtk.Align.START)
        
        display_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        display_adjustment = Gtk.Adjustment(value=self.current_display_brightness, lower=0, upper=100, step_increment=1, page_increment=10)
        display_scale = Gtk.HScale.new(display_adjustment)
        display_scale.set_digits(0)        
        display_scale.set_draw_value(False)

        display_hbox.pack_start(display_scale, True, True, 0)
        self.display_box.pack_start(display_label, False, False, 0)
        self.display_box.pack_start(display_hbox, False, False, 0)
        
        display_scale.connect("value-changed", self.on_display_changed)
    
    def keyboard_brightness(self):
        self.keyboard_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.keyboard_box.set_name("slider-box")

        keyboard_label = Gtk.Label()
        keyboard_label.set_text("Keyboard")
        keyboard_label.set_name("slider-title")
        keyboard_label.set_halign(Gtk.Align.START)
        self.keyboard_box.pack_start(keyboard_label, False, False, 0)
        
        keyboard_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        keyboard_adjustment = Gtk.Adjustment(value=self.current_keyboard_brightness, lower=0, upper=4, step_increment=1, page_increment=1)
        keyboard_scale = Gtk.HScale.new(keyboard_adjustment)
        keyboard_scale.set_digits(0)
        keyboard_scale.set_draw_value(False)
        keyboard_hbox.pack_start(keyboard_scale, True, True, 0)

        self.keyboard_box.pack_start(keyboard_hbox, False, False, 0)
        
        keyboard_scale.connect("value-changed", self.on_keyboard_changed)

    def css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        provider.load_from_path("/home/jonalm/scripts/qtile/bar_menus/main/main_menu_styles.css")
        visual = screen.get_rgba_visual()
        self.content_area.set_visual(visual)
        self.set_visual(visual)

    def get_slider_data(self):
        self.current_volume = subprocess.check_output("pactl get-sink-volume @DEFAULT_SINK@ | awk -F'/' '{print $2}' | awk -F'%' '{print $1}'", shell=True, text=True).strip()
        self.current_volume = float(self.current_volume)    

        self.current_display_brightness = subprocess.check_output("brillo", shell=True, text=True).strip()
        self.current_display_brightness = float(self.current_display_brightness)

        self.current_keyboard_brightness = subprocess.check_output("brightnessctl --device='asus::kbd_backlight' get", shell=True, text=True).strip()
        self.current_keyboard_brightness = float(self.current_keyboard_brightness)
    
    def on_icon_hover(self, widget, event):
        self.previous_css_class = widget.get_name() 
        if self.previous_css_class == "toggle-right-box":
            widget.set_name("toggle-right-box-enabled")
        else:
            widget.set_name("rofi-icon-hover")

    def on_icon_leave(self, widget, event):
        if self.previous_css_class:
            widget.set_name(self.previous_css_class)

    def get_wifi_ssid(self):
        process = subprocess.Popen(['python3', '/home/jonalm/scripts/qtile/get_wifi_ssid.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout = process.communicate()
        ssid = stdout[0].strip()
        if not self.get_wifi_on():
            return "Off" 
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
            widget.set_name("toggle-left-box-disabled")
            self.wifi_icon.set_name("toggle-icon-disabled")
            self.wifi_ssid.set_text("Off")
        else:
            subprocess.run(["nmcli",  "radio", "wifi", "on"])
            widget.set_name("toggle-left-box-enabled")
            self.wifi_icon.set_name("toggle-icon-enabled")
            self.wifi_ssid.set_text(self.get_wifi_ssid())

    def update_ui_with_networks(self, networks):
        for child in self.list_box.get_children():
            self.list_box.remove(child)
        for network in networks:
            row = Gtk.ListBoxRow()
            label = Gtk.Label()
            if network["IN-USE"]:
                label.set_name("list-obj-active")
            else:
                label.set_name("list-obj")
            label.set_text(network["SSID"])
            label.set_halign(Gtk.Align.START)
            row.add(label)
            self.list_box.add(row)
        self.list_box.show_all()

    def show_wifi_list(self, widget, event):
        if self.wifi_list_active:
            self.wifi_list_active = False
            self.wifi_list_button_icon.set_text("")
            self.wifi_list_button_icon.set_name("toggle-list-button-disabled")
            self.rofi_box.show_all()
            self.wifi_list_box.hide()
        else:
            self.wifi_list_active = True
            self.wifi_list_button_icon.set_text("")
            self.wifi_list_button_icon.set_name("toggle-list-button-enabled")
            self.rofi_box.hide()
            self.wifi_list_box.show_all()

    def update_ui_with_networks(self, networks):
        for child in self.list_box.get_children():
            self.list_box.remove(child)
        for network in networks:
            row = Gtk.ListBoxRow()
            label = Gtk.Label()
            if network["IN-USE"]:
                label.set_name("list-obj-active")
            else:
                label.set_name("list-obj")
            label.set_text(network["SSID"])
            label.set_halign(Gtk.Align.START)
            row.add(label)
            self.list_box.add(row)
        self.list_box.show_all()

    def run_nmcli(self):
        if self.first_wifi_scan:
            output = subprocess.check_output("nmcli device wifi list --rescan no", shell=True).decode("utf-8")
        else:
            output = subprocess.check_output("nmcli device wifi list", shell=True).decode("utf-8")
        
        self.first_wifi_scan = False
        return output

    def fetch_networks(self):
        nmcli_output = self.run_nmcli()
        if nmcli_output:
            lines = nmcli_output.splitlines()
            unique_networks = []

            for line in lines[1:]:
                parts = line.split()
                in_use = False

                if parts[0] == "*":
                    parts.pop(0)
                    in_use = True

                if parts[1] != "--" and "▂" in parts[7]:
                    ssid = f'{parts[7]} {parts[1][:10]}' 
                    unique_networks.append({"SSID": ssid, "IN-USE": in_use})

            unique_networks.sort(key=lambda x: not x["IN-USE"])

            self.update_ui_with_networks(unique_networks)
        
    def get_bluetooth_on(self):
        try:
            bluetooth_state = subprocess.check_output("systemctl status bluetooth | grep Running", shell=True, stderr=subprocess.PIPE, text=True).strip()
            if "Running" in bluetooth_state:
                return True
            else:
                return False
        except subprocess.CalledProcessError as e:
            print(f"Error: Unable to determine Bluetooth state. Error message: {e}")
            return False

    def bluetooth_clicked(self, widget, event):
        if self.get_bluetooth_on():
            subprocess.run(["sudo", "systemctl",  "stop", "bluetooth"])
            widget.set_name("toggle-left-box-disabled")
            self.bluetooth_icon.set_name("toggle-icon-disabled")
            self.bluetooth_device.set_text("Off")
        else:
            subprocess.run(["sudo", "systemctl",  "start", "bluetooth"])
            widget.set_name("toggle-left-box-enabled")
            self.bluetooth_icon.set_name("toggle-icon-enabled")
            self.bluetooth_device.set_text("No device")

    def get_redshift_on(self):
        try:
            redshift_state = subprocess.check_output("xrandr --verbose | grep Gamma", shell=True, stderr=subprocess.PIPE, text=True).strip()
            start_index = redshift_state.find("Gamma: ")
            gamma_values = None
            if start_index != -1:
                gamma_values = redshift_state[start_index + len("Gamma: "):].strip()
            if gamma_values == "1.0:1.0:1.0":
                return False
            else:
                return True
        except subprocess.CalledProcessError:
            print("Error: Unable to determine Bluetooth state")

    def redshift_clicked(self, widget, event):
        if self.get_redshift_on() == True:
            subprocess.run("redshift -P -O 6300", shell=True)
            widget.set_name("toggle-left-box-disabled")
            self.redshift_icon.set_name("toggle-icon-disabled")
            self.redshift_desc.set_text("Off")
        else:
            subprocess.run("redshift -P -O 4500", shell=True)
            widget.set_name("toggle-left-box-enabled")
            self.redshift_icon.set_name("toggle-icon-enabled")
            self.redshift_desc.set_text("On")

    def app_launcher_clicked(self, widget, event):
        subprocess.run(["/home/jonalm/.config/rofi/files/launchers/type-1/launcher.sh"])
        self.exit_remove_pid()

    def search_clicked(self, widget, event):
        subprocess.run(["/home/jonalm/scripts/rofi/search/search_web.sh"])
        self.exit_remove_pid()

    def config_clicked(self, widget, event):
        subprocess.run(["/home/jonalm/scripts/rofi/config/config_files.sh"])
        self.exit_remove_pid()
    
    def power_menu_clicked(self, widget, event):
        subprocess.run(["/home/jonalm/.config/rofi/files/powermenu/type-2/powermenu.sh"])
        self.exit_remove_pid()
    
    def automation_clicked(self, widget, event):
        subprocess.run(["/home/jonalm/scripts/rofi/automation/automation.sh"])
        self.exit_remove_pid()

    def keyboard_shortcut_clicked(self, widget, event):
        subprocess.run(["/home/jonalm/scripts/term/show_keys.sh"])
        self.exit_remove_pid()

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
        if not self.ignore_focus_lost:
            self.exit_remove_pid()

    def on_escape_press(self, widget, event):
        keyval = event.keyval
        if keyval == Gdk.KEY_Escape or keyval == Gdk.KEY_Escape_L:
            self.on_focus_out(widget, event)

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


pid_file = "/home/jonalm/scripts/qtile/bar_menus/main/main_pid_file.pid"
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
        dialog = MainMenu()
        Gtk.main()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    exit(0)

