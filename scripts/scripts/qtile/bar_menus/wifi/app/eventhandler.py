import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk
import subprocess
import copy
import sys
import os

class EventHandler:
    def __init__(self, app):
        self.app = app

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