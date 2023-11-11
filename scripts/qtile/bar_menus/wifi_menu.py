import gi
gi.require_version('Gtk', '3.0')
import subprocess
import os
import asyncio
import threading
import multiprocessing
import time
from Xlib import display 
from gi.repository import Gtk, Gdk, Gio, GObject, GLib
from dbus.mainloop.glib import DBusGMainLoop

class WifiMenu(Gtk.Dialog):
    def __init__(self):
        self.pid_file = "/home/jonalm/scripts/qtile/bar_menus/wifi_menu_pid_file.pid"
        Gtk.Dialog.__init__(self, "Sound Control", None, 0)
        if self.get_wifi_on():
            self.set_default_size(340, 500)

        x, y = self.get_mouse_position()

        if x and y:
            self.move(x - 120, y - 18)

        self.ignore_focus_lost = False
        self.previous_css_class = None
        self.wifi_list_active = False
        self.first_wifi_scan = True
        self.active_network_widget = None
        self.previouse_network_in_use = False

        self.content_area = self.get_content_area()
        self.content_area.set_name("content-area")
        self.set_name("root")

        self.css()
        self.wifi_list()
        self.wifi_title()

        self.connect("focus-out-event", self.on_focus_out)
        self.connect("key-press-event", self.on_escape_press)

        self.content_area.pack_start(self.wifi_title_box, False, False, 0)        

        if self.get_wifi_on():
            # print(self.get_wifi_on)
            print("iawdjoaiwjd")
            self.content_area.pack_start(self.wifi_list_box, True, True, 0)
        
        self.show_all()

    def wifi_title(self):
        self.wifi_title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.wifi_title_box.set_name("toggle-box")

        wifi_title = Gtk.Label()
        wifi_title.set_text("Networks")
        wifi_title.set_name("toggle-title")
        wifi_title.set_halign(Gtk.Align.START)

        wifi_left_box = Gtk.EventBox()
        wifi_left_box.set_name("toggle-left-box")

        self.wifi_icon_background_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        self.wifi_icon = Gtk.Label()
        self.wifi_icon.set_text("")
        self.wifi_icon.set_halign(Gtk.Align.START)

        if self.get_wifi_on():
            self.wifi_icon_background_box.set_name("toggle-icon-background-enabled")
            self.wifi_icon.set_name("toggle-icon-enabled")
        else:
            self.wifi_icon_background_box.set_name("toggle-icon-background-disabled")
            self.wifi_icon.set_name("toggle-icon-disabled")

        self.wifi_icon_background_box.pack_start(self.wifi_icon, False, False, 0)
        wifi_left_box.add(self.wifi_icon_background_box)
        self.wifi_title_box.pack_start(wifi_left_box, False, False, 0)
        self.wifi_title_box.pack_start(wifi_title, True, True, 0)

        wifi_left_box.connect("button-press-event", self.wifi_clicked)

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
        GLib.timeout_add(8000, self.fetch_networks)

    def css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        provider.load_from_path("/home/jonalm/scripts/qtile/bar_menus/wifi_menu_styles.css")
        visual = screen.get_rgba_visual()
        self.content_area.set_visual(visual)
        self.set_visual(visual)

    def wifi_clicked(self, widget, event):
        if self.get_wifi_on():
            subprocess.run(["nmcli",  "radio", "wifi", "off"])
            self.wifi_icon_background_box.set_name("toggle-icon-background-disabled")
            self.wifi_icon.set_name("toggle-icon-disabled")
            self.content_area.remove(self.wifi_list_box)
            self.set_default_size(0, 0)
        else:
            subprocess.run(["nmcli",  "radio", "wifi", "on"])
            self.wifi_icon_background_box.set_name("toggle-icon-background-enabled")
            self.wifi_icon.set_name("toggle-icon-enabled")
            self.content_area.pack_start(self.wifi_list_box, True, True, 0)
            self.set_default_size(300, 500)

    def get_wifi_on(self):
        wifi_state = subprocess.check_output(["nmcli",  "radio", "wifi"]).strip().decode("utf-8")
        if wifi_state == "enabled":
            return True
        elif wifi_state == "disabled":
            return False

    def on_connect_clicked(self, widget, event, network, password_entry):
        ssid = network["SSID"][5:]

        if network["NETWORK-KNOWN"]:
            subprocess.call(f"nmcli connection up id {ssid}", shell=True)
        else: 
            password = password_entry.get_text()
            subprocess.call(f"nmcli device wifi connect {ssid} password {password}", shell=True)
            
        self.active_network_widget = None
        self.first_wifi_scan = True
        self.fetch_networks()

    def on_disconnect_clicked(self, widget, event, network):
        ssid = network["SSID"][5:]
        subprocess.call(f"nmcli connection down id {ssid}", shell=True)
        print("disconnected")
        self.active_network_widget = None
        self.first_wifi_scan = True
        self.fetch_networks()

    def on_forget_clicked(self, widget, event, network):
        ssid = network["SSID"][5:]
        subprocess.call(f"nmcli connection delete {ssid}", shell=True)
        self.active_network_widget = None
        self.first_wifi_scan = True
        self.fetch_networks()

    def network_clicked(self, widget, event, network, network_in_use):
        if self.active_network_widget:
            buttons = self.active_network_widget.get_parent().get_children()
            for child in buttons[1:]:
                self.active_network_widget.get_parent().remove(child)
            
            self.active_network_widget.get_parent().set_name("list-content-box-inactive")

            if self.previouse_network_in_use:
                self.active_network_widget.get_parent().set_name("list-obj-box-active")
                self.previouse_network_in_use = False

            if self.active_network_widget == widget:
                self.active_network_widget = None
                return True

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        connection_button = Gtk.Button()
        connection_button.connect("key-press-event", self.on_connect_clicked)
        button_box.pack_start(connection_button, True, True, 0)
        
        password_entry = Gtk.Entry()

        if network["NETWORK-KNOWN"]:
            remove_button = Gtk.Button(label = "Remove")
            remove_button.connect("button-press-event", self.on_forget_clicked, network)
            button_box.pack_start(remove_button, True, True, 0)
        else:
            password_entry.set_placeholder_text("Password")
            button_box.pack_start(password_entry, True, True, 0)
        
        if network_in_use:
            connection_button.set_label("Disconnect")
            connection_button.connect("button-press-event", self.on_disconnect_clicked, network)
            self.previouse_network_in_use = True
        else:
            connection_button.set_label("Connect")
            connection_button.connect("button-press-event", self.on_connect_clicked, network, password_entry)
        
        widget.get_parent().set_name("list-content-box-active")
        widget.get_parent().pack_start(button_box, False, False, 0)     
        widget.get_parent().show_all()

        self.active_network_widget = widget
        return True
    
    def update_ui_with_networks(self, networks):
        for child in self.list_box.get_children():
            self.list_box.remove(child)
        for network in networks:
            row = Gtk.ListBoxRow()
            label = Gtk.Label()

            list_content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

            list_obj_clickable_box = Gtk.EventBox()
            list_obj_clickable_box.connect("button-press-event", self.network_clicked, network, network["IN-USE"])

            if network["IN-USE"]:
                label.set_name("list-obj")
                list_content_box.set_name("list-obj-box-active")
            else:
                label.set_name("list-obj")

            label.set_text(network["SSID"][:20])
            label.set_halign(Gtk.Align.START)
            
            list_obj_clickable_box.add(label)
            list_content_box.pack_start(list_obj_clickable_box, False, False, 0)
            row.add(list_content_box)
            self.list_box.add(row)

        self.list_box.show_all()

    def scan_networks(self):
        if self.first_wifi_scan:
            output = subprocess.check_output("nmcli device wifi list --rescan no", shell=True).decode("utf-8")
        else:
            output = subprocess.check_output("nmcli device wifi list", shell=True).decode("utf-8")
        
        self.first_wifi_scan = False
        return output
    
    def get_known_networks(self):
        known_networks_output = subprocess.check_output("nmcli connection show ", shell=True).decode("utf-8")
        lines = known_networks_output.splitlines()
        known_networks = []

        for line in lines[1:]:
            parts = line.split()
            ssid = parts[0]
            known_networks.append(ssid)
            
        return known_networks

    def fetch_networks(self):
        if not self.active_network_widget:            
            nmcli_output = self.scan_networks()
            known_networks = self.get_known_networks()
            if nmcli_output:
                lines = nmcli_output.splitlines()
                unique_networks = []

                seen_ssids = set()

                for line in lines[1:]:
                    parts = line.split()
                    in_use = False

                    if parts[0] == "*":
                        parts.pop(0)
                        in_use = True

                    if parts[1] != "--" and "▂" in parts[7]:
                        ssid = f'{parts[7]} {parts[1][:]}' 

                        network_known = False
                        if ssid[5:] in known_networks:
                            network_known = True

                    if ssid[5:] not in seen_ssids or in_use:
                        unique_networks.append({"SSID": ssid, "IN-USE": in_use, "NETWORK-KNOWN": network_known})
                        seen_ssids.add(ssid[5:])

                unique_networks.sort(key=lambda x: (not x["IN-USE"], not x["NETWORK-KNOWN"]))

                self.update_ui_with_networks(unique_networks)

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

if __name__ == '__main__':
    pid_file = "/home/jonalm/scripts/qtile/bar_menus/wifi_menu_pid_file.pid"
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
            dialog = WifiMenu()
            Gtk.main()
                    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        exit(0)
