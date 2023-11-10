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
        self.set_default_size(100, 300)

        x, y = self.get_mouse_position()

        if x and y:
            self.move(x - 120, y - 50)

        self.ignore_focus_lost = False
        self.previous_css_class = None
        self.wifi_list_active = False
        self.first_wifi_scan = True

        self.content_area = self.get_content_area()
        self.content_area.set_name("content-area")
        self.set_name("root")

        self.css()
        self.wifi_list()

        self.connect("focus-out-event", self.on_focus_out)
        self.connect("key-press-event", self.on_escape_press)

        self.content_area.pack_start(self.wifi_list_box, True, True, 0)

        self.show_all()

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
            list_obj_box = Gtk.EventBox()

            if network["IN-USE"]:
                label.set_name("list-obj-active")
            else:
                label.set_name("list-obj")
            label.set_text(network["SSID"])
            label.set_halign(Gtk.Align.START)
            
            list_obj_box.add(label)
            row.add(list_obj_box)
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
