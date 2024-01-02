import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, GLib
import pulsectl
import pygame
import signal
import sys
import os

class VolumeMenu(Gtk.Dialog):
    def __init__(self, pid_file_path):
        Gtk.Dialog.__init__(self, "Sound Control", None, 0)
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
        self.content_area.set_visual(visual)
        self.set_visual(visual)

    def setup_ui(self):
        x, y = self.get_mouse_position()
        self.move(x, y)

        self.window_width = 200
        self.window_height = 250
        self.set_size_request(self.window_width, self.window_height)

        self.content_area = self.get_content_area()
        self.content_area.set_name("content-area")
        self.set_name("root")

        self.css()
        self.title()
        self.list()

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.main_box.pack_start(self.title_box, False, False, 0)
        self.main_box.pack_start(self.list_main_box, True, True, 0)

        self.content_area.pack_start(self.main_box, True, True, 0)

        self.show_all()

    def title(self):
        self.title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.title_box.set_name("toggle-box")

        desc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        desc_box.set_name("toggle-desc-box")

        title = Gtk.Label()
        title.set_text("Outputs")
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

        left_box.connect("button-press-event", self.volume_clicked)

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

        # GLib.timeout_add(4000, self.update_list_with_sound_outputs)

    def volume_clicked(self, widget, event):
        if self.sound_on:
            self.sound_on = False
            self.desc.set_text("Muted")
            self.icon.set_text("")
            self.pulse.sink_mute(self.active_sink.index, 1)
            self.icon_background_box.set_name("toggle-icon-background-disabled")
            self.icon.set_name("toggle-icon-disabled")
        else:
            self.sound_on = True
            self.icon.set_text("")
            self.pulse.sink_mute(self.active_sink.index, 0)
            self.icon_background_box.set_name("toggle-icon-background-enabled")
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
        
        for child in self.list_box.get_children():
            self.list_box.remove(child)

        for sink in sinks:
            row = Gtk.ListBoxRow()
            row.set_name("row")
            label = Gtk.Label()

            list_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            list_obj_icon_box = Gtk.EventBox()
            list_obj_icon_box.set_name("list-icon-box")
            icon = Gtk.Label()

            device_type = sink.proplist["device.icon_name"] 
            if device_type == "audio-headphones-bluetooth":
                icon.set_name("list-icon-headphone")
                icon.set_text("")
            elif device_type == "audio-card-pci":
                icon.set_name("list-icon-speaker")
                icon.set_text("")
            elif device_type == "audio-card-usb":
                icon.set_name("list-icon-headphone")
                icon.set_text("")

            list_obj_clickable_box = Gtk.EventBox()

            if sink.name == self.active_sink.name:
                label.set_name("list-obj")
                list_content_box.set_name("list-obj-box-active")
            else:
                list_obj_clickable_box.connect("button-press-event", self.sound_output_clicked, sink)
                list_content_box.set_name("list-obj-box-inactive")
                label.set_name("list-obj")

            if sink.description == "Family 17h/19h HD Audio Controller Analog Stereo":
                label.set_text("Laptop Speakers")
            elif sink.description == "HyperX Cloud Alpha Wireless Analog Stereo":
                label.set_text("HyperX Headphones")
            else:
                label.set_text(sink.description)
            
            label.set_halign(Gtk.Align.START)
            
            list_obj_icon_box.add(icon)
            list_obj_clickable_box.add(label)

            list_content_box.pack_start(list_obj_icon_box, False, False, 0)
            list_content_box.pack_start(list_obj_clickable_box, False, False, 0)
            row.add(list_content_box)
            self.list_box.add(row)

        self.list_box.show_all()
        return False

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
            self.exit_remove_pid()

    def on_escape_press(self, widget, event):
        keyval = event.keyval
        if keyval == Gdk.KEY_Escape:
            self.exit_remove_pid()

    def handle_sigterm(self, signum, frame):
        self.exit_remove_pid() 

    def exit_remove_pid(self):  
        try:
            self.pulse.close()
            with open(self.pid_file_path, "r") as file:
                pid = int(file.read().strip())
            try:
                os.remove(self.pid_file_path)
                os.kill(pid, 15)
            except ProcessLookupError:
                pass
        finally:
            sys.exit(0)

if __name__ == '__main__':
    pid_file_path = "/home/jonalm/scripts/qtile/bar_menus/volume/volume_menu_pid_file.pid"
    dialog = None

    try:
        if os.path.isfile(pid_file_path):
            with open(pid_file_path, "r") as file:
                pid = int(file.read().strip())
            try:
                os.remove(pid_file_path)
                os.kill(pid, 9)    
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            with open(pid_file_path, "w") as file:
                file.write(str(os.getpid()))

            dialog = VolumeMenu(pid_file_path)
            Gtk.main()
                    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sys.exit(0)
