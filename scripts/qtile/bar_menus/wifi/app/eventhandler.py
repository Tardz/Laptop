from options_window import OptionWindow
from multiprocessing import Process
from gi.repository import Gdk
import subprocess
import os

class EventHandler:
    def wifi_clicked(self, widget, event, parent):
        if parent.wifi_on:
            parent.wifi_on = False
            parent.resize(parent.window_width, 10)
            parent.set_size_request(parent.window_width, 10)
            parent.desc.set_text("Off")
            parent.status_dot.set_name("status-dot-off")
            subprocess.run(["nmcli",  "radio", "wifi", "off"])
            parent.icon.set_name("toggle-icon-disabled")
            parent.list_box.hide()
            parent.list_options_main_box.hide()
        else:
            parent.wifi_on = True
            parent.resize(parent.window_width, parent.window_height)
            parent.set_size_request(parent.window_width, parent.window_height)
            parent.status_dot.set_name("status-dot-inactive")
            subprocess.run(["nmcli",  "radio", "wifi", "on"])
            parent.icon.set_name("toggle-icon-enabled")
            parent.main_box.show_all()

    def scan_clicked(self, widget, event, parent):
        parent.history_shown = False
        parent.active_known_widget = None
        parent.history_box.set_name("list-options-inactive")
        parent.config_title.set_name("list-opitons-title-inactive")
        parent.scan_box.set_name("list-options-active")
        parent.scan_title.set_name("list-opitons-title-active")
        parent.update_list_with_networks()
        
    def history_clicked(self, widget, event, parent):
        parent.active_widget = None
        parent.skip_update = False
        parent.history_box.set_name("list-options-active")
        parent.config_title.set_name("list-opitons-title-active")
        parent.scan_box.set_name("list-options-inactive")
        parent.scan_title.set_name("list-opitons-title-inactive")
        parent.update_list_with_networks(get_known=True)
    
    def on_network_clicked(self, widget, event, main_window, network=False):
        main_window.ignore_focus_lost = True
        main_window.active_widget = widget
        widget.get_parent().get_parent().set_name("row-box-clicked")
        OptionWindow(main_window, network, widget)

    def on_network_pressed(self, entry, widget, main_window, network):
        self.on_network_clicked(widget=widget, parent=main_window, network=network)
        
    def on_password_pressed(self, entry, main_window, password_entry):
        self.on_connect_clicked(main_window=main_window, password_entry=password_entry)

    def on_connect_clicked(self, widget=False, event=False, main_window=None, password_entry=False):
        password = None
        if password_entry:
            password = password_entry.get_text()
            if not password:
                return False
        
        for child in self.main_box.get_children():
            self.main_box.remove(child)

        self.ignore_focus_lost = True
        x, y = main_window.get_position()
        width, height = main_window.get_size()
        dialog_width, dialog_height = width - 80, 80
        self.set_size_request(dialog_width, dialog_height)
        self.resize(dialog_width, dialog_height)
        animation_window_x, animation_window_y = x + (width - dialog_width)/2, y + (height/3) 
        self.move(animation_window_x, animation_window_y)
        
        self.activate_load_circle_stage_1()
        self.connect_process = Process(target=self.connect_process_start, args=(password,))
        self.connect_process.start()
    
    def on_disconnect_clicked(self, entry=False, widget=False, event=False):
        ssid = self.network["SSID"]
        subprocess.call(f"nmcli connection down id {ssid}", shell=True)
        self.exit()

    def on_remove_clicked(self, entry=False, widget=False, event=False):
        ssid = self.network["SSID"]
        subprocess.call(f"nmcli connection delete '{ssid}'", shell=True)
        self.exit()

    def on_focus_out(self, widget, event, parent, escape=False):
        if not parent.ignore_focus_lost or escape:
            self.exit(parent)

    def on_escape_press(self, widget, event, parent):
        keyval = event.keyval
        if keyval == Gdk.KEY_Escape:
            self.on_focus_out(widget, event, parent, True)

    def handle_sigterm(self, signum, frame, parent):
        self.exit(parent) 

    def exit(self, parent):
        parent.exit()