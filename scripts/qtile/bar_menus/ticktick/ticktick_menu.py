from multiprocessing import Process, Value
from gi.repository import Gtk, WebKit2
from gi.repository import Gtk, Gdk
from Xlib import display 
import subprocess
import requests
import gi
import os

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')

class WebWindow(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self, "TickTick Menu", None, 0)

        self.webview = WebKit2.WebView()
        self.content_area = self.get_content_area()

        self.content_area.pack_start(self.webview, True, True, 0)
        self.webview.connect("load-changed", self.on_load_changed)
        authorization_url = "http://127.0.0.1:5000/login"
        self.webview.load_uri(authorization_url)

    def on_load_changed(self, webview, event):
        if event == WebKit2.LoadEvent.FINISHED:
            current_uri = webview.get_uri()
            print(f"Current URI: {current_uri}")

            if "login" in current_uri:
                self.fetch_projects()

class TicktickMenu(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self, "TickTick Menu", None, 0)

        self.set_size_request(400, 500)

        self.content_area = self.get_content_area()

        self.server_base_url = 'http://127.0.0.1:5000/'

        self.list()
        self.css()

        self.connect("focus-out-event", self.on_focus_out)
        self.connect("key-press-event", self.on_escape_press)

        self.content_area.pack_start(self.list_main_box, True, True, 0)
        
        # self.fetch_project({"project_id": "697a4292a33a085e060d7e62"})
        self.show_all()

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
        # self.update_list_with_projects()

    def css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        provider.load_from_path("/home/jonalm/scripts/qtile/bar_menus/ticktick/ticktick_menu_styles.css")
        visual = screen.get_rgba_visual()
        self.content_area.set_visual(visual)
        self.set_visual(visual)

    def on_project_clicked(self,  widget, event, dir):
        pass

    def on_project_pressed(self, entry, widget, dir):
        self.on_project_clicked(widget=widget, dir=dir)

    def update_list_with_projects(self):
        projects = self.fetch_projects()
        for project in projects:
            row = Gtk.ListBoxRow()
            row.get_style_context().add_class("row")

            list_content_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

            list_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

            list_obj_icon_box = Gtk.EventBox()
            list_obj_icon_box.get_style_context().add_class("list-icon-box")
            icon = Gtk.Label()
            icon.get_style_context().add_class("list-icon")
            icon.set_text(project["name"][0])
            list_obj_icon_box.add(icon)

            list_obj_clickable_box = Gtk.EventBox()
            list_obj_clickable_box.connect("button-press-event", self.on_project_clicked, project)
            project_name = Gtk.Label()
            project_name.get_style_context().add_class("list-name")
            project_name.set_text(project["name"][1:])
            list_obj_clickable_box.add(project_name)

            list_content_box.pack_start(list_obj_icon_box, True, True, 0)
            list_content_box.pack_start(list_obj_clickable_box, True, True, 0)
            list_content_main_box.pack_start(list_content_box, True, True, 0)

            row.add(list_content_main_box)
            row.connect("activate", self.on_project_pressed, list_obj_clickable_box, project)
            self.list_box.add(row)

        self.list_box.show_all()
        return True

    def fetch_projects(self):
        response = requests.get(f'{self.server_base_url}projects')

        if response.status_code == 200:
            projects = response.json()
            print(projects)
            return projects
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return []
        
    def fetch_project(self, project_id):
        response = requests.get(f'{self.server_base_url}project', params=project_id)

        if response.status_code == 200:
            tasks = response.json()
            print(tasks)
            return tasks
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return []
        
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

    def on_focus_out(self, widget, event, escape=False):
        if not self.ignore_focus_lost or escape:
            self.exit_remove_pid()
        
    def on_escape_press(self, widget, event):
        keyval = event.keyval
        if keyval == Gdk.KEY_Escape:
            self.on_focus_out(widget, event, True)

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
    pid_file = "/home/jonalm/scripts/qtile/bar_menus/ticktick/ticktick_menu_pid_file.pid"
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

            process = Process(target=wifi_process)
            process.start()

            dialog = WifiMenu(process)
            Gtk.main()
                    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        exit(0)


if __name__ == '__main__':
    win = TicktickMenu()
    Gtk.main()
