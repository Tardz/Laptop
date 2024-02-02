import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, GLib
import subprocess
import pulsectl
import signal
import sys
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class VolumeMenu(Gtk.Window):
    def __init__(self, pid_file_path):
        Gtk.Window.__init__(self, title="Sound Control")
        signal.signal(signal.SIGTERM, self.handle_sigterm)
        self.singal_file_path = os.path.expanduser("~/scripts/qtile/bar_menus/volume/signal_data.txt")
        self.hidden = False
        self.pid_file_path = pid_file_path
        self.initialize_resources()
        self.setup_ui()
        GLib.idle_add(self.update_list_with_sound_outputs)

    def initialize_resources(self):
        self.connect("focus-out-event", self.on_focus_out)
        self.connect("key-press-event", self.on_escape_press)

        pygame.mixer.init()
        self.pulse = pulsectl.Pulse()
        self.active_sink = self.get_active_sink()
        self.sound_on = self.get_sound_on()
        self.ignore_focus_lost = False

    def css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        provider.load_from_path("/home/jonalm/scripts/qtile/bar_menus/volume/volume_menu_styles.css")
        visual = screen.get_rgba_visual()
        self.set_visual(visual)

    def setup_ui(self):
        x, y = self.get_mouse_position()
        self.move(x, y)

        self.window_width = 290
        self.window_height = 220
        self.set_size_request(self.window_width, self.window_height)

        self.set_name("root")

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.main_box.get_style_context().add_class("main")

        self.css()
        self.create_title()
        self.create_list()

        self.add(self.main_box)
        self.main_box.grab_focus()
        self.show_all()

    def create_title(self):
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        title_box.get_style_context().add_class("toggle-box")

        desc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        title = Gtk.Label()
        title.get_style_context().add_class("toggle-title")
        title.set_text("Outputs")
        title.set_halign(Gtk.Align.START)

        self.desc = Gtk.Label()
        self.desc.get_style_context().add_class("toggle-desc")
        self.desc.set_halign(Gtk.Align.START)
        if not self.sound_on:
            self.desc.set_text("Off")

        left_box = Gtk.EventBox()
        icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        self.icon = Gtk.Label()
        self.icon.get_style_context().add_class('toggle-icon')
        self.icon.set_text("")
        self.icon.set_halign(Gtk.Align.START)

        if self.sound_on:
            self.icon.set_name("toggle-icon-enabled")
        else:
            self.icon.set_name("toggle-icon-disabled")

        icon_box.pack_start(self.icon, False, False, 0)
        left_box.add(icon_box)
        desc_box.pack_start(title, False, False, 0)
        desc_box.pack_start(self.desc, False, False, 0)
        title_box.pack_start(left_box, False, False, 0)
        title_box.pack_start(desc_box, False, False, 0)

        left_box.connect("button-press-event", self.volume_clicked)
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

        self.main_box.pack_start(self.list_box, True, True, 0)

        self.update_sounds_timeout = GLib.timeout_add(6000, self.update_list_with_sound_outputs)

    def volume_clicked(self, widget, event):
        if self.sound_on:
            self.sound_on = False
            self.desc.set_text("Muted")
            self.icon.set_text("")
            self.pulse.sink_mute(self.active_sink.index, 1)
            self.icon.set_name("toggle-icon-disabled")
        else:
            self.sound_on = True
            self.icon.set_text("")
            self.pulse.sink_mute(self.active_sink.index, 0)
            self.icon.set_name("toggle-icon-enabled")
            self.update_list_with_sound_outputs()

    def sound_output_clicked(self, widget, event, sink):
        self.pulse.sink_default_set(sink.name)
        pygame.mixer.music.load('/home/jonalm/scripts/qtile/bar_menus/volume/output_change_sound.mp3')
        pygame.mixer.music.play()
        self.active_sink = self.get_active_sink()
        self.update_list_with_sound_outputs()
        
    def get_active_sink(self):
        sinks = self.pulse.sink_list()
        default_sink = self.pulse.server_info().default_sink_name
        active_sink = None
        for sink in sinks:
            if sink.name == default_sink:
                active_sink = sink

        return active_sink

    def get_sound_on(self):
        return self.active_sink.mute == 0
        
    def update_list_with_sound_outputs(self):
        sinks = self.pulse.sink_list()

        if self.sound_on:
            self.desc.set_text(f"{len(sinks)} Available")
        else:
            self.desc.set_text("Muted")
        
        for child in self.list.get_children():
            self.list.remove(child)

        for sink in sinks:
            row = Gtk.ListBoxRow()
            row.get_style_context().add_class('list-row')

            row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            row_box.get_style_context().add_class('row-box')

            icon_box = Gtk.EventBox()
            icon = Gtk.Label()
            icon.get_style_context().add_class('list-icon')

            name_box = Gtk.EventBox()
            name = Gtk.Label()
            name.get_style_context().add_class('list-name')
            name.set_halign(Gtk.Align.START)

            device_type = sink.proplist["device.icon_name"] 
            print("sinkname: " + sink.name)
            print("sink desc: " + sink.description)
            print("device_type: " + device_type + "\n")

            if sink.name == self.active_sink.name:
                row.set_name("row-box-active")
                print ("aiwda")
                print(device_type)
                if device_type == "audio-headphones-bluetooth" or device_type == "audio-headset-bluetooth":
                    if "Pods" in sink.description or "Ear" in sink.description:
                        print  ("aiwda")
                        icon.set_text("")
                    else:
                        icon.set_text("")
                    icon.set_name("list-icon-headphone-active")
                elif device_type == "audio-card-pci":
                    icon.set_name("list-icon-speaker-active")
                    icon.set_text("")
                elif device_type == "audio-card-usb":
                    icon.set_name("list-icon-headphone-active")
                    icon.set_text("")
            else:
                if device_type == "audio-headphones-bluetooth" or device_type == "audio-headset-bluetooth":
                    if "Pods" in sink.description or "Ear" in sink.description:
                        icon.set_text("")
                    else:
                        icon.set_text("")
                    icon.set_name("list-icon-headphone-inactive")
                elif device_type == "audio-card-pci":
                    icon.set_name("list-icon-speaker-inactive")
                    icon.set_text("")
                elif device_type == "audio-card-usb":
                    icon.set_name("list-icon-headphone-inactive")
                    icon.set_text("")
                name_box.connect("button-press-event", self.sound_output_clicked, sink)
                row.set_name("row-box-inactive")

            if sink.description == "Family 17h/19h HD Audio Controller Analog Stereo":
                name.set_text("Laptop Speakers")
            elif sink.description == "HyperX Cloud Alpha Wireless Analog Stereo":
                name.set_text("HyperX Headphones")
            elif "Bose" in sink.description:
                name.set_text("Bose Headphones")
            elif "Pods" in sink.description:
                name.set_text("Airpods")
            else:
                name.set_text(sink.description)
            
            icon_box.add(icon)
            name_box.add(name)

            row_box.pack_start(icon_box, False, False, 0)
            row_box.pack_start(name_box, False, False, 0)
            row.add(row_box)
            self.list.add(row)

        # self.add_test_outputs(2)
        self.list.show_all()
        return False
    
    def add_test_outputs(self, n):
        for i in range(n):
            row = Gtk.ListBoxRow()
            row.get_style_context().add_class('list-row')

            row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            row_box.get_style_context().add_class('row-box')

            icon_box = Gtk.EventBox()
            icon_box.get_style_context().add_class('list-icon-box')
            icon = Gtk.Label()
            icon.get_style_context().add_class('list-icon')

            name_box = Gtk.EventBox()
            name = Gtk.Label()
            name.get_style_context().add_class('list-name')
            name.set_halign(Gtk.Align.START)

            icon.set_name("list-icon-headphone-inactive")
            icon.set_text("")

            row.set_name("row-box-inactive")

            name.set_text(f"Test output {i}")
            
            icon_box.add(icon)
            name_box.add(name)

            row_box.pack_start(icon_box, False, False, 0)
            row_box.pack_start(name_box, False, False, 0)
            row.add(row_box)
            self.list.add(row)

    def get_mouse_position(self):
        from Xlib import display 
        from Xlib.ext import randr
        try:
            d = display.Display()
            s = d.screen()
            root = s.root
            root.change_attributes(event_mask=0x10000)
            pointer = root.query_pointer()
            x = pointer.root_x - 130

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
            self.hide_menu()

    def handle_sigterm(self, signum, frame):
        with open(self.singal_file_path, "r") as file:
            signal_arg = file.read()
            with open(self.singal_file_path, "w") as file:
                file.write("")

            if signal_arg == "hide":
                self.hide_menu()
            elif signal_arg == "kill":
                self.pulse.close()
                GLib.idle_add(Gtk.main_quit)  

    def hide_menu(self):  
        try:
            if self.hidden:
                self.ignore_focus_lost = False
                self.pulse = pulsectl.Pulse()
                self.update_list_with_sound_outputs()
                self.update_sounds_timeout = GLib.timeout_add(6000, self.update_list_with_sound_outputs)
                self.hidden = False
                self.show()
            else:
                self.ignore_focus_lost = True
                GLib.source_remove(self.update_sounds_timeout)
                self.pulse.close()
                self.hidden = True
                subprocess.run("qtile cmd-obj -o widget volumeicon -f unclick", shell=True)
                self.hide()

        except Exception as e:
            print(f"Error occurred: {e}")

def write_pid_to_settings_data(pid, json_file_path):
    import json
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data['volume_menu_pid'] = pid

    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

    subprocess.run("qtile cmd-obj -o widget volumeicon -f update_menu_pid", shell=True)

def remove_pid_from_settings_data(json_file_path):
    import json
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data['volume_menu_pid'] = None

    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

    subprocess.run("qtile cmd-obj -o widget volumeicon -f update_menu_pid", shell=True)

if __name__ == '__main__':
    pid_file_path = os.path.expanduser("~/scripts/qtile/bar_menus/volume/volume_menu_pid_file.pid")
    json_file_path = os.path.expanduser("~/settings_data/processes.json")
    dialog = None
        
    try:
        if not os.path.isfile(pid_file_path):
            pid = os.getpid()
            write_pid_to_settings_data(pid, json_file_path)
            
            with open(pid_file_path, "w") as file:
                file.write(str(pid))

            dialog = VolumeMenu(pid_file_path)
            Gtk.main()
        else:
            print("Another instance of this menu is already active.")
                    
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if dialog:
            dialog.destroy
            remove_pid_from_settings_data(json_file_path)
            os.remove(pid_file_path)
        sys.exit(0)
