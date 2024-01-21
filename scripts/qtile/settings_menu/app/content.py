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
        self.create_overlay_options()
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

        self.overlay = Gtk.Overlay()
        self.overlay.add(self.main_content_box)
        self.overlay.add_overlay(self.overlay_options_box)

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
        desc_box.get_style_context().add_class("switch-desc-box")
        desc_title = Gtk.Label()
        desc_title.set_halign(Gtk.Align.START)
        desc_title.get_style_context().add_class("switch-desc-title")
        desc_title.set_text(title)
        desc = Gtk.Label()
        self.switch_descs.append([desc, desc_status])
        desc.set_halign(Gtk.Align.START)
        desc.get_style_context().add_class("switch-desc")
        if self.app.qtile_data[desc_status]:
            desc.set_text("On")
            desc.set_name("switch-desc-active")
        else:
            desc.set_text("Off")
            desc.set_name("switch-desc-inactive")
        desc_box.pack_start(desc_title, False, False, 0)
        desc_box.pack_start(desc, False, False, 0)
        box.pack_start(switch, False, False, 0)
        box.pack_start(desc_box, False, False, 0)

        main_switch_box.pack_start(box, False, False, 0)
        switch.connect("state-set", self.app.event_handler.on_qtile_switch_state_changed, desc, desc_status)

        return box
    
    def create_overlay_options(self):
        self.overlay_options_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.overlay_options_box.get_style_context().add_class("overlay-box")
        self.overlay_options_box.set_valign(Gtk.Align.END)
        self.overlay_options_box.set_halign(Gtk.Align.END)

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

        self.profile_box = Gtk.EventBox()
        self.profile_box.set_name("global-options-icon-box-inactive")
        profile_icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        profile_icon_box.get_style_context().add_class("global-options-icon-box")
        self.profile_icon = Gtk.Label()
        self.profile_icon.get_style_context().add_class("global-options-icon")
        self.profile_icon.set_name("save-icon-inactive")
        self.profile_icon.set_text("")
        self.profile_name = Gtk.Label()
        self.profile_name.get_style_context().add_class("profile-name")
        self.profile_name.set_text("Simple bar")
        profile_icon_box.add(self.profile_icon)
        profile_icon_box.add(self.profile_name)
        self.profile_box.add(profile_icon_box)
        self.profile_box.connect("enter-notify-event", self.app.event_handler.global_options_on_box_enter, self.profile_box, self.profile_icon, "save-icon-box-active")
        self.profile_box.connect("leave-notify-event", self.app.event_handler.global_options_on_box_leave, self.profile_box, self.profile_icon, "save-icon-inactive")
        # self.profile_box.connect("button-press-event", self.app.event_handler.save_config)

        self.overlay_options_box.pack_start(self.revert_box, True, True, 0)
        self.overlay_options_box.pack_start(self.save_box, True, True, 0)
        self.overlay_options_box.pack_start(self.profile_box, True, True, 0)
        self.overlay_options_box.pack_start(self.quit_box, True, True, 0)