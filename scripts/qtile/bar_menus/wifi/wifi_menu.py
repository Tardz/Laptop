import gi
gi.require_version('Gtk', '3.0')
import subprocess
import os
from gi.repository import Gtk, Gdk, GLib
import time
import json
from Xlib import display
from multiprocessing import Process, Value

class OptionWindow(Gtk.Dialog):
    def __init__(self, parent, main_window, network, active_widget):
        super(OptionWindow, self).__init__(title="Device Options", transient_for=parent)
        self.main_window = main_window
        self.active_widget = active_widget
        self.network = network

        if self.main_window.history_shown:
            self.set_size_request(130, 45)
        else:
            self.set_size_request(130, 90)
        x, y = self.get_mouse_position()
        self.move(x, y)

        self.ignore_focus_lost = False
        self.load_speed = 300
        
        self.wrong_password = Value('b', False)
        self.connect_process_successful = Value('b', False)
        self.connect_process = None 
        self.ping_process_successful = Value('b', False)
        self.ping_process = None 

        self.connect("focus-out-event", self.on_focus_out)
        self.connect("key-press-event", self.on_escape_press)

        self.content_area = self.get_content_area()
        self.content_area.get_style_context().add_class('root')

        connection_button = Gtk.Button()
        connection_button.get_style_context().add_class('buttons')

        if not self.main_window.history_shown:
            self.content_area.pack_start(connection_button, True, True, 0)
        
        password_entry = Gtk.Entry()
        password_entry.get_style_context().add_class('buttons')

        if self.network["KNOWN"]:
            remove_button = Gtk.Button(label = "Remove")
            remove_button.get_style_context().add_class('buttons')
            remove_button.connect("button-press-event", self.on_remove_clicked)
            remove_button.connect("activate", self.on_remove_clicked)

            self.content_area.pack_start(remove_button, True, True, 0)
        else:
            password_entry.set_placeholder_text("Password")
            self.content_area.pack_start(password_entry, True, True, 0)
        
        if self.network["CONNECTED"]:
            connection_button.set_label("Disconnect")
            connection_button.connect("button-press-event", self.on_disconnect_clicked)
            connection_button.connect("activate", self.on_disconnect_clicked)
            self.main_window.previous_network_in_use = True
        else:
            connection_button.set_label("Connect")
            if self.network["KNOWN"]:
                connection_button.connect("button-press-event", self.on_connect_clicked)
                connection_button.connect("activate", self.on_connect_clicked)
                password_entry.connect("activate", self.on_password_pressed)
            else:
                connection_button.connect("button-press-event", self.on_connect_clicked, password_entry)
                connection_button.connect("activate", self.on_password_pressed, password_entry)
                password_entry.connect("activate", self.on_password_pressed, password_entry)
                password_entry.grab_focus()

        self.show_all()
        
    def on_password_pressed(self, entry=False, password_entry=False):
        self.on_connect_clicked(password_entry=password_entry)

    def on_connect_clicked(self, widget=False, event=False, password_entry=False):
        password = None
        if password_entry:
            password = password_entry.get_text()
            if not password:
                return False
        
        for child in self.content_area.get_children():
            self.content_area.remove(child)

        self.ignore_focus_lost = True
        x, y = self.main_window.get_position()
        width, height = self.main_window.get_size()
        dialog_width, dialog_height = width - 80, 80
        self.set_size_request(dialog_width, dialog_height)
        self.resize(dialog_width, dialog_height)
        animation_window_x, animation_window_y = x + (width - dialog_width)/2, y + (height/3) 
        self.move(animation_window_x, animation_window_y)

        connect_animation_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        connect_animation_box.get_style_context().add_class('connect-animation-box')

        self.laptop_icon = Gtk.Label()
        self.laptop_icon.set_text("")
        self.laptop_icon.get_style_context().add_class('connect-animation-icon')
        self.laptop_icon.set_name("connect-animation-active")

        self.load_circle_1 = Gtk.Label()
        self.load_circle_1.set_text("")
        self.load_circle_1.get_style_context().add_class('connect-animation-circle')
        self.load_circle_1.set_name("connect-animation-inactive")

        self.load_circle_2 = Gtk.Label()
        self.load_circle_2.set_text("")
        self.load_circle_2.get_style_context().add_class('connect-animation-circle')
        self.load_circle_2.set_name("connect-animation-inactive")

        self.load_circle_3 = Gtk.Label()
        self.load_circle_3.set_text("")
        self.load_circle_3.get_style_context().add_class('connect-animation-circle')
        self.load_circle_3.set_name("connect-animation-inactive")

        self.network_icon = Gtk.Label()
        if "phone" in self.network["SSID"]:
            self.network_icon.set_text("")
        else:
            self.network_icon.set_text("")
        self.network_icon.get_style_context().add_class('connect-animation-icon')
        self.network_icon.set_name("connect-animation-inactive")

        self.load_circle_4 = Gtk.Label()
        self.load_circle_4.set_text("")
        self.load_circle_4.get_style_context().add_class('connect-animation-circle')
        self.load_circle_4.set_name("connect-animation-inactive")

        self.load_circle_5 = Gtk.Label()
        self.load_circle_5.set_text("")
        self.load_circle_5.get_style_context().add_class('connect-animation-circle')
        self.load_circle_5.set_name("connect-animation-inactive")

        self.load_circle_6 = Gtk.Label()
        self.load_circle_6.set_text("")
        self.load_circle_6.get_style_context().add_class('connect-animation-circle')
        self.load_circle_6.set_name("connect-animation-inactive")

        self.internet_icon = Gtk.Label()
        self.internet_icon.set_text("")
        self.network_icon.get_style_context().add_class('connect-icon')
        self.internet_icon.set_name("connect-animation-inactive")

        connect_animation_box.pack_start(self.laptop_icon,   True, False, 0)
        connect_animation_box.pack_start(self.load_circle_1, True, False, 0)
        connect_animation_box.pack_start(self.load_circle_2, True, False, 0)
        connect_animation_box.pack_start(self.load_circle_3, True, False, 0)
        connect_animation_box.pack_start(self.network_icon,  True, False, 0)
        connect_animation_box.pack_start(self.load_circle_4, True, False, 0)
        connect_animation_box.pack_start(self.load_circle_5, True, False, 0)
        connect_animation_box.pack_start(self.load_circle_6, True, False, 0)
        connect_animation_box.pack_start(self.internet_icon, True, False, 0)

        self.content_area.pack_start(connect_animation_box, True, False, 0)
        self.content_area.show_all()
        
        self.activate_load_circle_stage_1()
        self.connect_process = Process(target=self.connect_process_start, args=(password,))
        self.connect_process.start()

    def connect_process_start(self, password):
        ssid = self.network["SSID"]
        result = None
        if self.network["KNOWN"]:
            result = subprocess.call(f"nmcli connection up id {ssid}", shell=True)
        else: 
            result = subprocess.call(f"nmcli device wifi connect {ssid} password {password}", shell=True)

        if result == 0:
            with self.connect_process_successful.get_lock():
                self.connect_process_successful.value = True
        elif result == 4:
            with self.wrong_password.get_lock():
                self.wrong_password = True
        else:
            self.connect_process_start(password)

    def activate_load_circle_stage_1(self):
        self.load_circle_1.set_name("connect-animation-active")
        GLib.timeout_add(self.load_speed, self.activate_load_circle_2)
        return False

    def activate_load_circle_2(self):
        self.load_circle_2.set_name("connect-animation-active")
        GLib.timeout_add(self.load_speed, self.activate_load_circle_3)
        return False
    
    def activate_load_circle_3(self):
        self.load_circle_3.set_name("connect-animation-active")
        GLib.timeout_add(self.load_speed, self.deactivate_load_circle_stage_1)
        return False
    
    def deactivate_load_circle_stage_1(self):
        with self.wrong_password.get_lock():
            if self.wrong_password.value:
                for child in self.content_area.get_children():
                    self.content_area.remove(child)
                self.wrong_password = False
                self.terminate_connect_process()
                return False
        
        with self.connect_process_successful.get_lock():
            if self.connect_process_successful.value:
                self.terminate_connect_process()
                self.network_icon.set_name("connect-animation-active")
                self.ping_process = Process(target=self.ping_process_start)
                self.ping_process.start()
                GLib.timeout_add(self.load_speed, self.activate_load_circle_stage_2)
            else:
                self.load_circle_1.set_name("connect-animation-inactive")
                self.load_circle_2.set_name("connect-animation-inactive")
                self.load_circle_3.set_name("connect-animation-inactive")
                GLib.timeout_add(self.load_speed, self.activate_load_circle_stage_1)
        return False
    
    def terminate_connect_process(self):
        self.connect_process.terminate()
        self.connect_process.join()
        self.connect_process_successful = False
        self.connect_process = None 

    def ping_process_start(self):
        result = subprocess.call("ping -c 2 google.com", shell=True)
        if result == 0:
            with self.ping_process_successful.get_lock():
                self.ping_process_successful.value = True
                print(f"Worker: {self.ping_process_successful.value}")
        else:
            time.sleep(3)
            self.ping_process_start()
    
    def activate_load_circle_stage_2(self):
        self.load_circle_4.set_name("connect-animation-active")
        GLib.timeout_add(self.load_speed, self.activate_load_circle_4)
        return False

    def activate_load_circle_4(self):
        self.load_circle_5.set_name("connect-animation-active")
        GLib.timeout_add(self.load_speed, self.activate_load_circle_5)
        return False
    
    def activate_load_circle_5(self):
        self.load_circle_6.set_name("connect-animation-active")
        GLib.timeout_add(self.load_speed, self.deactivate_load_circle_stage_2)
        return False

    def deactivate_load_circle_stage_2(self):
        with self.ping_process_successful.get_lock():
            if self.ping_process_successful.value:
                self.ping_process_successful = False
                self.ping_process.terminate()
                self.ping_process.join()
                self.ping_process = None
                self.internet_icon.set_name("connect-animation-active")
                self.ignore_focus_lost = False
                GLib.timeout_add(self.load_speed, self.connection_successful_animation)
            else:
                self.load_circle_4.set_name("connect-animation-inactive")
                self.load_circle_5.set_name("connect-animation-inactive")
                self.load_circle_6.set_name("connect-animation-inactive")
                GLib.timeout_add(self.load_speed, self.activate_load_circle_stage_2)
        return False
    
    def connection_successful_animation(self):
        self.laptop_icon.set_name("connect-animation-success")
        self.network_icon.set_name("connect-animation-success")
        self.internet_icon.set_name("connect-animation-success")
        self.load_circle_1.set_name("connect-animation-success")
        self.load_circle_2.set_name("connect-animation-success")
        self.load_circle_3.set_name("connect-animation-success")
        self.load_circle_4.set_name("connect-animation-success")
        self.load_circle_5.set_name("connect-animation-success")
        self.load_circle_6.set_name("connect-animation-success")
        
        GLib.timeout_add(400, self.exit)
        return False
    
    def on_disconnect_clicked(self, entry=False, widget=False, event=False):
        ssid = self.network["SSID"]
        subprocess.call(f"nmcli connection down id {ssid}", shell=True)
        self.exit()

    def on_remove_clicked(self, entry=False, widget=False, event=False):
        ssid = self.network["SSID"]
        subprocess.call(f"nmcli connection delete '{ssid}'", shell=True)
        self.exit()

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
    
    def on_escape_press(self, widget, event):
        keyval = event.keyval
        if keyval == Gdk.KEY_Escape:
            self.on_focus_out(widget, event, True)

    def on_focus_out(self, widget, event, escape_pressed=False):
        if not self.ignore_focus_lost or escape_pressed:
            self.exit()

    def exit(self):
        if self.ping_process and self.ping_process.is_alive():
            self.ping_process.terminate()
            self.ping_process.join() 
        if self.connect_process and self.connect_process.is_alive():
            self.connect_process.terminate()
            self.connect_process.join()
            
        self.main_window.active_widget = None
        self.main_window.ignore_focus_lost = False
        
        if self.network["CONNECTED"]:
            self.active_widget.get_parent().get_parent().set_name("list-name-box-active")
        else: 
            self.active_widget.get_parent().get_parent().set_name("list-name-box-inactive")

        self.main_window.update_list_with_networks(scan_offline=True)
        self.destroy()

