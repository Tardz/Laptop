import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from config_manager import ConfigManager
from sidebar_events import EventHandler
from sidebar import Sidebar
from content import Content
import copy
import sys
import os

class SettingsMenu(Gtk.Window):
    def __init__(self, pid_file_path):
        Gtk.Window.__init__(self, title="System settings")
        self.pid_file_path = pid_file_path
        self.initialize_resources()
        self.setup_ui()

    def initialize_resources(self):
        self.ignore_focus_lost = True
        self.active_list_box = None
        self.active_list_text = None
        self.first_list_box = None
        self.first_list_info = None
        self.required_restart = False
    
        self.config_manager = ConfigManager()
        self.event_handler = EventHandler(self)
        
        self.load_qtile_data()
        self.load_qtile_colors()
        self.load_other_data()
        self.list_elements = self.config_manager.get_list_elements()

        self.set_can_focus(False)
        
        self.set_property("has-focus", False)

        self.connect("focus-out-event", self.event_handler.on_focus_out)
        self.connect("key-press-event", self.event_handler.on_button_press)

    def load_qtile_data(self):
        self.qtile_data_file_path = os.path.expanduser('~/settings_data/qtile_data.json')
        self.qtile_data = self.config_manager.load_qtile_data(self.qtile_data_file_path)
        self.qtile_data_copy = copy.deepcopy(self.qtile_data)

    def load_qtile_colors(self):
        self.qtile_colors_file_path = os.path.expanduser('~/settings_data/qtile_colors.json')
        self.qtile_colors = self.config_manager.load_qtile_colors(self.qtile_colors_file_path)
        self.qtile_colors_copy = copy.deepcopy(self.qtile_colors)

    def load_other_data(self):
        self.other_data_file_path = os.path.expanduser('~/settings_data/other_data.json')
        self.other_data = self.config_manager.load_other_data(self.other_data_file_path)
        self.other_data_copy = copy.deepcopy(self.other_data)

    def setup_ui(self):
        self.move(780, 300)
        self.window_width = 1160
        self.window_height = 720
        self.set_size_request(self.window_width, self.window_height)

        self.set_name("root")

        self.css()
        self.side_bar = Sidebar(self)
        self.content = Content(self)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.main_box.pack_start(self.side_bar.side_bar_box, False, True, 1)
        self.main_box.pack_start(self.content.overlay, True, True, 0)
        self.add(self.main_box)
    
        self.show_all()
        self.content.qtile.qtile_content_box.hide()
        self.event_handler.change_global_options_visability()
        self.side_bar.search_entry.grab_focus()

    def css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        provider.load_from_path(os.path.expanduser('~/scripts/qtile/settings_menu/css/settings_menu_styles.css'))
        visual = screen.get_rgba_visual()
        self.set_visual(visual)

if __name__ == '__main__':
    pid_file_path = os.path.expanduser('~/scripts/qtile/settings_menu/settings_menu_pid_file.pid')
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

            dialog = SettingsMenu(pid_file_path)
            Gtk.main()
                    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sys.exit(0)
