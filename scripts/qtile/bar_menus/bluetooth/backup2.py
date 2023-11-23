import gi
gi.require_version('Gtk', '3.0')
import subprocess
import os
from Xlib import display 
from gi.repository import Gtk, Gdk, Gio, GObject, GLib
from dbus.mainloop.glib import DBusGMainLoop
from multiprocessing import Process, Event
import time
import signal
import json

class OptionWindow(Gtk.Dialog):
    def __init__(self, parent, main_window, device, active_widget):
        super(OptionWindow, self).__init__(title="Device Options", transient_for=parent)
        self.main_window = main_window
        self.active_widget = active_widget
        self.device = device

        self.set_default_size(150, 100)
        
        x, y = self.get_mouse_position()
        self.move(x, y)

        self.connect("focus-out-event", self.on_focus_out)

        self.set_name("root")
        content_area = self.get_content_area()
        content_area.set_name("content-area")

        connection_button = Gtk.Button()
        connection_button.set_name("buttons")
        content_area.pack_start(connection_button, True, True, 0)
        
        if self.device["CONNECTED"]:
            connection_button.set_label("Disconnect")
            connection_button.connect("button-press-event", self.on_disconnect_clicked)
            self.previouse_widget_in_use = True
        else:
            connection_button.set_label("Connect")
            connection_button.connect("button-press-event", self.on_connect_clicked)

        trust_button = Gtk.Button()
        trust_button.set_name("buttons")
        content_area.pack_start(trust_button, True, True, 0)

        if self.device["DEVICE-TRUSTED"]:
            trust_button.set_label("Untrust")
            trust_button.connect("button-press-event", self.on_untrust_clicked)
        else:
            trust_button.set_label("Trust")
            trust_button.connect("button-press-event", self.on_trust_clicked)

        if self.device["DEVICE-KNOWN"]:
            remove_button = Gtk.Button(label = "Remove")
            remove_button.set_name("buttons")
            remove_button.connect("button-press-event", self.on_remove_clicked)
            content_area.pack_start(remove_button, True, True, 0)

        self.show_all()

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

    def on_trust_clicked(self, widget, event):
        device_addr = self.device["MAC-ADDR"]
        subprocess.call(f"bluetoothctl trust {device_addr}", shell=True)

        self.main_window.active_widget = None
        self.main_window.update_ui_with_devices()
        self.exit()

    def on_untrust_clicked(self, widget, event):
        device_addr = self.device["MAC-ADDR"]
        subprocess.call(f"bluetoothctl untrust {device_addr}", shell=True)

        self.main_window.active_widget = None
        self.main_window.update_ui_with_devices()
        self.exit()

    def on_remove_clicked(self, widget, event):
        device_addr = self.device["MAC-ADDR"]
        subprocess.call(f"bluetoothctl remove {device_addr}", shell=True)

        self.main_window.active_widget = None
        self.main_window.update_ui_with_devices()
        self.exit()

    def on_disconnect_clicked(self, widget, event):
        device_addr = self.device["MAC-ADDR"]
        subprocess.call(f"bluetoothctl disconnect {device_addr}", shell=True)

        self.main_window.active_widget = None
        self.main_window.update_ui_with_devices()
        self.exit()

    def on_connect_clicked(self, widget, event):
        device_addr = self.device["MAC-ADDR"]
        subprocess.call(f"bluetoothctl connect {device_addr}", shell=True)
            
        self.main_window.active_widget = None
        self.main_window.update_ui_with_devices()
        self.exit()
    
    def on_focus_out(self, widget, event):
        self.exit()

    def exit(self):
        if self.device["CONNECTED"]:
            self.active_widget.get_parent().get_parent().set_name("list-obj-box-active")
        else: 
            self.active_widget.get_parent().get_parent().set_name("list-obj-box-inactive")
        self.main_window.ignore_focus_lost = False
        self.main_window.active_widget = None
        self.destroy()