class WifiMenu(Gtk.Dialog):
    def __init__(self, pid_file_path, wifi_process):
        Gtk.Dialog.__init__(self, "Sound Control", None, 0)

        import signal
        self.wifi_process = wifi_process
        signal.signal(signal.SIGTERM, self.handle_sigterm)

        x, y = self.get_mouse_position()
        self.move(x, y)

        self.window_width = 340
        self.window_height = 400

        self.wifi_on = self.get_wifi_on()
        if self.wifi_on:
            self.set_size_request(self.window_width, self.window_height)
        else:
            self.set_size_request(self.window_width, 10)

        self.pid_file_path = pid_file_path
        self.ignore_focus_lost = False
        self.previous_css_class = None
        self.active_widget = None
        self.previous_network_in_use = False
        self.history_shown = False
        self.active_known_widget = None
        self.skip_update = False

        self.content_area = self.get_content_area()

        self.content_area.get_style_context().add_class('content-area')
        self.get_style_context().add_class('root')

        self.css()
        self.title()
        self.list()
        self.list_options()

        self.connect("focus-out-event", self.on_focus_out)
        self.connect("key-press-event", self.on_escape_press)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.main_box.pack_start(self.title_box, False, False, 0)
        self.main_box.pack_start(self.list_main_box, True, True, 0)        
        self.main_box.pack_start(self.list_options_main_box, False, False, 0)

        self.content_area.pack_start(self.main_box, True, True, 0)   

        self.show_all()

        if not self.wifi_on:
            self.resize(self.window_width, 10)
            self.set_size_request(self.window_width, 10)
            self.list_main_box.hide()
            self.list_options_main_box.hide()

    def title(self):
        self.title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.title_box.get_style_context().add_class('toggle-title-box')

        desc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        title = Gtk.Label()
        title.get_style_context().add_class('toggle-title')
        title.set_text("Networks")
        title.set_halign(Gtk.Align.START)

        self.desc = Gtk.Label()
        self.desc.get_style_context().add_class('toggle-desc')
        self.desc.set_halign(Gtk.Align.START)
        if not self.wifi_on:
            self.desc.set_text("Off")

        left_box = Gtk.EventBox()

        self.icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.icon_box.get_style_context().add_class('toggle-icon-box')

        self.icon = Gtk.Label()
        self.icon.get_style_context().add_class('toggle-icon')
        self.icon.set_text("")
        self.icon.set_halign(Gtk.Align.START)

        if self.wifi_on:
            self.icon_box.set_name("toggle-icon-box-enabled")
            self.icon.set_name("toggle-icon-enabled")
        else:
            self.icon_box.set_name("toggle-icon-box-disabled")
            self.icon.set_name("toggle-icon-disabled")

        self.status_dot = Gtk.Label()
        self.status_dot.get_style_context().add_class('status-dot')
        self.status_dot.set_text("")
        if self.wifi_on:
            self.status_dot.set_name("status-dot-inactive")
        else:
            self.status_dot.set_name("status-dot-off")
        self.status_dot.set_halign(Gtk.Align.END)

        self.icon_box.pack_start(self.icon, False, False, 0)
        left_box.add(self.icon_box)
        desc_box.pack_start(title, False, False, 0)
        desc_box.pack_start(self.desc, False, False, 0)
        self.title_box.pack_start(left_box, False, False, 0)
        self.title_box.pack_start(desc_box, False, False, 0)
        self.title_box.pack_start(self.status_dot, True, True, 0)

        left_box.connect("button-press-event", self.wifi_clicked)

    def list(self):
        self.list_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        
        self.list_box = Gtk.ListBox()
        self.list_box.get_style_context().add_class('list')
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.get_style_context().add_class('list-box')
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC) 
        scrolled_window.add(self.list_box)  

        self.list_main_box.pack_start(scrolled_window, True, True, 0)

        self.update_list_with_networks()
        GLib.timeout_add(7000, self.update_list_with_networks)

    def list_options(self):
        self.list_options_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.scan_box = Gtk.EventBox()
        self.scan_box.get_style_context().add_class("toggle-box-list-options")
        self.scan_box.set_name("toggle-box-list-options-active")
        self.scan_title = Gtk.Label()
        self.scan_title.get_style_context().add_class("list-options-title")
        self.scan_title.set_name("list-opitons-title-active")
        self.scan_title.set_text("")

        self.history_box = Gtk.EventBox()
        self.history_box.get_style_context().add_class("toggle-box-list-options")
        self.history_box.set_name("toggle-box-list-options-inactive")
        self.config_title = Gtk.Label()
        self.config_title.get_style_context().add_class("list-options-title")
        self.config_title.set_name("list-opitons-title-inactive")
        self.config_title.set_text("")

        self.scan_box.add(self.scan_title)
        self.history_box.add(self.config_title)

        self.list_options_main_box.pack_start(self.scan_box, True, True, 0)
        self.list_options_main_box.pack_start(self.history_box, True, True, 0)

        self.scan_box.connect("button-press-event", self.scan_clicked)
        self.history_box.connect("button-press-event", self.history_clicked)

    def css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        provider.load_from_path(os.path.expanduser("~/scripts/qtile/bar_menus/wifi/css/wifi_menu_styles.css"))
        visual = screen.get_rgba_visual()
        self.content_area.set_visual(visual)
        self.set_visual(visual)

    def restore_status_dot(self):
        self.status_dot.set_name("status-dot-inactive")
        return False

    def wifi_clicked(self, widget, event):
        if self.wifi_on:
            self.wifi_on = False
            self.resize(self.window_width, 10)
            self.set_size_request(self.window_width, 10)
            self.desc.set_text("Off")
            self.status_dot.set_name("status-dot-off")
            subprocess.run(["nmcli",  "radio", "wifi", "off"])
            self.icon_box.set_name("toggle-icon-box-disabled")
            self.icon.set_name("toggle-icon-disabled")
            self.list_main_box.hide()
            self.list_options_main_box.hide()
        else:
            self.wifi_on = True
            self.resize(self.window_width, self.window_height)
            self.set_size_request(self.window_width, self.window_height)
            self.status_dot.set_name("status-dot-inactive")
            subprocess.run(["nmcli",  "radio", "wifi", "on"])
            self.icon_box.set_name("toggle-icon-box-enabled")
            self.icon.set_name("toggle-icon-enabled")
            self.main_box.show_all()

    def scan_clicked(self, widget, event):
        self.history_shown = False
        self.active_known_widget = None
        self.history_box.set_name("toggle-box-list-options-inactive")
        self.config_title.set_name("list-opitons-title-inactive")
        self.scan_box.set_name("toggle-box-list-options-active")
        self.scan_title.set_name("list-opitons-title-active")
        self.update_list_with_networks()
        
    def history_clicked(self, widget, event):
        self.active_widget = None
        self.skip_update = False
        self.history_box.set_name("toggle-box-list-options-active")
        self.config_title.set_name("list-opitons-title-active")
        self.scan_box.set_name("toggle-box-list-options-inactive")
        self.scan_title.set_name("list-opitons-title-inactive")
        self.update_list_with_networks(get_known=True)
    
    def on_network_clicked(self, widget, event=False, network=False):
        self.ignore_focus_lost = True
        self.active_widget = widget
        widget.get_parent().get_parent().set_name("list-name-box-clicked")
        dialog = OptionWindow(self, self, network, widget)
        dialog.run()

    def on_network_pressed(self, entry, widget, network):
        self.on_network_clicked(widget=widget, network=network)

    def get_wifi_on(self):
        wifi_state = subprocess.check_output(["nmcli",  "radio", "wifi"]).strip().decode("utf-8")
        if wifi_state == "enabled":
            return True
        elif wifi_state == "disabled":
            return False
        
    def get_networks(self):
        with open(os.path.expanduser('~/scripts/qtile/bar_menus/wifi/data/wifi_networks.json'), 'r') as json_file:
            networks = json.load(json_file)
        return networks
        
    def get_known_networks(self):
        known_networks_output = subprocess.check_output("nmcli connection show ", shell=True).decode("utf-8").strip()
        known_networks = []
        from io import StringIO
        import pandas as pd

        df = pd.read_fwf(StringIO(known_networks_output), header=0)

        data = df.to_dict(orient='records')

        for line in data:
            ssid = line["NAME"]
            type = line["TYPE"]

            if type == "wifi":
                known_networks.append({
                    "SSID": ssid, 
                    "STRENGTH": "", 
                    "CONNECTED": False, 
                    "KNOWN": True
                })
            
        return known_networks
    
    def get_networks_offline(self):
        nmcli_output = subprocess.check_output("nmcli device wifi list --rescan no", shell=True).decode("utf-8")
        known_networks = get_known_networks()
        if nmcli_output:
            lines = nmcli_output.splitlines()
            unique_networks = []

            seen_ssids = set()

            for line in lines[1:]:
                parts = line.split()
                connected = False
                network_known = False
                connected_marker = parts[0]

                if connected_marker == "*":
                    parts.pop(0)
                    connected = True
                
                ssid = parts[1]
                strength = parts[7]

                if ssid == "--" or "▂" not in strength:
                    ssid = None
                elif ssid in known_networks:
                        network_known = True
                        ssid = ssid

                if ssid and (ssid not in seen_ssids or connected):
                    if strength == "▂▄▆_":
                        strength = "▂▄▆▂"
                    elif strength == "▂▄__":
                        strength = "▂▄▂▂"                        
                    elif strength == "▂___":
                        strength = "▂▂▂▂"

                    unique_networks.append({
                        "SSID": ssid, 
                        "STRENGTH": strength, 
                        "CONNECTED": connected, 
                        "KNOWN": network_known
                    })
                    seen_ssids.add(ssid)

            unique_networks.sort(key=lambda x: (not x["CONNECTED"], not x["KNOWN"]))

        return unique_networks
    
    def update_list_with_networks(self, get_known=False, scan_offline=False):
        if self.skip_update and not scan_offline:
            self.skip_update = False
            return True
        if not self.active_widget and self.wifi_on and not self.history_shown:
            if get_known:
                self.history_shown = True
                
            self.status_dot.set_name("status-dot-list-update")
            GLib.timeout_add(300, self.restore_status_dot)
            
            if scan_offline:
                networks = self.get_networks_offline()
                self.skip_update = True
            elif get_known:
                networks = self.get_known_networks()
                print(networks)
            else:
                networks = self.get_networks()

            if not networks:
                return True
            
            self.desc.set_text(f"{len(networks)} Available")
            
            for child in self.list_box.get_children():
                self.list_box.remove(child)

            for network in networks:
                row = Gtk.ListBoxRow()
                row.get_style_context().add_class('row')
                name = Gtk.Label()
                name.get_style_context().add_class('list-name')
                name.set_text(network["SSID"][:15])
                name.set_halign(Gtk.Align.START)

                list_content_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
                list_content_main_box.get_style_context().add_class('list-name-box')

                list_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

                list_obj_icon_box = Gtk.EventBox()
                list_obj_icon_box.get_style_context().add_class('list-icon-box')
                icon = Gtk.Label()
                icon.get_style_context().add_class('list-icon')

                list_obj_clickable_box = Gtk.EventBox()
                list_obj_clickable_box.connect("button-press-event", self.on_network_clicked, network)

                if network["CONNECTED"]:
                    list_content_main_box.set_name("list-name-box-active")
                else:
                    list_content_main_box.set_name("list-name-box-inactive")

                if not get_known:
                    icon.set_name("list-icon")
                    icon.set_text(network["STRENGTH"])
                    list_obj_icon_box.add(icon)
                    list_content_box.pack_start(list_obj_icon_box, False, False, 0)
                
                list_obj_clickable_box.add(name)
                list_content_box.pack_start(list_obj_clickable_box, False, False, 0)

                if network["KNOWN"] and not get_known:
                    known_icon = Gtk.Label()
                    known_icon.set_halign(Gtk.Align.END)
                    known_icon.get_style_context().add_class('known-icon')
                    if network["CONNECTED"]:
                        known_icon.set_name("known-icon-active")
                    else:
                        known_icon.set_name("known-icon-inactive")
                    known_icon.set_text("")
                    list_content_box.pack_start(known_icon, True, True, 0)
                    
                list_content_main_box.pack_start(list_content_box, False, False, 0)
                
                row.add(list_content_main_box)
                row.connect("activate", self.on_network_pressed, list_obj_clickable_box, network)
                self.list_box.add(row)

            self.list_box.show_all()

        return True

    def get_mouse_position(self):
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

    def on_focus_out(self, widget, event, escape=False):
        if not self.ignore_focus_lost or escape:
            self.exit_remove_pid()

    def on_escape_press(self, widget, event):
        keyval = event.keyval
        if keyval == Gdk.KEY_Escape:
            self.on_focus_out(widget, event, True)

    def handle_sigterm(self, signum, frame):
        self.exit_remove_pid() 

    def exit_remove_pid(self):
        try:
            if self.wifi_process.is_alive():
                self.wifi_process.terminate()
                self.wifi_process.join() 

            with open(self.pid_file_path, "r") as file:
                pid = int(file.read().strip())
            try:
                os.remove(self.pid_file_path)
                os.kill(pid, 15)
            except ProcessLookupError:
                pass
        finally:
            exit(0)

