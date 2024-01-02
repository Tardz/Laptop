import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Content:
    def __init__(self, app):
        self.app = app
        self.switches = []
        self.switch_descs = []
        self.original_focus_desc = None

        self.main_content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.main_content_box.get_style_context().add_class("main-content-box")

        self.main_content_scrolled_window = Gtk.ScrolledWindow()
        self.main_content_scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.create_title()
        self.create_about()
        self.create_themes()
        self.create_general()
        self.create_qtile()
        self.create_power()
        self.create_security()
        self.create_wifi()
        self.create_bluetooth()
        self.create_sound()

        self.main_content_scrolled_window.add(self.about_content_box)
        self.main_content_box.pack_start(self.content_title_box, False, False, 0)
        self.main_content_box.pack_start(self.main_content_scrolled_window, True, True, 0)

        self.main_content_box.set_size_request(500, -1)

    def create_title(self):
        self.content_title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.content_title_box.get_style_context().add_class("content-title-box")
        self.content_title = Gtk.Label()
        self.content_title.get_style_context().add_class("content-title")
        self.content_title.set_text("About")
        self.content_title.set_halign(Gtk.Align.START)

        self.content_icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.content_icon_box.get_style_context().add_class("content-icon-box")
        self.content_icon_box.set_name("about-box")
        self.content_icon = Gtk.Label()
        self.content_icon.get_style_context().add_class("general-icon")
        self.content_icon.set_name("about-content-icon")
        self.content_icon.set_text("")
        self.content_icon.set_halign(Gtk.Align.START)
        self.content_icon_box.add(self.content_icon)

        self.content_title_box.pack_start(self.content_icon_box, False, False, 0)
        self.content_title_box.pack_start(self.content_title, False, False, 0)

    def create_about(self):
        self.about_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.active_content_box = self.about_content_box
        self.app.list_elements[0]["box"] = self.about_content_box

    def create_themes(self):
        self.themes_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.app.list_elements[1]["box"] = self.themes_content_box
    
    def create_general(self):
        self.general_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.app.list_elements[2]["box"] = self.general_content_box

    def create_qtile(self):
        self.qtile_content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.app.list_elements[3]["box"] = self.qtile_content_box

        self.create_qtile_bar_options()
        self.create_qtile_mouse_settings()
        self.create_qtile_window_settings()
        self.create_qtile_general_settings()

        self.qtile_content_box.set_size_request(20, -1)
        
    def create_qtile_bar_options(self):
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

        for i, switch in enumerate(switch_list):
            new_switch = self.create_new_switch(switch[0], switch[1], switch[2])
            # if i%2 == 0:
            box.pack_start(new_switch, False, False, 0)
        
        self.qtile_content_box.pack_start(title_box, False, False, 0)
        box.pack_start(switch_box_1, False, False, 0)
        self.qtile_content_box.pack_start(box, False, False, 0)

    def create_qtile_mouse_settings(self):
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

        for i, switch in enumerate(switch_list):
            new_switch = self.create_new_switch(switch[0], switch[1], switch[2])
            if i%2 == 0:
                box.pack_start(new_switch, False, False, 0)
        
        self.qtile_content_box.pack_start(title_box, False, False, 0)
        box.pack_start(switch_box_1, False, False, 0)
        box.pack_start(switch_box_2, False, False, 0)
        self.qtile_content_box.pack_start(box, False, False, 0)

    def create_qtile_window_settings(self):
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

        for i, switch in enumerate(switch_list):
            new_switch = self.create_new_switch(switch[0], switch[1], switch[2])
            if i%2 == 0:
                box.pack_start(new_switch, False, False, 0)


        focus_on_window_activation_title = Gtk.Label()
        focus_on_window_activation_title.get_style_context().add_class("focus-title")
        focus_on_window_activation_title.set_halign(Gtk.Align.START)
        focus_on_window_activation_title.set_text("Focus on window activation")

        desc_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        desc_box.get_style_context().add_class("focus-box")

        box_1 = Gtk.EventBox()
        focus_on_window_activation_desc_1 = Gtk.Label()
        focus_on_window_activation_desc_1.get_style_context().add_class("focus")
        focus_on_window_activation_desc_1.set_halign(Gtk.Align.START)
        focus_on_window_activation_desc_1.set_text("Smart")
        box_1.add(focus_on_window_activation_desc_1)

        box_2 = Gtk.EventBox()
        focus_on_window_activation_desc_2 = Gtk.Label()
        focus_on_window_activation_desc_2.get_style_context().add_class("focus")
        focus_on_window_activation_desc_2.set_halign(Gtk.Align.START)
        focus_on_window_activation_desc_2.set_text("Focus")
        box_2.add(focus_on_window_activation_desc_2)

        box_3 = Gtk.EventBox()
        focus_on_window_activation_desc_3 = Gtk.Label()
        focus_on_window_activation_desc_3.get_style_context().add_class("focus")
        focus_on_window_activation_desc_3.set_halign(Gtk.Align.START)
        focus_on_window_activation_desc_3.set_text("Never")
        box_3.add(focus_on_window_activation_desc_3)


        if self.app.qtile_data["focus_on_window_activation"] == "smart":
            focus_on_window_activation_desc_1.set_name("focus-active")
            self.active_focus_desc = focus_on_window_activation_desc_1
            self.original_focus_desc = focus_on_window_activation_desc_1
        elif self.app.qtile_data["focus_on_window_activation"] == "focus":
            focus_on_window_activation_desc_2.set_name("focus-active")
            self.active_focus_desc = focus_on_window_activation_desc_2
            self.original_focus_desc = focus_on_window_activation_desc_2
        elif self.app.qtile_data["focus_on_window_activation"] == "never":
            focus_on_window_activation_desc_3.set_name("focus-active")
            self.active_focus_desc = focus_on_window_activation_desc_3
            self.original_focus_desc = focus_on_window_activation_desc_3

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
        self.qtile_content_box.pack_start(focus_on_window_activation_title, False, False, 0)
        self.qtile_content_box.pack_start(desc_box, False, False, 0)
    
    def create_qtile_general_settings(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        title_box.get_style_context().add_class("sub-content-title-box")
        title = Gtk.Label()
        title.get_style_context().add_class("sub-content-title")
        title.set_text("General settings")
        title_box.pack_start(title, False, False, 0)

        box.pack_start(title_box, False, False, 0)

        self.qtile_content_box.pack_start(box, False, False, 0)

    def create_menus(self):
        self.menus_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.app.list_elements[4]["box"] = self.menus_content_box

    def create_notifications(self):
        self.notifications_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.app.list_elements[5]["box"] = self.notifications_content_box

    def create_power(self):
        self.power_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.app.list_elements[6]["box"] = self.power_content_box
    
    def create_display(self):
        self.display_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.app.list_elements[7]["box"] = self.display_content_box
    
    def create_backlight(self):
        self.backlight_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.app.list_elements[8]["box"] = self.backlight_content_box

    def create_security(self):
        self.security_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.app.list_elements[9]["box"] = self.security_content_box

    def create_wifi(self):
        self.wifi_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.app.list_elements[10]["box"] = self.wifi_content_box

    def create_bluetooth(self):
        self.bluetooth_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.app.list_elements[11]["box"] = self.bluetooth_content_box

    def create_sound(self):
        self.sound_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.app.list_elements[12]["box"] = self.sound_content_box

    def create_new_switch(self, title, desc_status, main_switch_box):
        switch_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        switch_box.get_style_context().add_class("switch-box")
        switch = Gtk.Switch()    
        switch.set_active(self.app.qtile_data[desc_status])
        switch.get_style_context().add_class("switch")    
        self.switches.append([switch, desc_status])
        switch_desc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2) 
        switch_desc_box.get_style_context().add_class("sub-content-desc-box")
        switch_desc_title = Gtk.Label()
        switch_desc_title.set_halign(Gtk.Align.START)
        switch_desc_title.get_style_context().add_class("sub-content-desc-title")
        switch_desc_title.set_text(title)
        switch_desc = Gtk.Label()
        self.switch_descs.append([switch_desc, desc_status])
        switch_desc.set_halign(Gtk.Align.START)
        switch_desc.get_style_context().add_class("sub-content-desc")
        if self.app.qtile_data[desc_status]:
            switch_desc.set_text("On")
            switch_desc.set_name("sub-content-desc-active")
        else:
            switch_desc.set_text("Off")
            switch_desc.set_name("sub-content-desc-inactive")
        switch_desc_box.pack_start(switch_desc_title, False, False, 0)
        switch_desc_box.pack_start(switch_desc, False, False, 0)
        switch_box.pack_start(switch, False, False, 0)
        switch_box.pack_start(switch_desc_box, False, False, 0)

        main_switch_box.pack_start(switch_box, False, False, 0)
        switch.connect("state-set", self.app.event_handler.on_qtile_switch_state_changed, switch_desc, desc_status)

        return switch_box