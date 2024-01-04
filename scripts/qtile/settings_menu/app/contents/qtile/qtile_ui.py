import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Qtile:
    def __init__(self, content, app):
        self.content = content
        self.app = app

        self.qtile_content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.app.list_elements[3]["box"] = self.qtile_content_box

        # self.create_version()
        self.create_bar_options()
        self.create_mouse_settings()
        self.create_window_settings()
        self.create_general_settings()

    def create_version(self):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        title_box.get_style_context().add_class("sub-content-title-box")
        title = Gtk.Label()
        title.get_style_context().add_class("sub-content-title")
        title.set_text("Qtile version options")
        title_box.pack_start(title, False, False, 0)

        desc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2) 
        desc_box.get_style_context().add_class("sub-content-desc-box")
        desc_title = Gtk.Label()
        desc_title.set_halign(Gtk.Align.START)
        desc_title.get_style_context().add_class("sub-content-desc-title")
        desc_title.set_text("Version")
        desc = Gtk.Label()
        desc.set_halign(Gtk.Align.START)
        desc.get_style_context().add_class("sub-content-desc")
        desc.set_text("On")
        desc.set_name("sub-content-desc-active")

        desc_box.pack_start(desc_title, False, False, 0)
        desc_box.pack_start(desc, False, False, 0)

        self.qtile_content_box.pack_start(title_box, False, False, 0)
        self.qtile_content_box.pack_start(desc_box, False, False, 0)
        self.qtile_content_box.pack_start(box, False, False, 0)

    def create_bar_options(self):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        title_box.get_style_context().add_class("sub-content-title-box")
        title = Gtk.Label()
        title.get_style_context().add_class("sub-content-title")
        title.set_text("Bar Options")
        title_box.pack_start(title, False, False, 0)

        switch_box_1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        switch_list = [
            ["Top bar             ", "top_bar_status", switch_box_1],
            ["Bottom bar", "bottom_bar_status", switch_box_1],
        ]

        for switch in switch_list:
            new_switch = self.content.create_new_switch(switch[0], switch[1], switch[2])
            box.pack_start(new_switch, False, False, 0)
        
        self.qtile_content_box.pack_start(title_box, False, False, 0)
        box.pack_start(switch_box_1, False, False, 0)
        self.qtile_content_box.pack_start(box, False, False, 0)

    def create_mouse_settings(self):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        title_box.get_style_context().add_class("sub-content-title-box")
        title = Gtk.Label()
        title.get_style_context().add_class("sub-content-title")
        title.set_text("Focus settings")
        title_box.pack_start(title, False, False, 0)

        
        switch_box_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        switch_box_2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        switch_list = [
            ["Follow mouse focus", "follow_mouse_focus", switch_box_1],
            ["Bring front on click", "bring_front_click", switch_box_1],
            ["Cursor wrap", "cursor_warp", switch_box_2],
        ]

        for switch in switch_list:
            new_switch = self.content.create_new_switch(switch[0], switch[1], switch[2])
            box.pack_start(new_switch, False, False, 0)
        
        self.qtile_content_box.pack_start(title_box, False, False, 0)
        box.pack_start(switch_box_1, False, False, 0)
        box.pack_start(switch_box_2, False, False, 0)
        self.qtile_content_box.pack_start(box, False, False, 0)

    def create_window_settings(self):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        title_box.get_style_context().add_class("sub-content-title-box")
        title = Gtk.Label()
        title.get_style_context().add_class("sub-content-title")
        title.set_text("Window settings")
        title_box.pack_start(title, False, False, 0)

        switch_box_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        switch_box_2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        switch_list = [
            ["Auto fullscreen     ", "auto_fullscreen", switch_box_1],
            ["Auto minimize       ", "auto_minimize", switch_box_1],
            ["Reconfigure screens", "reconfigure_screens", switch_box_2],
            ["Scratchpad focus", "scratchpad_focus_value", switch_box_2],
        ]

        for switch in switch_list:
            new_switch = self.content.create_new_switch(switch[0], switch[1], switch[2])
            box.pack_start(new_switch, False, False, 0)

        focus_title = Gtk.Label()
        focus_title.get_style_context().add_class("focus-title")
        focus_title.set_halign(Gtk.Align.START)
        focus_title.set_text("Focus on window activation")

        desc_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        desc_box.get_style_context().add_class("focus-box")

        box_1 = Gtk.EventBox()
        desc_1 = Gtk.Label()
        desc_1.get_style_context().add_class("focus")
        desc_1.set_halign(Gtk.Align.START)
        desc_1.set_text("Smart")
        box_1.add(desc_1)

        box_2 = Gtk.EventBox()
        desc_2 = Gtk.Label()
        desc_2.get_style_context().add_class("focus")
        desc_2.set_halign(Gtk.Align.START)
        desc_2.set_text("Focus")
        box_2.add(desc_2)

        box_3 = Gtk.EventBox()
        desc_3 = Gtk.Label()
        desc_3.get_style_context().add_class("focus")
        desc_3.set_halign(Gtk.Align.START)
        desc_3.set_text("Never")
        box_3.add(desc_3)

        if self.app.qtile_data["focus_on_window_activation"] == "smart":
            desc_1.set_name("focus-active")
            self.active_focus_desc = desc_1
            self.original_focus_desc = desc_1
        elif self.app.qtile_data["focus_on_window_activation"] == "focus":
            desc_2.set_name("focus-active")
            self.active_focus_desc = desc_2
            self.original_focus_desc = desc_2
        elif self.app.qtile_data["focus_on_window_activation"] == "never":
            desc_3.set_name("focus-active")
            self.active_focus_desc = desc_3
            self.original_focus_desc = desc_3

        box_1.connect("button-press-event", self.app.event_handler.on_focus_clicked, "smart")
        box_2.connect("button-press-event", self.app.event_handler.on_focus_clicked, "focus")
        box_3.connect("button-press-event", self.app.event_handler.on_focus_clicked, "never")

        desc_box.pack_start(box_1, False, False, 0)
        desc_box.pack_start(box_2, False, False, 0)
        desc_box.pack_start(box_3, False, False, 0)
        
        self.qtile_content_box.pack_start(title_box, False, False, 0)
        box.pack_start(switch_box_1, False, False, 0)
        box.pack_start(switch_box_2, False, False, 0)
        self.qtile_content_box.pack_start(box, False, False, 0)
        self.qtile_content_box.pack_start(focus_title, False, False, 0)
        self.qtile_content_box.pack_start(desc_box, False, False, 0)
    
    def create_general_settings(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        title_box.get_style_context().add_class("sub-content-title-box")
        title = Gtk.Label()
        title.get_style_context().add_class("sub-content-title")
        title.set_text("General settings")
        title_box.pack_start(title, False, False, 0)

        box.pack_start(title_box, False, False, 0)

        self.qtile_content_box.pack_start(box, False, False, 0)
