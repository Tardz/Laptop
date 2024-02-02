import gi
gi.require_version('Gtk', '3.0')
import subprocess
import os
from gi.repository import Gtk, Gdk, GLib
from multiprocessing import Process, Value
from Xlib import display 
from Xlib.ext import randr
from background_process import BackgroundProcess
import pulsectl
import signal
import time
import json
import sys

class OptionWindow(Gtk.Dialog):
    def __init__(self, parent, main_window, device, active_widget):
        super(OptionWindow, self).__init__(title="Device Options", transient_for=parent)
        self.main_window = main_window
        self.active_widget = active_widget
        self.device = device

        x, y = self.get_mouse_position()
        self.move(x, y)

        self.ignore_focus_lost = False
        self.load_speed = 300
        
        self.connect_process_successful = Value('b', False)
        self.connect_process = None 

        self.connect("focus-out-event", self.on_focus_out)
        self.connect("key-press-event", self.on_escape_press)

        self.content_area = self.get_content_area()
        self.content_area.get_style_context().add_class('root')

        connection_button = Gtk.Button()
        connection_button.get_style_context().add_class("buttons")
        self.content_area.pack_start(connection_button, True, True, 0)
        
        if self.device["CONNECTED"]:
            connection_button.set_label("Disconnect")
            connection_button.connect("activate", self.on_disconnect_clicked)

            connection_button.connect("button-press-event", self.on_disconnect_clicked)
            self.previouse_widget_in_use = True
        else:
            connection_button.set_label("Connect")
            connection_button.connect("activate", self.on_connect_clicked)
            connection_button.connect("button-press-event", self.on_connect_clicked)

        trust_button = Gtk.Button()
        trust_button.get_style_context().add_class("buttons")
        self.content_area.pack_start(trust_button, True, True, 0)

        if self.device["DEVICE-TRUSTED"]:
            trust_button.set_label("Untrust")
            trust_button.connect("activate", self.on_untrust_clicked)
            trust_button.connect("button-press-event", self.on_untrust_clicked)
        else:
            trust_button.set_label("Trust")
            trust_button.connect("activate", self.on_trust_clicked)
            trust_button.connect("button-press-event", self.on_trust_clicked)

        if self.device["DEVICE-KNOWN"]:
            remove_button = Gtk.Button(label = "Remove")
            remove_button.get_style_context().add_class("buttons")
            remove_button.connect("activate", self.on_remove_clicked)
            remove_button.set_name("buttons")
            remove_button.connect("button-press-event", self.on_remove_clicked)
            self.content_area.pack_start(remove_button, True, True, 0)
            self.set_size_request(130, 135)
        else:
            self.set_size_request(130, 90)

        self.show_all()

    def on_connect_clicked(self, widget=False, event=False, entry=False):
        for child in self.content_area.get_children():
            self.content_area.remove(child)

        self.ignore_focus_lost = True
        x, y = self.main_window.get_position()
        width, height = self.main_window.get_size()
        dialog_width, dialog_height = width - 80, 80
        self.resize(dialog_width, dialog_height)
        self.set_size_request(dialog_width, dialog_height)
        animation_window_x, animation_window_y = x + (width - dialog_width)/2, y + (height/3) 
        self.move(animation_window_x, animation_window_y)

        connect_animation_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
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

        self.device_icon = Gtk.Label()
        if "Bose" or "pods" in self.device["DEVICE"]:
            self.device_icon.set_text("")
        else:
            self.device_icon.set_text("")
        self.device_icon.get_style_context().add_class('connect-animation-icon')
        self.device_icon.set_name("connect-animation-inactive")

        connect_animation_box.pack_start(self.laptop_icon,   True, False, 0)
        connect_animation_box.pack_start(self.load_circle_1, True, False, 0)
        connect_animation_box.pack_start(self.load_circle_2, True, False, 0)
        connect_animation_box.pack_start(self.load_circle_3, True, False, 0)
        connect_animation_box.pack_start(self.device_icon,  True, False, 0)

        self.content_area.pack_start(connect_animation_box, True, False, 0)
        self.content_area.show_all()
        
        self.activate_load_circle_stage_1()
        self.connect_process = Process(target=self.connect_process_start)
        self.connect_process.start()

    def connect_process_start(self):
        device_addr = self.device["MAC-ADDR"]

        result = subprocess.call(f"bluetoothctl connect {device_addr}", shell=True)
        if result == 0:
            with self.connect_process_successful.get_lock():
                self.connect_process_successful.value = True
        else:
            time.sleep(4)
            self.connect_process_start()

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
        with self.connect_process_successful.get_lock():
            if self.connect_process_successful.value:
                self.terminate_connect_process()
                self.device_icon.set_name("connect-animation-active")
                GLib.timeout_add(self.load_speed, self.connection_successful_animation)
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
    
    def connection_successful_animation(self):
        self.laptop_icon.set_name("connect-animation-success")
        self.device_icon.set_name("connect-animation-success")
        self.load_circle_1.set_name("connect-animation-success")
        self.load_circle_2.set_name("connect-animation-success")
        self.load_circle_3.set_name("connect-animation-success")
        
        GLib.timeout_add(400, self.exit)
        return False

    def on_disconnect_clicked(self, widget=False, event=False, entry=False):
        device_addr = self.device["MAC-ADDR"]
        subprocess.call(f"bluetoothctl disconnect {device_addr}", shell=True)
        self.exit()

    def on_trust_clicked(self, widget=False, event=False, entry=False):
        device_addr = self.device["MAC-ADDR"]
        subprocess.call(f"bluetoothctl trust {device_addr}", shell=True)
        self.exit()

    def on_untrust_clicked(self, widget=False, event=False, entry=False):
        device_addr = self.device["MAC-ADDR"]
        subprocess.call(f"bluetoothctl untrust {device_addr}", shell=True)
        self.exit()

    def on_remove_clicked(self, widget=False, event=False, entry=False):
        device_addr = self.device["MAC-ADDR"]
        subprocess.call(f"bluetoothctl remove {device_addr}", shell=True)
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
        if self.connect_process and self.connect_process.is_alive():
            self.connect_process.terminate()
            self.connect_process.join()

        self.main_window.active_widget = None
        self.main_window.ignore_focus_lost = False
        
        if self.device["CONNECTED"]:
            self.active_widget.get_parent().get_parent().set_name("row-box-active")
        else: 
            self.active_widget.get_parent().get_parent().set_name("row-box-inactive")

        self.main_window.update_ui_with_devices()
        self.destroy()