def get_known_networks():
    known_networks_output = subprocess.check_output("nmcli connection show ", shell=True).decode("utf-8")
    lines = known_networks_output.splitlines()
    known_networks = []

    for line in lines[1:]:
        parts = line.split()
        ssid = parts[0]

        known_networks.append(ssid)
        
    return known_networks

def get_wifi_on():
    wifi_state = subprocess.check_output(["nmcli",  "radio", "wifi"]).strip().decode("utf-8")
    if wifi_state == "enabled":
        return True
    elif wifi_state == "disabled":
        return False

def wifi_process():
    while True:
        if get_wifi_on():
            nmcli_output = subprocess.check_output("nmcli device wifi list", shell=True).decode("utf-8")
            known_networks = get_known_networks()
            if nmcli_output:
                lines = nmcli_output.splitlines()
                unique_networks = []

                seen_ssids = set()

                for line in lines[1:]:
                    parts = line.split()
                    connected = False
                    network_known = False
                    connected_marker = parts[0]

                    if connected_marker == "*":
                        parts.pop(0)
                        connected = True
                    
                    ssid = parts[1]
                    strength = parts[7]

                    if ssid == "--" or "▂" not in strength:
                        ssid = None
                    elif ssid in known_networks:
                            network_known = True
                            ssid = ssid

                    if ssid and (ssid not in seen_ssids or connected):
                        if strength == "▂▄▆_":
                            strength = "▂▄▆▂"
                        elif strength == "▂▄__":
                            strength = "▂▄▂▂"                        
                        elif strength == "▂___":
                            strength = "▂▂▂▂"

                        unique_networks.append({
                            "SSID": ssid, 
                            "STRENGTH": strength, 
                            "CONNECTED": connected, 
                            "KNOWN": network_known
                        })
                        seen_ssids.add(ssid)

                unique_networks.sort(key=lambda x: (not x["CONNECTED"], not x["KNOWN"]))

            with open(os.path.expanduser('~/scripts/qtile/bar_menus/wifi/data/wifi_networks.json'), 'w') as json_file:
                json.dump(unique_networks, json_file, indent=2)

            time.sleep(4)
        else:
            time.sleep(4)

if __name__ == '__main__':
    pid_file_path = os.path.expanduser("~/scripts/qtile/bar_menus/wifi/wifi_menu_pid_file.pid")
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

            process = Process(target=wifi_process)
            process.start()

            dialog = WifiMenu(pid_file_path, process)
            Gtk.main()
                    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        exit(0)
