import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from contents.about.about_ui import About
from contents.themes.themes_ui import Themes
from contents.general.general_ui import General
from contents.qtile.qtile_ui import Qtile
from contents.power.power_ui import Power
from contents.security.security_ui import Security
from contents.wifi.wifi_ui import Wifi
from contents.bluetooth.bluetooth_ui import Bluetooth
from contents.sound.sound_ui import Sound

class Content:
    def __init__(self, app):
        self.app = app
        self.switches = []
        self.switch_descs = []
        self.original_focus_desc = None
        self.active_content_box = None

        self.main_content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.main_content_box.get_style_context().add_class("main-content-box")

        self.main_content_scrolled_window = Gtk.ScrolledWindow()
        self.main_content_scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.create_title()
        self.about = About(self, app)
        self.themes = Themes(self, app)
        self.general = General(self, app)
        self.qtile = Qtile(self, app)
        self.power = Power(self, app)
        self.security = Security(self, app)
        self.wifi = Wifi(self, app)
        self.bluetooth = Bluetooth(self, app)
        self.sound = Sound(self, app)

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

    def create_new_switch(self, title, desc_status, main_switch_box):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        box.get_style_context().add_class("switch-box")
        switch = Gtk.Switch()    
        switch.set_active(self.app.qtile_data[desc_status])
        switch.get_style_context().add_class("switch")    
        self.switches.append([switch, desc_status])
        desc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2) 
        desc_box.get_style_context().add_class("sub-content-desc-box")
        desc_title = Gtk.Label()
        desc_title.set_halign(Gtk.Align.START)
        desc_title.get_style_context().add_class("sub-content-desc-title")
        desc_title.set_text(title)
        desc = Gtk.Label()
        self.switch_descs.append([desc, desc_status])
        desc.set_halign(Gtk.Align.START)
        desc.get_style_context().add_class("sub-content-desc")
        if self.app.qtile_data[desc_status]:
            desc.set_text("On")
            desc.set_name("sub-content-desc-active")
        else:
            desc.set_text("Off")
            desc.set_name("sub-content-desc-inactive")
        desc_box.pack_start(desc_title, False, False, 0)
        desc_box.pack_start(desc, False, False, 0)
        box.pack_start(switch, False, False, 0)
        box.pack_start(desc_box, False, False, 0)

        main_switch_box.pack_start(box, False, False, 0)
        switch.connect("state-set", self.app.event_handler.on_qtile_switch_state_changed, desc, desc_status)

        return box