class BluetoothMenu(Gtk.Dialog):
    def __init__(self, bluetooth_process):
        self.pid_file = "/home/jonalm/scripts/qtile/bar_menus/bluetooth/bluetooth_menu_pid_file.pid"
        Gtk.Dialog.__init__(self, "Bluetooth menu", None, 0)

        self.bluetooth_process = bluetooth_process
        signal.signal(signal.SIGTERM, self.handle_sigterm)

        x, y = self.get_mouse_position()

        self.move(x - 160, 5)

        self.window_width = 340
        self.window_height = 300

        self.bluetooth_on = self.get_bluetooth_on()
        if self.bluetooth_on:
            self.set_size_request(self.window_width, self.window_height)
        else:
            self.set_size_request(self.window_width, 20)

        self.ignore_focus_lost = False
        self.previous_css_class = None
        self.active_widget = None
        self.previouse_widget_in_use = False
        self.history_shown = False
        self.active_known_widget = None
        self.load_bars_active = False
        self.load_speed = 40
        self.load_icon = ""
        self.no_devices = False

        self.content_area = self.get_content_area()
        self.content_area.set_name("content-area")
        self.set_name("root")

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        self.css()
        self.title() 
        self.initialize_loading_screen()
        self.list()
        self.list_options()

        self.connect("focus-out-event", self.on_focus_out)
        self.connect("key-press-event", self.on_escape_press)

        self.main_box.pack_start(self.title_main_box, False, False, 0)
        self.main_box.pack_start(self.list_main_box, True, True, 0)        
        self.main_box.pack_start(self.list_options_main_box, False, False, 0)

        self.content_area.pack_start(self.main_box, True, True, 0)        

        self.show_all()
        self.load_bar_box.hide()

        if not self.bluetooth_on:
            self.resize(self.window_width, 10)
            self.set_size_request(self.window_width, 10)
            self.list_main_box.hide()
            self.list_options_main_box.hide()
        
        self.update_ui_with_devices()

    def title(self):
        self.title_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.title_main_box.set_name("toggle-box")

        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        self.desc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.desc_box.set_name("toggle-desc-box")
        
        title = Gtk.Label() 
        title.set_text("Devices")
        title.set_name("toggle-title")
        title.set_halign(Gtk.Align.START)

        self.desc = Gtk.Label()
        if not self.bluetooth_on:
            self.desc.set_text("Off")
        self.desc.set_name("toggle-desc")
        self.desc.set_halign(Gtk.Align.START)

        left_box = Gtk.EventBox()
        left_box.set_name("toggle-left-box")

        self.icon_background_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        self.icon = Gtk.Label()
        self.icon.set_text("")
        self.icon.set_halign(Gtk.Align.START)

        if self.bluetooth_on:
            self.icon_background_box.set_name("toggle-icon-background-enabled")
            self.icon.set_name("toggle-icon-enabled")
        else:
            self.icon_background_box.set_name("toggle-icon-background-disabled")
            self.icon.set_name("toggle-icon-disabled")

        self.status_dot = Gtk.Label()
        self.status_dot.set_text("")
        self.status_dot.set_name("status-dot-inactive")
        self.status_dot.set_halign(Gtk.Align.END)
        
        self.icon_background_box.pack_start(self.icon, False, False, 0)
        left_box.add(self.icon_background_box)
        self.desc_box.pack_start(title, False, False, 0)
        self.desc_box.pack_start(self.desc, False, False, 0)
        title_box.pack_start(left_box, False, False, 0)
        title_box.pack_start(self.desc_box, False, False, 0)
        title_box.pack_start(self.status_dot, True, True, 0)

        self.title_main_box.pack_start(title_box, False, False, 0)
        
        left_box.connect("button-press-event", self.bluetooth_clicked)

    def list(self):
        self.list_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        
        self.list_box = Gtk.ListBox()
        self.list_box.set_name("list")
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_name("list-box")
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC) 
        scrolled_window.add(self.list_box)  

        self.list_main_box.pack_start(scrolled_window, True, True, 0)

        GLib.timeout_add(6000, self.update_ui_with_devices)

    def list_options(self):
        self.list_options_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.scan_box = Gtk.EventBox()
        self.scan_box.set_name("toggle-box-list-options-active")
        self.scan_title = Gtk.Label()
        self.scan_title.set_text("")
        self.scan_title.set_name("list-opitons-title-active")

        self.config_box = Gtk.EventBox()
        self.config_box.set_name("toggle-box-list-options-inactive")
        self.config_title = Gtk.Label()
        self.config_title.set_text("")
        self.config_title.set_name("list-opitons-title-inactive")

        self.scan_box.add(self.scan_title)
        self.config_box.add(self.config_title)

        self.list_options_main_box.pack_start(self.scan_box, True, True, 0)
        self.list_options_main_box.pack_start(self.config_box, True, True, 0)

        self.scan_box.connect("button-press-event", self.scan_clicked)
        self.config_box.connect("button-press-event", self.history_clicked)

    def initialize_loading_screen(self):
        self.load_bar_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.load_bar_box.set_name("load-box")

        self.load_bar_1 = Gtk.Label() 
        self.load_bar_1.set_name("load-circle-inactive")
        self.load_bar_1.set_text(self.load_icon)

        self.load_bar_2 = Gtk.Label() 
        self.load_bar_2.set_name("load-circle-inactive")
        self.load_bar_2.set_text(self.load_icon)
        
        self.load_bar_3 = Gtk.Label() 
        self.load_bar_3.set_name("load-circle-inactive")
        self.load_bar_3.set_text(self.load_icon)
        
        self.load_bar_4 = Gtk.Label() 
        self.load_bar_4.set_name("load-circle-inactive")
        self.load_bar_4.set_text(self.load_icon)

        self.load_bar_5 = Gtk.Label() 
        self.load_bar_5.set_name("load-circle-inactive")
        self.load_bar_5.set_text(self.load_icon)

        self.load_bar_6 = Gtk.Label() 
        self.load_bar_6.set_name("load-circle-inactive")
        self.load_bar_6.set_text(self.load_icon)
        
        self.load_bar_7 = Gtk.Label() 
        self.load_bar_7.set_name("load-circle-inactive")
        self.load_bar_7.set_text(self.load_icon)
        
        self.load_bar_8 = Gtk.Label() 
        self.load_bar_8.set_name("load-circle-inactive")
        self.load_bar_8.set_text(self.load_icon)

        self.load_bar_9 = Gtk.Label() 
        self.load_bar_9.set_name("load-circle-inactive")
        self.load_bar_9.set_text(self.load_icon)

        self.load_bar_10 = Gtk.Label() 
        self.load_bar_10.set_name("load-circle-inactive")
        self.load_bar_10.set_text(self.load_icon)
        
        self.load_bar_11 = Gtk.Label() 
        self.load_bar_11.set_name("load-circle-inactive")
        self.load_bar_11.set_text(self.load_icon)
        
        self.load_bar_12 = Gtk.Label() 
        self.load_bar_12.set_name("load-circle-inactive")
        self.load_bar_12.set_text(self.load_icon)

        self.load_bar_13 = Gtk.Label() 
        self.load_bar_13.set_name("load-circle-inactive")
        self.load_bar_13.set_text(self.load_icon)

        self.load_bar_14 = Gtk.Label() 
        self.load_bar_14.set_name("load-circle-inactive")
        self.load_bar_14.set_text(self.load_icon)
        
        self.load_bar_15 = Gtk.Label() 
        self.load_bar_15.set_name("load-circle-inactive")
        self.load_bar_15.set_text(self.load_icon)
        
        self.load_bar_16 = Gtk.Label() 
        self.load_bar_16.set_name("load-circle-inactive")
        self.load_bar_16.set_text(self.load_icon)

        self.load_bar_17 = Gtk.Label() 
        self.load_bar_17.set_name("load-circle-inactive")
        self.load_bar_17.set_text(self.load_icon)
        
        self.load_bar_box.pack_start(self.load_bar_1, False, False, 0)
        self.load_bar_box.pack_start(self.load_bar_2, False, False, 0)
        self.load_bar_box.pack_start(self.load_bar_3, False, False, 0)
        self.load_bar_box.pack_start(self.load_bar_4, False, False, 0)
        self.load_bar_box.pack_start(self.load_bar_5, False, False, 0)
        self.load_bar_box.pack_start(self.load_bar_6, False, False, 0)
        self.load_bar_box.pack_start(self.load_bar_7, False, False, 0)
        self.load_bar_box.pack_start(self.load_bar_8, False, False, 0)
        self.load_bar_box.pack_start(self.load_bar_9, False, False, 0)
        self.load_bar_box.pack_start(self.load_bar_10, False, False, 0)
        self.load_bar_box.pack_start(self.load_bar_11, False, False, 0)
        self.load_bar_box.pack_start(self.load_bar_12, False, False, 0)
        self.load_bar_box.pack_start(self.load_bar_13, False, False, 0)
        self.load_bar_box.pack_start(self.load_bar_14, False, False, 0)
        self.load_bar_box.pack_start(self.load_bar_15, False, False, 0)
        self.load_bar_box.pack_start(self.load_bar_16, False, False, 0)
        self.load_bar_box.pack_start(self.load_bar_17, False, False, 0)
        
        self.desc_box.pack_start(self.load_bar_box, True, True, 0)

    def css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        provider.load_from_path("/home/jonalm/scripts/qtile/bar_menus/bluetooth/bluetooth_menu_styles.css")
        visual = screen.get_rgba_visual()
        self.content_area.set_visual(visual)
        self.set_visual(visual)

    def restore_status_dot(self):
        self.status_dot.set_name("status-dot-inactive")
        return False
    
    def activate_load_bars(self, loop_times):
        if self.load_bars_active:
            self.load_bar_1.set_name("load-circle-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_2, loop_times)
        else:
            return False
        
    def activate_load_bar_2(self, loop_times):
        if self.load_bars_active:
            self.load_bar_1.set_name("load-circle-inactive")
            self.load_bar_2.set_name("load-circle-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_3, loop_times)
        else:
            return False
        
    def activate_load_bar_3(self, loop_times):
        if self.load_bars_active:
            self.load_bar_2.set_name("load-circle-inactive")
            self.load_bar_3.set_name("load-circle-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_4, loop_times)
        else:
            return False
        
    def activate_load_bar_4(self, loop_times):
        if self.load_bars_active:
            self.load_bar_3.set_name("load-circle-inactive")
            self.load_bar_4.set_name("load-circle-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_5, loop_times)
        else:
            return False
        
    def activate_load_bar_5(self, loop_times):
        if self.load_bars_active:
            self.load_bar_4.set_name("load-circle-inactive")
            self.load_bar_5.set_name("load-circle-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_6, loop_times)
        else:
            return False
        
    def activate_load_bar_6(self, loop_times):
        if self.load_bars_active:
            self.load_bar_5.set_name("load-circle-inactive")
            self.load_bar_6.set_name("load-circle-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_7, loop_times)
        else:
            return False
        
    def activate_load_bar_7(self, loop_times):
        if self.load_bars_active:
            self.load_bar_6.set_name("load-circle-inactive")
            self.load_bar_7.set_name("load-circle-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_8, loop_times)
        else:
            return False
        
    def activate_load_bar_8(self, loop_times):
        if self.load_bars_active:
            self.load_bar_7.set_name("load-circle-inactive")
            self.load_bar_8.set_name("load-circle-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_9, loop_times)
        else:
            return False
        
    def activate_load_bar_9(self, loop_times):
        if self.load_bars_active:
            self.load_bar_8.set_name("load-circle-inactive")
            self.load_bar_9.set_name("load-circle-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_10, loop_times)
        else:
            return False

    def activate_load_bar_10(self, loop_times):
        if self.load_bars_active:
            self.load_bar_9.set_name("load-circle-inactive")
            self.load_bar_10.set_name("load-circle-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_11, loop_times)
        else:
            return False

    def activate_load_bar_11(self, loop_times):
        if self.load_bars_active:
            self.load_bar_10.set_name("load-circle-inactive")
            self.load_bar_11.set_name("load-circle-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_12, loop_times)
        else:
            return False
        
    def activate_load_bar_12(self, loop_times):
        if self.load_bars_active:
            self.load_bar_11.set_name("load-circle-inactive")
            self.load_bar_12.set_name("load-circle-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_13, loop_times)
        else:
            return False
    
    def activate_load_bar_13(self, loop_times):
        if self.load_bars_active:
            self.load_bar_12.set_name("load-circle-inactive")
            self.load_bar_13.set_name("load-circle-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_14, loop_times)
        else:
            return False

    def activate_load_bar_14(self, loop_times):
        if self.load_bars_active:
            self.load_bar_13.set_name("load-circle-inactive")
            self.load_bar_14.set_name("load-circle-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_15, loop_times)
        else:
            return False

    def activate_load_bar_15(self, loop_times):
        if self.load_bars_active:
            self.load_bar_14.set_name("load-circle-inactive")
            self.load_bar_15.set_name("load-circle-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_16, loop_times)
        else:
            return False
        
    def activate_load_bar_16(self, loop_times):
        if self.load_bars_active:
            self.load_bar_15.set_name("load-circle-inactive")
            self.load_bar_16.set_name("load-circle-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_17, loop_times)
        else:
            return False

    def activate_load_bar_17(self, loop_times):
        if self.load_bars_active:
            self.load_bar_16.set_name("load-circle-inactive")
            self.load_bar_17.set_name("load-circle-active")
            GLib.timeout_add(self.load_speed, self.deactivate_load_bars, loop_times)
        else:
            return False
    
    def deactivate_load_bars(self, loop_times):
        if self.load_bars_active:
            self.load_bar_17.set_name("load-circle-inactive")
            if loop_times == 0:
                self.load_bars_active = False
                return False
            else:
                loop_times -= 1
                GLib.timeout_add(800, self.activate_load_bars, loop_times)
        else:
            return False

    def bluetooth_clicked(self, widget, event):
        if self.bluetooth_on:
            self.bluetooth_on = False
            self.resize(self.window_width, 10)
            self.set_size_request(self.window_width, 10)
            self.desc.set_text("Off")
            self.status_dot.set_name("status-dot-off")
            subprocess.run(["sudo", "systemctl",  "stop", "bluetooth"])
            self.icon_background_box.set_name("toggle-icon-background-disabled")
            self.icon.set_name("toggle-icon-disabled")
            self.load_bars_active = False
            self.main_box.show_all()
            self.load_bar_box.hide()
            self.list_main_box.hide()
            self.list_options_main_box.hide()
        else:
            self.bluetooth_on = True
            self.resize(self.window_width, self.window_height)
            self.set_size_request(self.window_width, self.window_height)
            self.status_dot.set_name("status-dot-inactive")
            subprocess.run(["sudo", "systemctl",  "start", "bluetooth"])
            self.icon_background_box.set_name("toggle-icon-background-enabled")
            self.icon.set_name("toggle-icon-enabled")
            self.main_box.show_all()
            self.update_ui_with_devices()

    def scan_clicked(self, widget, event):
        self.history_shown = False
        self.active_known_widget = None
        self.config_box.set_name("toggle-box-list-options-inactive")
        self.config_title.set_name("list-opitons-title-inactive")
        self.scan_box.set_name("toggle-box-list-options-active")
        self.scan_title.set_name("list-opitons-title-active")
        self.update_ui_with_devices()
        if self.no_devices:
            x, y = self.get_mouse_position()
            subprocess.run(f"xdotool mousemove {x} {y - 175}", shell = True)
        
    def history_clicked(self, widget, event):
        self.history_shown = True
        self.active_widget = None
        self.config_box.set_name("toggle-box-list-options-active")
        self.config_title.set_name("list-opitons-title-active")
        self.scan_box.set_name("toggle-box-list-options-inactive")
        self.scan_title.set_name("list-opitons-title-inactive")
        self.update_ui_with_known_devices()

    def get_bluetooth_on(self):
        try:
            bluetooth_state = subprocess.check_output("systemctl status bluetooth | grep Running", shell=True, stderr=subprocess.PIPE, text=True).strip()
            if "Running" in bluetooth_state:
                return True
            else:
                return False
        except subprocess.CalledProcessError as e:
            return False

    def on_device_clicked(self, widget, event, device):
        self.ignore_focus_lost = True
        self.active_widget = widget
        if device["CONNECTED"]:
            widget.get_parent().get_parent().set_name("list-obj-box-active-clicked")
        else:
            widget.get_parent().get_parent().set_name("list-obj-box-inactive-clicked")
        dialog = OptionWindow(self, self, device, widget)
        dialog.run()
        
    def known_device_clicked(self, widget, event, device_name):
        if self.active_known_widget:
            buttons = self.active_known_widget.get_parent().get_children()
            for child in buttons[1:]:
                self.active_known_widget.get_parent().remove(child)
            
            self.active_known_widget.get_parent().set_name("list-content-box-inactive")

            if self.active_known_widget == widget:
                self.active_known_widget = None
                return

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        connection_button = Gtk.Button()
        connection_button.connect("key-press-event", self.on_connect_clicked)
        button_box.pack_start(connection_button, True, True, 0)
        
        connection_button.set_label("Connect")
        connection_button.connect("button-press-event", self.on_connect_clicked, device_name)

        trust_button = Gtk.Button()
        button_box.pack_start(trust_button, True, True, 0)
        if device_name["device_name-TRUSTED"]:
            trust_button.set_label("Untrust")
            trust_button.connect("button-press-event", self.on_untrust_clicked, device_name)
        else:
            trust_button.set_label("Trust")
            trust_button.connect("button-press-event", self.on_trust_clicked, device_name)

        if device_name["device_name-KNOWN"]:
            remove_button = Gtk.Button(label = "Remove")
            remove_button.connect("button-press-event", self.on_remove_clicked, device_name)
            button_box.pack_start(remove_button, True, True, 0)
        
        widget.get_parent().set_name("list-content-box-active")
        widget.get_parent().pack_start(button_box, False, False, 0)     
        widget.get_parent().show_all()

        self.active_known_widget = widget
        return True
    
    def refresh_clicked(self, widget, event):
        self.update_ui_with_devices()
    
    def get_bluetooth_devices(self):
        with open('/home/jonalm/scripts/qtile/bar_menus/bluetooth/bluetooth_devices.json', 'r') as json_file:
            devices = json.load(json_file)
        return devices
    
    def get_known_devices(self):
        known_devices_output = subprocess.check_output("bluetoothctl devices", shell=True).decode("utf-8")
        if known_devices_output:
            lines = known_devices_output.splitlines()
            known_devices = []

            for line in lines:
                parts = line.split(" ", 2)
                device_name = parts[2]
                known_devices.append(device_name)
            
            return known_devices
    
    def get_trusted_devices(self):
        connected_devices_output = subprocess.check_output("bluetoothctl devices Trusted", shell=True).decode("utf-8")
        lines = connected_devices_output.splitlines()
        connected_devices = []
        if connected_devices_output:
            lines = connected_devices_output.splitlines()

            for line in lines:
                parts = line.split(" ", 2)
                parts.pop(0)
                device_addr = parts[0]

                connected_devices.append(device_addr)
                        
        return connected_devices
    
    def get_connected_devices(self):
        connected_devices_output = subprocess.check_output("bluetoothctl devices Connected", shell=True).decode("utf-8")
        lines = connected_devices_output.splitlines()
        connected_devices = []
        trusted_devices = self.get_trusted_devices()

        import pulsectl
        pulse = pulsectl.Pulse()
        sinks = pulse.sink_list()
        
        if connected_devices_output:
            lines = connected_devices_output.splitlines()

            for line in lines:
                parts = line.split(" ", 2)
                parts.pop(0)

                device_addr = parts[0]
                device_name = parts[1]
                icon = None
                battery = None

                for sink in sinks:
                    if device_name == sink.description:
                        icon = sink.proplist["device.icon_name"]
                        battery = sink.proplist["bluetooth.battery"]

                if device_addr == "default":
                    return

                trusted = False
                if trusted_devices:
                    if device_addr in trusted_devices:
                        trusted = True

                connected_devices.append({"DEVICE": device_name, "MAC-ADDR": device_addr, "CONNECTED": True, "DEVICE-KNOWN": True, "DEVICE-TRUSTED": trusted, "DEVICE-TYPE": icon, "BATTERY": battery})
                        
        return connected_devices
    
    def update_ui_with_devices(self):
        if not self.active_widget and self.bluetooth_on and not self.history_shown:
            self.status_dot.set_name("status-dot-list-update")
            GLib.timeout_add(300, self.restore_status_dot)

            for child in self.list_box.get_children():
                self.list_box.remove(child)

            devices = self.get_bluetooth_devices()
            connected_devices = self.get_connected_devices()
            if connected_devices:
                for connected_device in connected_devices:
                    for i, device in enumerate(devices):
                        if device["DEVICE"] == connected_device["DEVICE"]:
                            devices.pop(i) 
                    devices.append(connected_device)

            if not devices:
                if not self.load_bars_active:
                    self.main_box.show_all()
                    self.resize(self.window_width, 10)
                    self.set_size_request(self.window_width, 10)
                    self.list_main_box.hide()
                    self.desc.hide()
                    self.load_bars_active = True
                    self.activate_load_bars(3)
                    self.no_devices = True
                    return True
            else:
                self.resize(self.window_width, self.window_height)
                self.set_size_request(self.window_width, self.window_height)
                self.main_box.show_all()
                self.load_bar_box.hide()
                self.no_devices = False

            self.desc.set_text(f"{len(devices)} Available")

            devices.sort(key=lambda x: (not x["CONNECTED"], not x["DEVICE-KNOWN"]))

            for device in devices:
                row = Gtk.ListBoxRow()
                row.set_name("row")
                label = Gtk.Label()

                list_content_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

                list_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
                list_obj_icon_box = Gtk.EventBox()
                icon = Gtk.Label()
                
                device_type = device["DEVICE-TYPE"] 
                if device_type == "audio-headphones-bluetooth":
                    icon.set_name("list-icon-headphone")
                    icon.set_text("")
                elif device_type == "audio-card-pci":
                    icon.set_name("list-icon-speaker")
                    icon.set_text("")
                elif device_type == "audio-card-usb":
                    icon.set_name("list-icon-headphone")
                    icon.set_text("")
                else:
                    icon.set_name("list-icon-unknown")
                    icon.set_text("?")

                list_obj_battery_box = Gtk.EventBox()
                list_obj_battery_box.set_name("list-battery-box")
                battery = Gtk.Label()

                battery_percentage = device["BATTERY"]
                if battery_percentage:
                    battery.set_text(battery_percentage)
                    list_obj_icon_box.set_name("list-icon-box-if-battery")
                    if int(battery_percentage[:1]) <= 20:
                        battery.set_name("list-battery-under-20")
                    else:
                        battery.set_name("list-battery-over-20")
                else:
                    list_obj_icon_box.set_name("list-icon-box")

                list_obj_clickable_box = Gtk.EventBox()
                list_obj_clickable_box.connect("button-press-event", self.on_device_clicked, device)

                if device["CONNECTED"]:
                    label.set_name("list-obj")
                    list_content_main_box.set_name("list-obj-box-active")
                else:
                    list_content_main_box.set_name("list-obj-box-inactive")
                    label.set_name("list-obj")

                label.set_text(device["DEVICE"][:20])
                label.set_halign(Gtk.Align.START)
                
                list_obj_icon_box.add(icon)
                list_obj_clickable_box.add(label)

                list_content_box.pack_start(list_obj_icon_box, False, False, 0)
                if battery_percentage:
                    list_obj_battery_box.add(battery)
                    list_content_box.pack_start(list_obj_battery_box, False, False, 0)
                list_content_box.pack_start(list_obj_clickable_box, False, False, 0)
                
                list_content_main_box.pack_start(list_content_box, False, False, 0)
                
                row.add(list_content_main_box)
                self.list_box.add(row)

            self.list_box.show_all()

        return True
    
    def update_ui_with_known_devices(self):
        self.load_bars_active = False
        self.main_box.show_all()
        self.load_bar_box.hide()
        self.resize(self.window_width, self.window_height)
        self.set_size_request(self.window_width, self.window_height)
        
        for child in self.list_box.get_children():
            self.list_box.remove(child)

        devices = self.get_known_devices()

        self.desc.set_text(f"{len(devices)} Known")

        for device in devices:
            row = Gtk.ListBoxRow()
            row.set_name("row")
            label = Gtk.Label()

            list_content_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            list_content_main_box.set_name("list-obj-box-inactive")

            list_content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

            list_obj_clickable_box = Gtk.EventBox()
            list_obj_clickable_box.connect("button-press-event", self.on_device_clicked, device)

            label.set_name("list-obj")

            label.set_text(device[:20])
            label.set_halign(Gtk.Align.START)
            
            list_obj_clickable_box.add(label)
            list_content_box.pack_start(list_obj_clickable_box, False, False, 0)

            list_content_main_box.pack_start(list_content_box, False, False, 0)

            row.add(list_content_main_box)
            self.list_box.add(row)

        self.list_box.show_all()

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
        if keyval == Gdk.KEY_Escape:
            self.on_focus_out(widget, event)

    def handle_sigterm(self, signum, frame):
        self.exit_remove_pid() 

    def exit_remove_pid(self):
        try:
            if self.bluetooth_process.is_alive():
                self.bluetooth_process.terminate()
                self.bluetooth_process.join() 
            with open(self.pid_file, "r") as file:
                pid = int(file.read().strip())
            try:
                os.remove(self.pid_file)
                os.kill(pid, 15)
            except ProcessLookupError:
                pass
        finally:
            exit(0)

def scan_devices():
    subprocess.run("bluetoothctl --timeout 5 scan on", shell = True)
    output = subprocess.check_output("hcitool scan", shell = True).decode("utf-8")
    return output
    
def get_known_devices():
    known_devices_output = subprocess.check_output("bluetoothctl devices", shell=True).decode("utf-8")
    if known_devices_output:
        lines = known_devices_output.splitlines()
        known_devices = []

        for line in lines:
            parts = line.split(" ")
            device_addr = parts[1] 
            known_devices.append(device_addr)
        
        return known_devices

def get_trusted_devices():
    connected_devices_output = subprocess.check_output("bluetoothctl devices Trusted", shell=True).decode("utf-8")
    lines = connected_devices_output.splitlines()
    connected_devices = []
    if connected_devices_output:
        lines = connected_devices_output.splitlines()

        for line in lines:
            parts = line.split(" ", 2)
            parts.pop(0)

            device_addr = parts[0]

            connected_devices.append(device_addr)
                    
    return connected_devices

def get_bluetooth_on():
    try:
        bluetooth_state = subprocess.check_output("systemctl status bluetooth | grep Running", shell=True, stderr=subprocess.PIPE, text=True).strip()
        if "Running" in bluetooth_state:
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        return False
    
def bluetooth_process():
    while True:
        if get_bluetooth_on():
            bluetooth_output = scan_devices()
            known_devices = get_known_devices()
            trusted_devices = get_trusted_devices()
            if bluetooth_output:
                lines = bluetooth_output.splitlines()
                unique_devices = []

                for line in lines[1:]:
                    parts = line.split("\t", 2)
                    parts.pop(0)

                    device_name = parts[1]
                    device_addr = parts[0]

                    known = False
                    if known_devices:
                        if device_addr in known_devices:
                            known = True

                    trusted = False
                    if trusted_devices:
                        if device_addr in trusted_devices:
                            trusted = True
                    
                    if device_name != "n/a":
                        unique_devices.append({"DEVICE": device_name, "MAC-ADDR": device_addr, "CONNECTED": False, "DEVICE-KNOWN": known, "DEVICE-TRUSTED": trusted, "DEVICE-TYPE": None, "BATTERY": None})
            
            with open('/home/jonalm/scripts/qtile/bar_menus/bluetooth/bluetooth_devices.json', 'w') as json_file:
                json.dump(unique_devices, json_file, indent=2)
        else:
            time.sleep(4)

if __name__ == '__main__':
    pid_file = "/home/jonalm/scripts/qtile/bar_menus/bluetooth/bluetooth_menu_pid_file.pid"
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

            process = Process(target=bluetooth_process)
            process.start()
            
            dialog = BluetoothMenu(process)
            Gtk.main()
                    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        exit(0)