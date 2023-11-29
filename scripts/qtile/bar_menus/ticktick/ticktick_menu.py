import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2
from gi.repository import Gtk, Gdk, GLib, Pango
import requests

class TicktickMenu(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self, "TickTick Menu", None, 0)

        self.set_size_request(400, 500)

        self.content_area = self.get_content_area()
        self.webview = WebKit2.WebView()

        self.server_base_url = 'http://127.0.0.1:5000/'

        self.list()
        self.css()

        self.content_area.pack_start(self.list_main_box, True, True, 0)
        
        content_area.pack_start(self.webview, True, True, 0)
        self.webview.connect("load-changed", self.on_load_changed)
        authorization_url = "http://127.0.0.1:5000/login"  # Replace with your server's IP and port
        self.webview.load_uri(authorization_url)
        # self.fetch_projects()
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
            row.set_name("row")

            list_content_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

            list_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

            list_obj_icon_box = Gtk.EventBox()
            list_obj_icon_box.set_name("list-icon-box")
            icon = Gtk.Label()
            icon.set_name("list-icon")
            icon.set_text(project["name"][0])
            list_obj_icon_box.add(icon)

            list_obj_clickable_box = Gtk.EventBox()
            list_obj_clickable_box.connect("button-press-event", self.on_project_clicked, project)
            project_name = Gtk.Label()
            project_name.set_name("list-obj")
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

    def on_load_changed(self, webview, event):
        # Check if the page has finished loading
        if event == WebKit2.LoadEvent.FINISHED:
            current_uri = webview.get_uri()
            print(f"Current URI: {current_uri}")

            if "login" in current_uri:
                self.fetch_projects()

if __name__ == '__main__':
    win = TicktickMenu()
    Gtk.main()
