import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2
from gi.repository import Gtk, Gdk
from Xlib import display 
import subprocess
import requests
import time
import os
import signal

class WebWindow(Gtk.Dialog):
    def __init__(self, parent):
        super(WebWindow, self).__init__(title="Web Window", transient_for=parent)
        self.parent = parent

        x, y = self.get_mouse_position()
        self.move(x, y)

        self.set_size_request(400, 500)

        self.webview = WebKit2.WebView()
        self.content_area = self.get_content_area()
        
        authorization_url = "http://127.0.0.1:5000/login"

        self.content_area.pack_start(self.webview, True, True, 0)
        self.webview.connect("load-changed", self.on_load_changed)
        self.webview.load_uri(authorization_url)

        self.show_all()

    def on_load_changed(self, webview, event):
        if event == WebKit2.LoadEvent.FINISHED:
            current_uri = webview.get_uri()
            print(f"Current URI: {current_uri}")

            # if "login" in current_uri:
            #     self.fetch_projects()

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
        self.parent.active_widget = None
        self.parent.ignore_focus_lost = False
        self.destroy()

class TicktickMenu(Gtk.Dialog):
    def __init__(self, pid_file_path):
        Gtk.Dialog.__init__(self, "TickTick Menu", None, 0)

        self.content_area = self.get_content_area()

        self.pid_file_path = pid_file_path
        self.server_base_url = 'http://127.0.0.1:5000/'
        self.ignore_focus_lost = False
        self.active_widget = None
        self.personal_group_id = "c7cf4a1c8f1860c8183b2a9b"
        self.kalender_group_id = "630e7742b8c1113812839640"
        self.project_group_id = "64e6351e019fd105a6f7196a"
        self.rows = []
        self.active_project = None

        self.content_area.get_style_context().add_class('content-area')
        self.get_style_context().add_class('root')

        self.title()
        self.project_list()
        self.task_list()
        self.css()

        self.connect("focus-out-event", self.on_focus_out)
        self.connect("key-press-event", self.on_escape_press)
        signal.signal(signal.SIGTERM, self.handle_sigterm)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        list_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        list_main_box.pack_start(self.project_list_main_box, False, True, 0)
        list_main_box.pack_start(self.task_list_main_box, True, True, 0)

        main_box.pack_start(self.title_main_box, False, True, 0)
        main_box.pack_start(list_main_box, True, True, 0)

        self.content_area.pack_start(main_box, True, True, 0)

        self.show_all()
        self.task_list_main_box.hide()
        self.set_size_request(400, 500)

        self.update_list_with_projects()

    def title(self):
        self.title_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        title_box.get_style_context().add_class("toggle-title-box")

        title = Gtk.Label() 
        title.get_style_context().add_class('toggle-title')
        title.set_text("TickTick")
        title.set_halign(Gtk.Align.START)

        left_box = Gtk.EventBox()

        self.icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.icon_box.get_style_context().add_class('toggle-icon-box')

        self.icon = Gtk.Label()
        self.icon.get_style_context().add_class('toggle-icon')
        self.icon.set_text("")
        self.icon.set_halign(Gtk.Align.START)

        self.icon_box.set_name("toggle-icon-box-enabled")
        self.icon.set_name("toggle-icon-enabled")

        self.status_dot = Gtk.Label()
        self.status_dot.get_style_context().add_class('status-dot')
        self.status_dot.set_text("")
        self.status_dot.set_name("status-dot-inactive")
        self.status_dot.set_halign(Gtk.Align.END)
        
        self.icon_box.pack_start(self.icon, False, False, 0)
        left_box.add(self.icon_box)
        title_box.pack_start(left_box, False, False, 0)
        title_box.pack_start(title, False, False, 0)
        title_box.pack_start(self.status_dot, True, True, 0)

        self.title_main_box.pack_start(title_box, False, False, 0)
        
    def project_list(self):
        self.project_list_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        self.project_list_box = Gtk.ListBox()
        self.project_list_box.get_style_context().add_class("list")
        self.project_list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.get_style_context().add_class("list-box")
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC) 
        scrolled_window.add(self.project_list_box)  

        self.project_list_main_box.pack_start(scrolled_window, True, True, 0)

    def task_list(self):
        self.task_list_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.task_list_main_box.get_style_context().add_class("task-list-main-box")
        
        task_list_title_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        task_list_title_main_box.get_style_context().add_class("task_list_title_main_box")

        task_list_icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        task_list_icon_box.get_style_context().add_class('task-list-icon-box')
        self.task_list_icon = Gtk.Label()
        self.task_list_icon.get_style_context().add_class('task-list-icon')
        self.task_list_icon.set_halign(Gtk.Align.START)
        task_list_icon_box.pack_start(self.task_list_icon, False, False, 0)

        task_list_title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.task_list_title = Gtk.Label() 
        self.task_list_title.get_style_context().add_class('task-list-title')
        self.task_list_title.set_halign(Gtk.Align.START)
        task_list_title_box.pack_start(self.task_list_title, True, False, 0)

        plus_event_box = Gtk.EventBox()
        plus_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        plus_box.get_style_context().add_class('task-list-plus-box')
        plus_icon = Gtk.Label() 
        plus_icon.get_style_context().add_class('task-list-plus-icon')
        plus_icon.set_text("+")
        plus_box.pack_start(plus_icon, False, True, 0)
        plus_event_box.add(plus_box)

        task_list_title_main_box.pack_start(task_list_icon_box, False, True, 0)
        task_list_title_main_box.pack_start(task_list_title_box, False, True, 0)
        task_list_title_main_box.pack_start(plus_event_box, True, False, 0)

        self.task_list_box = Gtk.ListBox()
        self.task_list_box.get_style_context().add_class("task-list")
        self.task_list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.get_style_context().add_class("task-list-box")
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC) 
        scrolled_window.add(self.task_list_box)  

        self.task_list_main_box.pack_start(task_list_title_main_box, False, True, 0)
        self.task_list_main_box.pack_start(scrolled_window, True, True, 0)

    def css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        provider.load_from_path("ticktick_menu_styles.css")
        visual = screen.get_rgba_visual()
        self.content_area.set_visual(visual)
        self.set_visual(visual)

    def open_login_window(self):
        self.ignore_focus_lost = True
        login_window = WebWindow(self)
        login_window.run()

    def on_folder_clicked(self, widget, event, folder_group_id, folder_icon):
        for folder in self.rows:
            if folder['folder_group_id'] == folder_group_id:
                if folder['hidden']:
                    for row in folder['rows']:
                        row.show()
                    folder['hidden'] = False
                    folder_icon.set_text("")
                    folder_icon.set_name("main-list-icon-shown")
                else:
                    for row in folder['rows']:
                        row.hide()
                    folder['hidden'] = True
                    folder_icon.set_text("")
                    folder_icon.set_name("main-list-icon-hidden")

    def on_folder_pressed(self, entry, widget, folder_group_id, folder_icon):
        self.on_folder_clicked(widget=widget, folder_group_id=folder_group_id, folder_icon=folder_icon)

    def on_project_clicked(self, widget, event, row_content_box, row_icon, row_name):
        if self.active_project:
            self.active_project["content_box"].set_name("list-name-box-inactive")
            self.active_project["icon"].set_name("sub-list-icon-inactive")
            if self.active_project["content_box"] == row_content_box:
                self.resize(400, 500)
                self.set_size_request(400, 500)
                self.active_project = None
                self.task_list_main_box.hide()
            else:
                self.task_list_title.set_text(row_name[1:])
                self.task_list_icon.set_text(row_name[0])
                self.set_size_request(800, 500)
                self.task_list_main_box.show()
                row_content_box.set_name("list-name-box-active")
                row_icon.set_name("sub-list-icon-active")
                self.active_project = {'content_box': row_content_box, 'icon': row_icon}
        else:
            self.task_list_title.set_text(row_name[1:])
            self.task_list_icon.set_text(row_name[0])
            self.set_size_request(800, 500)
            self.task_list_main_box.show()
            row_content_box.set_name("list-name-box-active")
            row_icon.set_name("sub-list-icon-active")
            self.active_project = {'content_box': row_content_box, 'icon': row_icon}

    def on_project_pressed(self, entry, widget, row_content_box, row_icon, row_name):
        self.on_project_clicked(widget=widget, row_content_box=row_content_box, row_icon=row_icon, row_name=row_name)

    def update_list_with_projects(self):
        projects = self.fetch_projects()
        folder_count = 0
        prev_project = None
        if projects:
            for i, project in enumerate(projects):
                row = Gtk.ListBoxRow()                
                row.get_style_context().add_class("sub-row")
                
                list_content_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

                list_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
                list_content_box.get_style_context().add_class('list-name-box')

                list_obj_icon_box = Gtk.EventBox()
                list_obj_icon_box.get_style_context().add_class("sub-list-icon-box")
                icon = Gtk.Label()
                icon.get_style_context().add_class("sub-list-icon")
                icon.set_text(project["name"][0])
                list_obj_icon_box.add(icon)

                branch_icon_box = Gtk.EventBox()
                branch_icon = Gtk.Label()
                if i == len(projects) - 1 or (projects[i+1]["group_id"] and project["group_id"] != projects[i+1]["group_id"]):
                    branch_icon.set_text("└")
                else: 
                    branch_icon.set_text("├")
                branch_icon.get_style_context().add_class("branch-icon")
                branch_icon_box.add(branch_icon)

                list_name_clickable_box = Gtk.EventBox()
                project_name = Gtk.Label()
                project_name.get_style_context().add_class("sub-list-name")
                project_name.set_text(project["name"][1:])
                project_name.set_halign(Gtk.Align.START)
                list_name_clickable_box.add(project_name)

                list_content_box.pack_start(list_obj_icon_box, False, True, 0)
                list_content_box.pack_start(list_name_clickable_box, True, True, 0)
                list_content_main_box.pack_start(branch_icon_box, False, True, 0)
                list_content_main_box.pack_start(list_content_box, True, True, 0)

                if not prev_project or ("group_id" in prev_project and "group_id" in project and project["group_id"] != prev_project["group_id"]): 
                    folder_row = Gtk.ListBoxRow()                
                    folder_row.get_style_context().add_class("main-row")

                    folder_content_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
                    folder_content_main_box.get_style_context().add_class('list-name-box')

                    folder_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

                    folder_icon_box = Gtk.EventBox()
                    folder_icon_box.get_style_context().add_class("main-list-icon-box")

                    folder_icon = Gtk.Label()
                    folder_icon.set_text("")
                    folder_icon.get_style_context().add_class("main-list-icon")
                    folder_icon.set_name("main-list-icon-shown")
                    folder_icon_box.add(folder_icon)

                    folder_name_box = Gtk.EventBox()
                    folder_name_box.connect("button-press-event", self.on_folder_clicked, project["group_id"], folder_icon)

                    folder_name = Gtk.Label()
                    if project["group_id"] == "c7cf4a1c8f1860c8183b2a9b":
                        folder_name.set_text("ToDo")
                    elif project["group_id"] == "630e7742b8c1113812839640":
                        folder_name.set_text("Calender")
                    elif project["group_id"] == "64e6351e019fd105a6f7196a":
                        folder_name.set_text("Project")
                    else:
                        folder_name.set_text("Other")

                    folder_name.get_style_context().add_class("main-list-name")
                    folder_name.set_halign(Gtk.Align.START)
                    folder_name_box.add(folder_name)

                    folder_content_box.pack_start(folder_icon_box, False, True, 0)
                    folder_content_box.pack_start(folder_name_box, True, True, 0)
                    folder_content_main_box.pack_start(folder_content_box, True, True, 0)
                    
                    folder_row.add(folder_content_main_box)
                    self.project_list_box.add(folder_row)
                    
                    folder_count += 1
                    self.rows.append({'folder_group_id': project['group_id'], 'rows': [], 'hidden': False})

                prev_project = project

                row.add(list_content_main_box)
                row.connect("activate", self.on_project_pressed, list_name_clickable_box, project)
                self.project_list_box.add(row)

                list_name_clickable_box.connect("button-press-event", self.on_project_clicked, list_content_box, icon, project["name"])

                for folder in self.rows:
                    if folder['folder_group_id'] == project['group_id']: 
                        folder['rows'].append(row)

        self.project_list_box.show_all()
        return True
    
    def handle_token_expiry(self, response):
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 302:
            print("opening web login window \n")
            self.open_login_window()
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return []

    def fetch_projects(self, retries=5, updated=False):
        for _ in range(retries):
            try:
                if updated:
                    response = requests.get(f'{self.server_base_url}updated_projects')
                    return self.handle_token_expiry(response)
                else:
                    response = requests.get(f'{self.server_base_url}projects')
                    return self.handle_token_expiry(response)
            except requests.ConnectionError:
                print("Waiting for the server to start...")
                time.sleep(2)
        print("Max retries exceeded. Unable to connect to the server.")
        return []
    
    def fetch_project(self, project_id):
        response = requests.get(f'{self.server_base_url}project', params=project_id)
        return self.handle_token_expiry(response)

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
            with open(self.pid_file_path, "r") as file:
                pid = int(file.read().strip())
            try:
                os.remove(self.pid_file_path)
                os.kill(pid, 15)
            except ProcessLookupError:
                pass
        finally:
            exit(0)

if __name__ == '__main__':
    pid_file_path = "/home/jonalm/scripts/qtile/bar_menus/ticktick/ticktick_menu_pid_file.pid"
    dialog = None

    try:
        if os.path.isfile(pid_file_path):
            with open(pid_file_path, "r") as file:
                pid = int(file.read().strip())
            try:
                os.remove(pid_file_path)
                os.kill(pid, 15)            
            except ProcessLookupError:
                pass
        else:
            with open(pid_file_path, "w") as file:
                file.write(str(os.getpid()))

        dialog = TicktickMenu(pid_file_path)
        Gtk.main()
                    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        exit(0)