class BluetoothMenu(Gtk.Window):
    def __init__(self, pid_file_path):
        Gtk.Window.__init__(self, title="Bluetooth menu")

        self.bluetooth_process_instance = BackgroundProcess()
        self.process = Process(target=self.bluetooth_process_instance.bluetooth_process)
        self.process.start()

        signal.signal(signal.SIGTERM, self.handle_sigterm)
        self.singal_file_path = os.path.expanduser("~/scripts/qtile/bar_menus/bluetooth/signal_data.txt")

        x, y = self.get_mouse_position()

        self.move(x, y)

        self.window_width = 350
        self.window_height = 350

        self.bluetooth_on = self.get_bluetooth_on()
        if self.bluetooth_on:
            self.set_size_request(self.window_width, self.window_height)
        else:
            self.set_size_request(self.window_width, 20)

        self.pid_file_path = pid_file_path
        self.hidden = False
        self.ignore_focus_lost = False
        self.previous_css_class = None
        self.active_widget = None
        self.previouse_widget_in_use = False
        self.active_known_widget = None
        self.load_bars_active = False
        self.load_speed = 40
        self.load_icon = ""
        self.no_devices = False
        self.known_shown = False

        self.set_name('root')

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.main_box.get_style_context().add_class("main")
        
        self.css()
        self.create_title() 
        self.initialize_loading_screen()
        self.create_list()
        self.create_list_options()

        self.connect("focus-out-event", self.on_focus_out)
        self.connect("key-press-event", self.on_escape_press)

        self.add(self.main_box)
        self.show_all()
        self.load_bar_box.hide()

        if not self.bluetooth_on:
            self.resize(self.window_width, 10)
            self.set_size_request(self.window_width, 10)
            self.list_box.hide()
            self.list_options_main_box.hide()

        self.update_ui_with_devices()

    def create_title(self):
        self.title_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        title_box.get_style_context().add_class("toggle-title-box")

        self.desc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.desc_box.get_style_context().add_class('toggle-desc-box')

        title = Gtk.Label() 
        title.get_style_context().add_class('toggle-title')
        title.set_text("Devices")
        title.set_halign(Gtk.Align.START)

        self.desc = Gtk.Label()
        self.desc.get_style_context().add_class('toggle-desc')
        self.desc.set_halign(Gtk.Align.START)
        if not self.bluetooth_on:
            self.desc.set_text("Off")

        left_box = Gtk.EventBox()
        left_box.set_name("toggle-left-box")

        self.icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        self.icon = Gtk.Label()
        self.icon.get_style_context().add_class('toggle-icon')
        self.icon.set_text("")
        self.icon.set_halign(Gtk.Align.START)

        if self.bluetooth_on:
            self.icon.set_name("toggle-icon-enabled")
        else:
            self.icon.set_name("toggle-icon-disabled")

        self.status_dot = Gtk.Label()
        self.status_dot.get_style_context().add_class('status-dot')
        self.status_dot.set_text("")
        self.status_dot.set_name("status-dot-inactive")
        self.status_dot.set_halign(Gtk.Align.END)
        
        self.icon_box.pack_start(self.icon, False, False, 0)
        left_box.add(self.icon_box)
        self.desc_box.pack_start(title, False, False, 0)
        self.desc_box.pack_start(self.desc, False, False, 0)
        title_box.pack_start(left_box, False, False, 0)
        title_box.pack_start(self.desc_box, False, False, 0)
        title_box.pack_start(self.status_dot, True, True, 0)

        self.title_main_box.pack_start(title_box, False, False, 0)
        
        left_box.connect("button-press-event", self.bluetooth_clicked)
        self.main_box.pack_start(self.title_main_box, False, False, 0)

    def create_list(self):
        self.list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.list_box.get_style_context().add_class('list-box')
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.get_style_context().add_class('none')
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC) 
        
        self.list = Gtk.ListBox()
        self.list.get_style_context().add_class('none')
        self.list.set_selection_mode(Gtk.SelectionMode.NONE)

        scrolled_window.add(self.list)  
        self.list_box.pack_start(scrolled_window, True, True, 0)

        self.update_devices_timeout = GLib.timeout_add(6000, self.update_ui_with_devices)
        self.main_box.pack_start(self.list_box, True, True, 0)

    def create_list_options(self):
        self.list_options_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.list_options_main_box.get_style_context().add_class("list-options-box")
        self.scan_box = Gtk.EventBox()
        self.scan_box.get_style_context().add_class("list-options")
        self.scan_box.set_name("list-options-active")
        self.scan_title = Gtk.Label()
        self.scan_title.get_style_context().add_class("list-options-title")
        self.scan_title.set_name("list-opitons-title-active")
        self.scan_title.set_text("")

        self.config_box = Gtk.EventBox()
        self.config_box.get_style_context().add_class("list-options")
        self.config_box.set_name("list-options-inactive")
        self.config_title = Gtk.Label()
        self.config_title.get_style_context().add_class("list-options-title")
        self.config_title.set_name("list-opitons-title-inactive")
        self.config_title.set_text("")

        self.scan_box.add(self.scan_title)
        self.config_box.add(self.config_title)

        self.list_options_main_box.pack_start(self.scan_box, True, True, 0)
        self.list_options_main_box.pack_start(self.config_box, True, True, 0)

        self.scan_box.connect("button-press-event", self.scan_clicked)
        self.config_box.connect("button-press-event", self.known_clicked)
        
        self.main_box.pack_start(self.list_options_main_box, False, False, 0)

    def initialize_loading_screen(self):
        self.load_bar_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.load_bar_box.get_style_context().add_class('load-box')

        self.load_bar_1 = Gtk.Label() 
        self.load_bar_1.get_style_context().add_class('load-bar')
        self.load_bar_1.set_name("load-bar-inactive")
        self.load_bar_1.set_text(self.load_icon)

        self.load_bar_2 = Gtk.Label() 
        self.load_bar_2.get_style_context().add_class('load-bar')
        self.load_bar_2.set_name("load-bar-inactive")
        self.load_bar_2.set_text(self.load_icon)
        
        self.load_bar_3 = Gtk.Label() 
        self.load_bar_3.get_style_context().add_class('load-bar')
        self.load_bar_3.set_name("load-bar-inactive")
        self.load_bar_3.set_text(self.load_icon)
        
        self.load_bar_4 = Gtk.Label() 
        self.load_bar_4.get_style_context().add_class('load-bar')
        self.load_bar_4.set_name("load-bar-inactive")
        self.load_bar_4.set_text(self.load_icon)

        self.load_bar_5 = Gtk.Label() 
        self.load_bar_5.get_style_context().add_class('load-bar')
        self.load_bar_5.set_name("load-bar-inactive")
        self.load_bar_5.set_text(self.load_icon)

        self.load_bar_6 = Gtk.Label() 
        self.load_bar_6.get_style_context().add_class('load-bar')
        self.load_bar_6.set_name("load-bar-inactive")
        self.load_bar_6.set_text(self.load_icon)
        
        self.load_bar_7 = Gtk.Label() 
        self.load_bar_7.get_style_context().add_class('load-bar')
        self.load_bar_7.set_name("load-bar-inactive")
        self.load_bar_7.set_text(self.load_icon)
        
        self.load_bar_8 = Gtk.Label() 
        self.load_bar_8.get_style_context().add_class('load-bar')
        self.load_bar_8.set_name("load-bar-inactive")
        self.load_bar_8.set_text(self.load_icon)

        self.load_bar_9 = Gtk.Label() 
        self.load_bar_9.get_style_context().add_class('load-bar')
        self.load_bar_9.set_name("load-bar-inactive")
        self.load_bar_9.set_text(self.load_icon)

        self.load_bar_10 = Gtk.Label() 
        self.load_bar_10.get_style_context().add_class('load-bar')
        self.load_bar_10.set_name("load-bar-inactive")
        self.load_bar_10.set_text(self.load_icon)
        
        self.load_bar_11 = Gtk.Label() 
        self.load_bar_11.get_style_context().add_class('load-bar')
        self.load_bar_11.set_name("load-bar-inactive")
        self.load_bar_11.set_text(self.load_icon)
        
        self.load_bar_12 = Gtk.Label() 
        self.load_bar_12.get_style_context().add_class('load-bar')
        self.load_bar_12.set_name("load-bar-inactive")
        self.load_bar_12.set_text(self.load_icon)

        self.load_bar_13 = Gtk.Label() 
        self.load_bar_13.get_style_context().add_class('load-bar')
        self.load_bar_13.set_name("load-bar-inactive")
        self.load_bar_13.set_text(self.load_icon)

        self.load_bar_14 = Gtk.Label() 
        self.load_bar_14.get_style_context().add_class('load-bar')
        self.load_bar_14.set_name("load-bar-inactive")
        self.load_bar_14.set_text(self.load_icon)
        
        self.load_bar_15 = Gtk.Label() 
        self.load_bar_15.get_style_context().add_class('load-bar')
        self.load_bar_15.set_name("load-bar-inactive")
        self.load_bar_15.set_text(self.load_icon)
        
        self.load_bar_16 = Gtk.Label() 
        self.load_bar_16.get_style_context().add_class('load-bar')
        self.load_bar_16.set_name("load-bar-inactive")
        self.load_bar_16.set_text(self.load_icon)

        self.load_bar_17 = Gtk.Label() 
        self.load_bar_17.get_style_context().add_class('load-bar')
        self.load_bar_17.set_name("load-bar-inactive")
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
        self.set_visual(visual)

    def restore_status_dot(self):
        self.status_dot.set_name("status-dot-inactive")
        return False
    
    def activate_load_bars(self, loop_times):
        if self.load_bars_active:
            self.load_bar_1.set_name("load-bar-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_2, loop_times)
        else:
            return False
        
    def activate_load_bar_2(self, loop_times):
        if self.load_bars_active:
            self.load_bar_1.set_name("load-bar-inactive")
            self.load_bar_2.set_name("load-bar-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_3, loop_times)
        else:
            return False
        
    def activate_load_bar_3(self, loop_times):
        if self.load_bars_active:
            self.load_bar_2.set_name("load-bar-inactive")
            self.load_bar_3.set_name("load-bar-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_4, loop_times)
        else:
            return False
        
    def activate_load_bar_4(self, loop_times):
        if self.load_bars_active:
            self.load_bar_3.set_name("load-bar-inactive")
            self.load_bar_4.set_name("load-bar-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_5, loop_times)
        else:
            return False
        
    def activate_load_bar_5(self, loop_times):
        if self.load_bars_active:
            self.load_bar_4.set_name("load-bar-inactive")
            self.load_bar_5.set_name("load-bar-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_6, loop_times)
        else:
            return False
        
    def activate_load_bar_6(self, loop_times):
        if self.load_bars_active:
            self.load_bar_5.set_name("load-bar-inactive")
            self.load_bar_6.set_name("load-bar-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_7, loop_times)
        else:
            return False
        
    def activate_load_bar_7(self, loop_times):
        if self.load_bars_active:
            self.load_bar_6.set_name("load-bar-inactive")
            self.load_bar_7.set_name("load-bar-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_8, loop_times)
        else:
            return False
        
    def activate_load_bar_8(self, loop_times):
        if self.load_bars_active:
            self.load_bar_7.set_name("load-bar-inactive")
            self.load_bar_8.set_name("load-bar-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_9, loop_times)
        else:
            return False
        
    def activate_load_bar_9(self, loop_times):
        if self.load_bars_active:
            self.load_bar_8.set_name("load-bar-inactive")
            self.load_bar_9.set_name("load-bar-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_10, loop_times)
        else:
            return False

    def activate_load_bar_10(self, loop_times):
        if self.load_bars_active:
            self.load_bar_9.set_name("load-bar-inactive")
            self.load_bar_10.set_name("load-bar-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_11, loop_times)
        else:
            return False

    def activate_load_bar_11(self, loop_times):
        if self.load_bars_active:
            self.load_bar_10.set_name("load-bar-inactive")
            self.load_bar_11.set_name("load-bar-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_12, loop_times)
        else:
            return False
        
    def activate_load_bar_12(self, loop_times):
        if self.load_bars_active:
            self.load_bar_11.set_name("load-bar-inactive")
            self.load_bar_12.set_name("load-bar-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_13, loop_times)
        else:
            return False
    
    def activate_load_bar_13(self, loop_times):
        if self.load_bars_active:
            self.load_bar_12.set_name("load-bar-inactive")
            self.load_bar_13.set_name("load-bar-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_14, loop_times)
        else:
            return False

    def activate_load_bar_14(self, loop_times):
        if self.load_bars_active:
            self.load_bar_13.set_name("load-bar-inactive")
            self.load_bar_14.set_name("load-bar-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_15, loop_times)
        else:
            return False

    def activate_load_bar_15(self, loop_times):
        if self.load_bars_active:
            self.load_bar_14.set_name("load-bar-inactive")
            self.load_bar_15.set_name("load-bar-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_16, loop_times)
        else:
            return False
        
    def activate_load_bar_16(self, loop_times):
        if self.load_bars_active:
            self.load_bar_15.set_name("load-bar-inactive")
            self.load_bar_16.set_name("load-bar-active")
            GLib.timeout_add(self.load_speed, self.activate_load_bar_17, loop_times)
        else:
            return False

    def activate_load_bar_17(self, loop_times):
        if self.load_bars_active:
            self.load_bar_16.set_name("load-bar-inactive")
            self.load_bar_17.set_name("load-bar-active")
            GLib.timeout_add(self.load_speed, self.deactivate_load_bars, loop_times)
        else:
            return False
    
    def deactivate_load_bars(self, loop_times):
        if self.load_bars_active:
            self.load_bar_17.set_name("load-bar-inactive")
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
            off_result = subprocess.call(["sudo", "systemctl",  "stop", "bluetooth"])
            if off_result == 0:
                self.bluetooth_on = False
                
                self.resize(self.window_width, 10)
                self.set_size_request(self.window_width, 10)
                
                self.desc.set_text("Off")
                self.status_dot.set_name("status-dot-off")
                self.load_bars_active = False
                
                self.icon.set_name("toggle-icon-disabled")
                
                self.main_box.show_all()
                self.load_bar_box.hide()
                self.list_box.hide()
                self.list_options_main_box.hide()
        else:
            on_result = subprocess.call(["sudo", "systemctl",  "start", "bluetooth"])
            if on_result == 0:
                self.bluetooth_on = True
                
                self.status_dot.set_name("status-dot-inactive")
                
                self.icon.set_name("toggle-icon-enabled")
                
                self.main_box.show_all()
                if self.known_shown:
                    self.update_ui_with_devices(True)
                else:
                    self.update_ui_with_devices(False)

    def scan_clicked(self, widget, event):
        self.known_shown = False
        self.active_known_widget = None
        self.config_box.set_name("list-options-inactive")
        self.config_title.set_name("list-opitons-title-inactive")
        self.scan_box.set_name("list-options-active")
        self.scan_title.set_name("list-opitons-title-active")
        self.update_ui_with_devices()
        if self.no_devices:
            x, y = self.get_mouse_position()
            subprocess.run(f"xdotool mousemove {x} {y - 175}", shell = True)
        
    def known_clicked(self, widget, event):
        self.active_widget = None
        self.config_box.set_name("list-options-active")
        self.config_title.set_name("list-opitons-title-active")
        self.scan_box.set_name("list-options-inactive")
        self.scan_title.set_name("list-opitons-title-inactive")
        self.update_ui_with_devices(True)
        if self.no_devices:
            x, y = self.get_mouse_position()
            subprocess.run(f"xdotool mousemove {x} {y - 175}", shell = True)

    def get_bluetooth_on(self):
        try:
            bluetooth_state = subprocess.check_output("systemctl status bluetooth | grep Running", shell=True, stderr=subprocess.PIPE, text=True).strip()
            if "Running" in bluetooth_state:
                return True
            else:
                return False
        except subprocess.CalledProcessError as e:
            return False

    def on_device_clicked(self, widget, event=False, device=False):
        self.ignore_focus_lost = True
        self.active_widget = widget
        widget.get_parent().get_parent().set_name("row-box-clicked")
        dialog = OptionWindow(self, self, device, widget)
        dialog.run()

    def on_device_pressed(self, entry, widget, device):
        self.on_device_clicked(widget=widget, device=device)

    def get_bluetooth_devices(self):
        with open('/home/jonalm/scripts/qtile/bar_menus/bluetooth/bluetooth_devices.json', 'r') as json_file:
            devices = json.load(json_file)
        return devices
    
    def get_known_devices(self):
        known_devices_output = subprocess.check_output("bluetoothctl devices", shell=True).decode("utf-8")
        known_devices = []

        if known_devices_output:
            lines = known_devices_output.splitlines()

            for line in lines:
                parts = line.split(" ", 2)
                parts.pop(0)
                device_addr = parts[0]
                known_devices.append(device_addr)
            
        return known_devices
    
    def get_trusted_devices(self):
        trusted_devices_output = subprocess.check_output("bluetoothctl devices Trusted", shell=True).decode("utf-8")
        trusted_devices = []

        if trusted_devices_output:
            lines = trusted_devices_output.splitlines()

            for line in lines:
                parts = line.split(" ", 2)
                parts.pop(0)
                device_addr = parts[0]

                trusted_devices.append(device_addr)
                        
        return trusted_devices
    
    def get_connected_devices(self):
        connected_devices_output = subprocess.check_output("bluetoothctl devices Connected", shell=True).decode("utf-8")
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
    
    def get_connected_devices_with_names(self):
        connected_devices_output = subprocess.check_output("bluetoothctl devices Connected", shell=True).decode("utf-8")
        lines = connected_devices_output.splitlines()
        connected_devices = []

        if connected_devices_output:
            lines = connected_devices_output.splitlines()

            for line in lines:
                parts = line.split(" ", 2)
                parts.pop(0)
                device_addr = parts[0]
                device_name = parts[1]

                connected_devices.append({"DEVICE": device_name, "MAC-ADDR": device_addr})
                        
        return connected_devices
        
    def get_known_devices_with_names(self):
        known_devices_output = subprocess.check_output("bluetoothctl devices", shell=True).decode("utf-8")
        lines = known_devices_output.splitlines()
        known_devices = []

        if known_devices_output:
            lines = known_devices_output.splitlines()

            for line in lines:
                parts = line.split(" ", 2)
                parts.pop(0)
                device_addr = parts[0]
                device_name = parts[1]

                known_devices.append({"DEVICE": device_name, "MAC-ADDR": device_addr})
                        
        return known_devices
    
    def get_devices(self, get_known):
            devices = []
            connected_devices = self.get_connected_devices()
            trusted_devices = self.get_trusted_devices()
            known_devices = self.get_known_devices()
            
            pulse = pulsectl.Pulse()
            sinks = pulse.sink_list()

            complete_devices = []
            if not get_known:
                devices = self.get_bluetooth_devices()
                for device in devices:
                    icon = None
                    battery = None

                    for sink in sinks:
                        if device["DEVICE"] == sink.description:
                            try:
                                icon = sink.proplist["device.icon_name"]
                                battery = sink.proplist["bluetooth.battery"].replace("%", "")
                            except:
                                print("Could not access bluetooth.battery or device.icon_name")

                    complete_device = {
                        "DEVICE": device["DEVICE"], 
                        "MAC-ADDR": device["MAC-ADDR"], 
                        "CONNECTED": device["MAC-ADDR"] in connected_devices, 
                        "DEVICE-KNOWN": device["MAC-ADDR"] in known_devices, 
                        "DEVICE-TRUSTED": device["MAC-ADDR"] in trusted_devices, 
                        "DEVICE-TYPE": icon, 
                        "BATTERY": battery
                    }

                    complete_devices.append(complete_device)
            else:
                devices = self.get_known_devices_with_names()
                for device in devices:
                    icon = None
                    battery = None

                    for sink in sinks:
                        if device["DEVICE"] == sink.description:
                            try:
                                icon = sink.proplist["device.icon_name"]
                                battery = sink.proplist["bluetooth.battery"].replace("%", "")
                            except:
                                print("Could not access bluetooth.battery or device.icon_name")

                    complete_device = {
                        "DEVICE": device["DEVICE"], 
                        "MAC-ADDR": device["MAC-ADDR"], 
                        "CONNECTED": device["MAC-ADDR"] in connected_devices, 
                        "DEVICE-KNOWN": True, 
                        "DEVICE-TRUSTED": device["MAC-ADDR"] in trusted_devices, 
                        "DEVICE-TYPE": icon, 
                        "BATTERY": battery
                    }

                    if complete_device["DEVICE-KNOWN"]:
                        complete_devices.append(complete_device)

            for connected_device in self.get_connected_devices_with_names():
                already_exists = False
                for main_device in devices:
                    if connected_device["MAC-ADDR"] == main_device["MAC-ADDR"]:
                        already_exists = True

                icon = None
                battery = None

                for sink in sinks:
                    if connected_device["DEVICE"] == sink.description:
                        try:
                            icon = sink.proplist["device.icon_name"]
                            battery = sink.proplist["bluetooth.battery"].replace("%", "")
                        except:
                            print("Could not access bluetooth.battery or device.icon_name")
                
                if not already_exists:
                    complete_devices.append({
                        "DEVICE": connected_device["DEVICE"], 
                        "MAC-ADDR": connected_device["MAC-ADDR"], 
                        "CONNECTED": True, 
                        "DEVICE-KNOWN": connected_device["MAC-ADDR"] in known_devices, 
                        "DEVICE-TRUSTED": connected_device["MAC-ADDR"] in trusted_devices, 
                        "DEVICE-TYPE": icon, 
                        "BATTERY": battery
                    })

            
            complete_devices.sort(key=lambda x: (not x["CONNECTED"], not x["DEVICE-KNOWN"]))
            pulse.close()
            return complete_devices

    def update_ui_with_devices(self, get_known=False):
        if not self.active_widget and self.bluetooth_on and not self.known_shown:
            if get_known:
                self.known_shown = True

            self.status_dot.set_name("status-dot-list-update")
            GLib.timeout_add(300, self.restore_status_dot)

            devices = self.get_devices(get_known)

            for child in self.list.get_children():
                self.list.remove(child)

            if not devices:
                self.main_box.show_all()
                self.resize(self.window_width, 10)
                self.set_size_request(self.window_width, 10)
                self.list_box.hide()
                if not self.load_bars_active and not get_known:
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

            if not self.load_bars_active:
                self.desc.show()
                self.desc.set_text(f"{len(devices)} Available")

            for device in devices:
                row = Gtk.ListBoxRow()
                row.get_style_context().add_class('list-row')

                row_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
                row_box.get_style_context().add_class('row-box')

                icon_box = Gtk.EventBox()
                icon = Gtk.Label()
                icon.get_style_context().add_class('list-icon')

                name_box = Gtk.EventBox()
                name_box.connect("button-press-event", self.on_device_clicked, device)
                name = Gtk.Label()
                name.get_style_context().add_class('list-name')
                name.set_text(device["DEVICE"][:20])
                name.set_halign(Gtk.Align.START)

                device_info_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
                
                battery_box = Gtk.EventBox()
                battery_box.get_style_context().add_class("list-battery-box")
                battery = Gtk.Label()
                battery.get_style_context().add_class("list-battery")

                device_type = device["DEVICE-TYPE"] 
                if device_type == "audio-headphones-bluetooth":
                    icon.set_text("")
                    if device["CONNECTED"]:
                        icon.set_name("list-icon-headphone-active")
                    else:
                        icon.set_name("list-icon-headphone-inactive")
                elif device_type == "audio-card-pci":
                    icon.set_text("")
                    if device["CONNECTED"]:
                        icon.set_name("list-icon-speaker-active")
                    else:
                        icon.set_name("list-icon-speaker-inactive")
                elif device_type == "audio-card-usb":
                    icon.set_text("")
                    if device["CONNECTED"]:
                        icon.set_name("list-icon-headphone-active")
                    else:
                        icon.set_name("list-icon-headphone-inactive")
                else:
                    icon.set_text("?")
                    if device["CONNECTED"]:
                        icon.set_name("list-icon-unknown-active")
                    else:
                        icon.set_name("list-icon-unknown-inactive")

                battery_percentage = device["BATTERY"]
                if battery_percentage:
                    battery.set_text(battery_percentage + "%")
                    if int(battery_percentage) <= 20:
                        battery.set_name("list-battery-under-20")
                    else:
                        battery.set_name("list-battery-over-20")
                else:
                    icon_box.set_name("list-icon-box")

                if device["CONNECTED"]:
                    row.set_name("row-box-active")
                else:
                    row.set_name("row-box-inactive")
                
                icon_box.add(icon)
                name_box.add(name)

                device_info_box.pack_start(icon_box, False, False, 0)
                if battery_percentage:
                    # icon_box.set_name('list-icon-box-with-info')
                    battery_box.add(battery)
                    device_info_box.pack_start(battery_box, False, False, 0)
                device_info_box.pack_start(name_box, False, False, 0)
                
                row_box.pack_start(device_info_box, False, False, 0)
                
                row.add(row_box)
                row.connect("activate", self.on_device_clicked, name_box, device)
                self.list.add(row)

            self.list.show_all()  

        return True
    
    def get_mouse_position(self):
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
        if not self.ignore_focus_lost:
            self.hide_menu()

    def on_escape_press(self, widget, event):
        keyval = event.keyval
        if keyval == Gdk.KEY_Escape:
            self.on_focus_out(widget, event)

    def handle_sigterm(self, signum, frame):
        with open(self.singal_file_path, "r") as file:
            signal_arg = file.read()
            with open(self.singal_file_path, "w") as file:
                file.write("")

            if signal_arg == "hide":
                self.hide_menu()
            elif signal_arg == "kill":
                GLib.idle_add(Gtk.main_quit)  

    def hide_menu(self):
        try:
            if self.hidden:
                # self.process = Process(target=self.bluetooth_process_instance.bluetooth_process)
                # self.process.start()
                self.update_devices_timeout = GLib.timeout_add(6000, self.update_ui_with_devices)
                self.ignore_focus_lost = False
                self.hidden = False
                self.show()
            else:
                # if self.process.is_alive():
                #     self.process.terminate()
                #     self.process.join() 
                    
                GLib.source_remove(self.update_devices_timeout)

                self.ignore_focus_lost = True
                self.hidden = True
                subprocess.run("qtile cmd-obj -o widget bluetoothicon -f unclick", shell=True)
                self.hide()

        except Exception as e:
            print(f"Error occurred: {e}")

def write_pid_to_settings_data(pid, json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data['bluetooth_menu_pid'] = pid

    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

    subprocess.run("qtile cmd-obj -o widget bluetoothicon -f update_menu_pid", shell=True)

def remove_pid_from_settings_data(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data['bluetooth_menu_pid'] = None

    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

    subprocess.run("qtile cmd-obj -o widget bluetoothicon -f update_menu_pid", shell=True)

if __name__ == '__main__':
    pid_file_path = os.path.expanduser("~/scripts/qtile/bar_menus/bluetooth/bluetooth_menu_pid_file.pid")
    json_file_path = os.path.expanduser("~/settings_data/processes.json")
    dialog = None

    try:
        if not os.path.isfile(pid_file_path):
            pid = os.getpid()
            write_pid_to_settings_data(pid, json_file_path)
            
            with open(pid_file_path, "w") as file:
                file.write(str(pid))
            
            dialog = BluetoothMenu(pid_file_path)
            Gtk.main()
        else:
            print("Another instance of this menu is already active.")
                    
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if dialog:
            dialog.destroy()
            remove_pid_from_settings_data(json_file_path)
            os.remove(pid_file_path)
        sys.exit(0)
