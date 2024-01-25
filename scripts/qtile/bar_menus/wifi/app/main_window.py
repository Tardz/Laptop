import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, GLib
from Xlib.ext import randr
from Xlib import display
import signal
import os

class MainWindow(Gtk.Window):
    def __init__(self, parent):
        Gtk.Window.__init__(self, title="Networks Menu")
        self.parent = parent
        self.wifi_process = self.parent.wifi_process
        self.network_processing = self.parent.network_processing
        self.event_handler = parent.event_handler

        signal.signal(
            signal.SIGTERM, 
            lambda signum, frame: 
            self.event_handler.handle_sigterm(signum, frame, self)
            )
        
        x, y = self.calculate_window_position()
        self.move(x, y)

        self.window_width = 340
        self.window_height = 400

        self.wifi_on = self.network_processing.get_wifi_on()
        if self.wifi_on:
            self.set_size_request(self.window_width, self.window_height)
        else:
            self.set_size_request(self.window_width, 10)

        self.ignore_focus_lost = False
        self.active_widget = None
        self.history_shown = False
        self.skip_update = False

        self.set_name('root')
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.main_box.get_style_context().add_class("main")
        self.add(self.main_box)   

        self.css()
        self.create_title()
        self.create_list()
        self.create_list_options()

        self.connect("focus-out-event", self.event_handler.on_focus_out, self)
        self.connect("key-press-event", self.event_handler.on_escape_press, self)

        self.show_all()

        if not self.wifi_on:
            self.resize(self.window_width, 10)
            self.set_size_request(self.window_width, 10)
            self.list_box.hide()
            self.list_options_main_box.hide()

    def css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        provider.load_from_path(os.path.expanduser("~/scripts/qtile/bar_menus/wifi/css/wifi_menu_styles.css"))
        visual = screen.get_rgba_visual()
        self.set_visual(visual)

    def create_title(self):
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        title_box.get_style_context().add_class('toggle-title-box')

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
        icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        self.icon = Gtk.Label()
        self.icon.get_style_context().add_class('toggle-icon')
        self.icon.set_text("")
        self.icon.set_halign(Gtk.Align.START)

        if self.wifi_on:
            self.icon.set_name("toggle-icon-enabled")
        else:
            self.icon.set_name("toggle-icon-disabled")

        self.status_dot = Gtk.Label()
        self.status_dot.get_style_context().add_class('status-dot')
        self.status_dot.set_text("")
        if self.wifi_on:
            self.status_dot.set_name("status-dot-inactive")
        else:
            self.status_dot.set_name("status-dot-off")
        self.status_dot.set_halign(Gtk.Align.END)

        icon_box.pack_start(self.icon, False, False, 0)
        left_box.add(icon_box)
        desc_box.pack_start(title, False, False, 0)
        desc_box.pack_start(self.desc, False, False, 0)
        title_box.pack_start(left_box, False, False, 0)
        title_box.pack_start(desc_box, False, False, 0)
        title_box.pack_start(self.status_dot, True, True, 0)

        left_box.connect("button-press-event", self.event_handler.wifi_clicked, self)
        self.main_box.pack_start(title_box, False, False, 0)

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

        self.update_list_with_networks()
        GLib.timeout_add(7000, self.update_list_with_networks)
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

        self.history_box = Gtk.EventBox()
        self.history_box.get_style_context().add_class("list-options")
        self.history_box.set_name("list-options-inactive")
        self.config_title = Gtk.Label()
        self.config_title.get_style_context().add_class("list-options-title")
        self.config_title.set_name("list-opitons-title-inactive")
        self.config_title.set_text("")

        self.scan_box.add(self.scan_title)
        self.history_box.add(self.config_title)

        self.list_options_main_box.pack_start(self.scan_box, True, True, 0)
        self.list_options_main_box.pack_start(self.history_box, True, True, 0)

        self.scan_box.connect("button-press-event", self.event_handler.scan_clicked, self)
        self.history_box.connect("button-press-event", self.event_handler.history_clicked, self)
        self.main_box.pack_start(self.list_options_main_box, False, False, 0)

    def restore_status_dot(self):
        self.status_dot.set_name("status-dot-inactive")
        return False

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
                networks = self.network_processing.get_networks_offline()
                self.skip_update = True
            elif get_known:
                networks = self.network_processing.get_known_networks()
                print(networks)
            else:
                networks = self.network_processing.get_networks()

            if not networks:
                return True
            
            self.desc.set_text(f"{len(networks)} Available")
            
            for child in self.list.get_children():
                self.list.remove(child)

            for network in networks:
                row = Gtk.ListBoxRow()
                row.get_style_context().add_class('list-row')

                row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
                row_box.get_style_context().add_class('row-box')

                icon_box = Gtk.EventBox()
                icon = Gtk.Label()
                icon.get_style_context().add_class('list-icon')

                name_box = Gtk.EventBox()
                name_box.connect("button-press-event", self.event_handler.on_network_clicked, self, network)
                name = Gtk.Label()
                name.get_style_context().add_class('list-name')
                name.set_text(network["SSID"][:15])
                name.set_halign(Gtk.Align.START)

                if network["CONNECTED"]:
                    row_box.set_name("row-box-active")
                    row.set_name("list-row-connected")
                else:
                    row_box.set_name("row-box-inactive")
                    row.set_name("list-row-disconnected")

                if not get_known:
                    icon.set_name("list-icon")
                    icon.set_text(network["STRENGTH"])
                    icon_box.add(icon)
                    row_box.pack_start(icon_box, False, False, 0)
                
                name_box.add(name)
                row_box.pack_start(name_box, False, False, 0)

                if network["KNOWN"] and not get_known:
                    known_icon = Gtk.Label()
                    known_icon.set_halign(Gtk.Align.END)
                    known_icon.get_style_context().add_class('known-icon')
                    if network["CONNECTED"]:
                        known_icon.set_name("known-icon-active")
                    else:
                        known_icon.set_name("known-icon-inactive")
                    known_icon.set_text("")
                    row_box.pack_start(known_icon, True, True, 0)
                    
                row.add(row_box)
                row.connect("activate", self.event_handler.on_network_pressed, self, name_box, network)
                self.list.add(row)

            self.add_test_networks(4)
            self.list.show_all()

        return True
    
    def add_test_networks(self, n):
        for i in range(n):
            row = Gtk.ListBoxRow()
            row.get_style_context().add_class('list-row')

            name = Gtk.Label()
            name.get_style_context().add_class('list-name')
            name.set_text(f"Test network {i}")
            name.set_halign(Gtk.Align.START)

            list_content_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            list_content_main_box.get_style_context().add_class('row-box')

            list_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

            list_obj_icon_box = Gtk.EventBox()
            list_obj_icon_box.get_style_context().add_class('list-icon-box')
            icon = Gtk.Label()
            icon.get_style_context().add_class('list-icon')

            list_obj_clickable_box = Gtk.EventBox()

            list_content_main_box.set_name("row-box-inactive")

            icon.set_name("list-icon")
            icon.set_text("▂▄▆_")
            list_obj_icon_box.add(icon)
            list_content_box.pack_start(list_obj_icon_box, False, False, 0)
            
            list_obj_clickable_box.add(name)
            list_content_box.pack_start(list_obj_clickable_box, False, False, 0)

            list_content_main_box.pack_start(list_content_box, False, False, 0)
            
            row.add(list_content_main_box)
            self.list.add(row)

    def calculate_window_position(self):
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

    def exit(self):
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