import gi
gi.require_version('Gtk', '3.0')
import subprocess
import os
from gi.repository import Gtk, Gdk, GLib
import time
import pulsectl
import json

class VolumeMenu(Gtk.Dialog):
    def __init__(self):
        self.pid_file = "/home/jonalm/scripts/qtile/bar_menus/volume/volume_menu_pid_file.pid"
        Gtk.Dialog.__init__(self, "Sound Control", None, 0)

        x, y = self.get_mouse_position()

        if x and y:
            self.move(x - 160, 5)

        self.window_width = 330
        self.window_height = 400
        self.set_size_request(self.window_width, self.window_height)

        self.sound_on = self.get_sound_on()
        self.ignore_focus_lost = False
        self.active_widget = None
        self.previous_network_in_use = False
        self.history_shown = False
        self.active_known_widget = None

        self.content_area = self.get_content_area()
        self.content_area.set_name("content-area")
        self.set_name("root")

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

        if not self.sound_on:
            self.resize(self.window_width, 10)
            self.set_size_request(self.window_width, 10)
            self.list_main_box.hide()
            self.list_options_main_box.hide()

    def title(self):
        self.title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.title_box.set_name("toggle-box")

        desc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        desc_box.set_name("toggle-desc-box")

        title = Gtk.Label()
        title.set_text("Volume Outputs")
        title.set_name("toggle-title")
        title.set_halign(Gtk.Align.START)

        self.desc = Gtk.Label()
        self.desc.set_name("toggle-desc")
        self.desc.set_halign(Gtk.Align.START)

        left_box = Gtk.EventBox()
        left_box.set_name("toggle-left-box")

        self.icon_background_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        self.icon = Gtk.Label()
        self.icon.set_text("")
        self.icon.set_halign(Gtk.Align.START)

        if self.sound_on:
            self.icon_background_box.set_name("toggle-icon-background-enabled")
            self.icon.set_name("toggle-icon-enabled")
        else:
            self.icon_background_box.set_name("toggle-icon-background-disabled")
            self.icon.set_name("toggle-icon-disabled")

        self.icon_background_box.pack_start(self.icon, False, False, 0)
        left_box.add(self.icon_background_box)
        desc_box.pack_start(title, False, False, 0)
        desc_box.pack_start(self.desc, False, False, 0)
        self.title_box.pack_start(left_box, False, False, 0)
        self.title_box.pack_start(desc_box, False, False, 0)

        left_box.connect("button-press-event", self.wifi_clicked)

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

        self.update_ui_with_sound_outputs()

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

    def css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        provider.load_from_path("/home/jonalm/scripts/qtile/bar_menus/volume/volume_menu_styles.css")
        visual = screen.get_rgba_visual()
        self.content_area.set_visual(visual)
        self.set_visual(visual)

    def wifi_clicked(self, widget, event):
        if self.sound_on:
            self.sound_on = False
            self.resize(self.window_width, 10)
            self.set_size_request(self.window_width, 10)
            self.desc.set_text("Off")
            self.status_dot.set_name("status-dot-off")
            subprocess.run(["nmcli",  "radio", "wifi", "off"])
            self.icon_background_box.set_name("toggle-icon-background-disabled")
            self.icon.set_name("toggle-icon-disabled")
            self.list_main_box.hide()
            self.list_options_main_box.hide()
        else:
            self.sound_on = True
            self.resize(self.window_width, self.window_height)
            self.set_size_request(self.window_width, self.window_height)
            self.status_dot.set_name("status-dot-inactive")
            subprocess.run(["nmcli",  "radio", "wifi", "on"])
            self.icon_background_box.set_name("toggle-icon-background-enabled")
            self.icon.set_name("toggle-icon-enabled")
            self.main_box.show_all()

    def scan_clicked(self, widget, event):
        self.history_shown = False
        self.active_known_widget = None
        self.config_box.set_name("toggle-box-list-options-inactive")
        self.config_title.set_name("list-opitons-title-inactive")
        self.scan_box.set_name("toggle-box-list-options-active")
        self.scan_title.set_name("list-opitons-title-active")
        self.update_ui_with_networks()
        
    def history_clicked(self, widget, event):
        self.history_shown = True
        self.config_box.set_name("toggle-box-list-options-active")
        self.config_title.set_name("list-opitons-title-active")
        self.scan_box.set_name("toggle-box-list-options-inactive")
        self.scan_title.set_name("list-opitons-title-inactive")
        self.update_ui_with_known_networks()

    def get_sound_on(self):
        try:
            self.current_volume = subprocess.check_output("pactl get-sink-volume @DEFAULT_SINK@ | awk -F'/' '{print $2}' | awk -F'%' '{print $1}'", shell=True, text=True).strip()
            pulse = pulsectl.Pulse()
            sinks = pulse.sink_list()

            print(sinks)
            print(pulse.server_info().default_sink_name)
            # for index, sink in enumerate(sinks):
                # device_bus = sink.proplist.get("device.bus")
                # if device_bus == "pci":
                    # if sink.proplist.get('alsa.name') == pulse.server_info().default_sink_name:
                        # pass
                # elif device_bus == "bluetooth":
                    # if sink.proplist.get('alsa.name') == pulse.server_info().default_sink_name:

                
            # return mute == 0
        except Exception as e:
            print(f"Error while getting volume: {e}")
            return None
        
    def sound_output_clicked(self, widget, event, network, network_in_use):
        if self.active_widget:
            buttons = self.active_widget.get_parent().get_children()
            for child in buttons[1:]:
                self.active_widget.get_parent().remove(child)
            
            self.active_widget.get_parent().set_name("list-content-box-inactive")

            if self.previous_network_in_use:
                self.active_widget.get_parent().set_name("list-obj-box-active")
                self.previous_network_in_use = False

            if self.active_widget == widget:
                self.active_widget = None
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
            self.previous_network_in_use = True
        else:
            connection_button.set_label("Connect")
            connection_button.connect("button-press-event", self.on_connect_clicked, network, password_entry)
        
        widget.get_parent().set_name("list-content-box-active")
        widget.get_parent().pack_start(button_box, False, False, 0)     
        widget.get_parent().show_all()

        self.active_widget = widget
        return True
    
    def get_sound_outputs(self):
        with open('/home/jonalm/scripts/qtile/bar_menus/wifi/wifi_networks.json', 'r') as json_file:
            networks = json.load(json_file)
        return networks
    
    def update_ui_with_sound_outputs(self):
        # if not self.active_widget and self.sound_on and not self.history_shown:
        #     networks = self.get_networks()
        #     if not networks:
        #         networks = self.scan_offline()

        #     self.desc.set_text(f"{len(networks)} Available")
            
        #     if not networks:
        #         return True

        #     for child in self.list_box.get_children():
        #         self.list_box.remove(child)

        #     for network in networks:
        #         row = Gtk.ListBoxRow()
        #         label = Gtk.Label()

        #         list_content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        #         list_obj_clickable_box = Gtk.EventBox()
        #         list_obj_clickable_box.connect("button-press-event", self.sound_output_clicked, network, network["IN-USE"])

        #         if network["IN-USE"]:
        #             label.set_name("list-obj")
        #             list_content_box.set_name("list-obj-box-active")
        #         else:
        #             label.set_name("list-obj")

        #         label.set_text(network["SSID"][:20])
        #         label.set_halign(Gtk.Align.START)
                
        #         list_obj_clickable_box.add(label)

        #         list_content_box.pack_start(list_obj_clickable_box, False, False, 0)
        #         row.add(list_content_box)
        #         self.list_box.add(row)

        #     self.list_box.show_all()

        return True
    
    def get_mouse_position(self):
        from Xlib import display 
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

    def handle_sigterm(self, signum, frame):
        self.exit_remove_pid() 

    def exit_remove_pid(self):
        try:
            if self.wifi_process.is_alive():
                self.wifi_process.terminate()
                self.wifi_process.join() 

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
    pid_file = "/home/jonalm/scripts/qtile/bar_menus/volume/volume_menu_pid_file.pid"
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

            dialog = VolumeMenu()
            Gtk.main()
                    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        exit(0)
