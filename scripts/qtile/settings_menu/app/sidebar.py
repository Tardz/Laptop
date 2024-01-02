
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class CustomListBoxRow(Gtk.ListBoxRow):
    def __init__(self):
        Gtk.ListBoxRow.__init__(self)
        self.get_style_context().add_class('list-row')

class CustomListBox(Gtk.ListBox):
    def __init__(self):
        Gtk.ListBox.__init__(self)
        self.get_style_context().add_class('list-box')

class Sidebar:
    def __init__(self, app):
        self.app = app
        self.side_bar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=11)
        self.side_bar_box.get_style_context().add_class("sidebar-box")
        
        self.create_title()
        self.create_search()
        self.create_settings_list()
        self.create_global_options()

        self.side_bar_box.pack_start(self.title_box, False, True, 0)
        self.side_bar_box.pack_start(self.search_box, False, True, 0)
        self.side_bar_box.pack_start(self.list_box, True, True, 0)
        self.side_bar_box.pack_start(self.global_options_box, False, True, 0)
        self.side_bar_box.set_size_request(300, -1)

        self.configure_list()

    def create_title(self):
        self.title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.title_box.get_style_context().add_class("title-box")

        title = Gtk.Label()
        title.get_style_context().add_class("title")
        title.set_text("Settings")
        
        self.title_box.pack_start(title, True, True, 0)

    def create_search(self):
        self.search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.search_box.get_style_context().add_class("search-box")
        search_icon = Gtk.Label()
        search_icon.get_style_context().add_class("search-icon")
        search_icon.set_text("")

        self.search_entry = Gtk.Entry()
        self.search_entry.get_style_context().add_class("search-bar")
        self.search_entry.set_halign(Gtk.Align.START)
        self.search_entry.set_placeholder_text("Search")
        self.search_entry.connect("changed", self.app.event_handler.on_search_changed)
        self.search_entry.connect("activate", self.app.event_handler.on_search_pressed)

        self.search_box.pack_start(search_icon, False, True, 0)
        self.search_box.pack_start(self.search_entry, False, True, 0)

    def create_settings_list(self):
        self.list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.list_box.get_style_context().add_class('list-box')

        # self.list = Gtk.ListBox()
        self.list = CustomListBox()
        self.list.get_style_context().add_class('list')
        self.list.set_selection_mode(Gtk.SelectionMode.NONE)
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.get_style_context().add_class("scrolled-window")
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC) 
        scrolled_window.add(self.list)  

        self.list_box.pack_start(scrolled_window, True, True, 0)

    def configure_list(self, specified_elements=None):
        if specified_elements != None:
            list_elements = specified_elements
        else:
            list_elements = self.app.list_elements

        for i, element in enumerate(list_elements):
            row = CustomListBoxRow()
            # row = Gtk.ListBoxRow()
            row.get_style_context().add_class('list-row')
            if i == 0:
                row.set_name("first-list-row")
            elif i == len(list_elements):
                row.set_name("other-list-row")
            else:
                row.set_name("last-list-row")

            event_box = Gtk.EventBox()

            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            box.get_style_context().add_class('list-item-box')
            box.set_name("list-item-box-inactive")

            icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            icon_box.get_style_context().add_class('list-item-icon-box')
            icon_box.set_name(element["css"] + "-box")
            icon = Gtk.Label()
            icon.get_style_context().add_class('general-icon')
            icon.set_name(element["css"] + "-icon")
            icon.set_text(element["icon"])
            icon_box.pack_start(icon, False, False, 0)
            
            title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            title_box.get_style_context().add_class('list-item-title-box')
            title = Gtk.Label()
            title.get_style_context().add_class('list-item-title')
            title.set_text(element["title"])
            title_box.pack_start(title, False, False, 0)

            box.pack_start(icon_box, False, False, 0)
            box.pack_start(title_box, False, False, 0)

            event_box.add(box)
            row.add(event_box)
            self.list.add(row)

            row.connect("button-press-event", self.app.event_handler.on_item_clicked, element, box)
            row.connect("key-press-event", self.app.event_handler.on_item_pressed, element, box)
            if i == 0:
                self.app.first_list_box = box
                self.app.first_list_info = element

            if (specified_elements == None and not self.app.active_list_box) or element["title"] == self.app.active_list_text:
                self.app.active_list_text = element["title"]
                self.app.active_list_box = box
                self.app.active_list_box.set_name("list-item-box-active")
                
        self.app.show_all()

    def create_global_options(self):
        self.global_options_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        self.quit_box = Gtk.EventBox()
        self.quit_box.set_name("global-options-icon-box-inactive")
        quit_icon_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        quit_icon_box.get_style_context().add_class("global-options-icon-box")
        self.quit_icon = Gtk.Label()
        self.quit_icon.get_style_context().add_class("global-options-icon")
        self.quit_icon.set_name("quit-icon-inactive")
        self.quit_icon.set_text("")
        quit_icon_box.add(self.quit_icon)
        self.quit_box.add(quit_icon_box)
        self.quit_box.connect("enter-notify-event", self.app.event_handler.global_options_on_box_enter, self.quit_box, self.quit_icon, "quit-icon-box-active")
        self.quit_box.connect("leave-notify-event", self.app.event_handler.global_options_on_box_leave, self.quit_box, self.quit_icon, "quit-icon-inactive")
        self.quit_box.connect("button-press-event", self.app.event_handler.on_exit_press)

        self.revert_box = Gtk.EventBox()
        self.revert_box.set_name("global-options-icon-box-inactive")
        revert_icon_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        revert_icon_box.get_style_context().add_class("global-options-icon-box")
        self.revert_icon = Gtk.Label()
        self.revert_icon.get_style_context().add_class("global-options-icon")
        self.revert_icon.set_name("revert-icon-inactive")
        self.revert_icon.set_text("")
        revert_icon_box.add(self.revert_icon)
        self.revert_box.add(revert_icon_box)
        self.revert_box.connect("enter-notify-event", self.app.event_handler.global_options_on_box_enter, self.revert_box, self.revert_icon, "revert-icon-box-active")
        self.revert_box.connect("leave-notify-event", self.app.event_handler.global_options_on_box_leave, self.revert_box, self.revert_icon, "revert-icon-inactive")
        self.revert_box.connect("button-press-event", self.app.event_handler.revert_config)

        self.save_box = Gtk.EventBox()
        self.save_box.set_name("global-options-icon-box-inactive")
        save_icon_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        save_icon_box.get_style_context().add_class("global-options-icon-box")
        self.save_icon = Gtk.Label()
        self.save_icon.get_style_context().add_class("global-options-icon")
        self.save_icon.set_name("save-icon-inactive")
        self.save_icon.set_text("")
        save_icon_box.add(self.save_icon)
        self.save_box.add(save_icon_box)
        self.save_box.connect("enter-notify-event", self.app.event_handler.global_options_on_box_enter, self.save_box, self.save_icon, "save-icon-box-active")
        self.save_box.connect("leave-notify-event", self.app.event_handler.global_options_on_box_leave, self.save_box, self.save_icon, "save-icon-inactive")
        self.save_box.connect("button-press-event", self.app.event_handler.save_config)

        self.global_options_box.pack_start(self.quit_box, True, True, 0)
        self.global_options_box.pack_start(self.revert_box, True, True, 0)
        self.global_options_box.pack_start(self.save_box, True, True, 0)