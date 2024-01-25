import gi
gi.require_version('Gtk', '3.0')

from multiprocessing import Value
from gi.repository import Gtk, Gdk
from Xlib import display
import os

class OptionWindow(Gtk.Window):
    def __init__(self, main_window, network, active_widget):
        Gtk.Window.__init__(self, title="Network Options")
        self.main_window = main_window
        self.active_widget = active_widget
        self.network = network
        self.event_handler = main_window.parent.event_handler

        # if self.main_window.history_shown:
        #     self.set_size_request(130, 45)
        # else:
        # self.set_size_request(10, 10)
        # self.set_default_size(10, 20)
        self.set_default_size(20, 30) 

        x, y = self.get_mouse_position()
        self.move(x, y)

        self.ignore_focus_lost = False
        self.load_speed = 300
        
        self.wrong_password = Value('b', False)
        self.connect_process_successful = Value('b', False)
        self.connect_process = None 
        self.ping_process_successful = Value('b', False)
        self.ping_process = None 

        self.connect("focus-out-event", self.event_handler.on_focus_out, self)
        self.connect("key-press-event", self.event_handler.on_escape_press, self)

        self.set_name("root")
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.main_box.get_style_context().add_class("main")

        connection_button_box = Gtk.EventBox()
        connection_button_box.get_style_context().add_class('network-option-box')
        connection_button_text = Gtk.Label()
        connection_button_text.set_text("Connect")
        connection_button_box.add(connection_button_text)

        if not self.main_window.history_shown:
            self.main_box.pack_start(connection_button_box, True, True, 0)
        
        password_entry = Gtk.Entry()
        password_entry.get_style_context().add_class('buttons')

        if self.network["KNOWN"]:
            remove_button_box = Gtk.EventBox()
            remove_button_box.get_style_context().add_class('network-option-box')
            remove_button_text = Gtk.Label()
            remove_button_text.set_text("Remove")
            remove_button_box.add(remove_button_text)

            remove_button_box.connect("button-press-event", self.event_handler.on_remove_clicked)
            remove_button_box.connect("key-press-event", self.event_handler.on_remove_clicked)

            self.main_box.pack_start(remove_button_box, True, True, 0)
        else:
            password_entry.set_placeholder_text("Password")
            self.main_box.pack_start(password_entry, True, True, 0)
        
        if self.network["CONNECTED"]:
            connection_button_text.set_text("Disconnect")
            connection_button_box.connect("button-press-event", self.event_handler.on_disconnect_clicked)
            connection_button_box.connect("key-press-event", self.event_handler.on_disconnect_clicked)
            self.main_window.previous_network_in_use = True
        else:
            connection_button_text.set_text("Connect")
            if self.network["KNOWN"]:
                connection_button_box.connect("button-press-event", self.event_handler.on_connect_clicked, self.main_window)
                connection_button_box.connect("key-press-event", self.event_handler.on_connect_clicked, self.main_window)
                password_entry.connect("key-press-event", self.event_handler.on_password_pressed)
            else:
                connection_button_box.connect("button-press-event", self.event_handler.on_connect_clicked, password_entry, self.main_window)
                connection_button_box.connect("key-press-event", self.event_handler.on_password_pressed, password_entry)
                password_entry.connect("key-press-event", self.event_handler.on_password_pressed, password_entry)
                password_entry.grab_focus()

        self.setup_animation()
        self.add(self.main_box)
        self.show_all()
        self.connect_animation_box.hide()

    def css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        provider.load_from_path(os.path.expanduser("~/scripts/qtile/bar_menus/wifi/css/wifi_menu_styles.css"))
        visual = screen.get_rgba_visual()
        self.set_visual(visual)

    def setup_animation(self):
        self.connect_animation_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.connect_animation_box.get_style_context().add_class('connect-animation-box')

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

        self.connect_animation_box.pack_start(self.laptop_icon,   True, False, 0)
        self.connect_animation_box.pack_start(self.load_circle_1, True, False, 0)
        self.connect_animation_box.pack_start(self.load_circle_2, True, False, 0)
        self.connect_animation_box.pack_start(self.load_circle_3, True, False, 0)
        self.connect_animation_box.pack_start(self.network_icon,  True, False, 0)
        self.connect_animation_box.pack_start(self.load_circle_4, True, False, 0)
        self.connect_animation_box.pack_start(self.load_circle_5, True, False, 0)
        self.connect_animation_box.pack_start(self.load_circle_6, True, False, 0)
        self.connect_animation_box.pack_start(self.internet_icon, True, False, 0)

        self.main_box.pack_start(self.connect_animation_box, True, False, 0)
    
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
            self.active_widget.get_parent().get_parent().set_name("row-box-active")
        else: 
            self.active_widget.get_parent().get_parent().set_name("row-box-inactive")

        self.main_window.update_list_with_networks(scan_offline=True)
        self.destroy()