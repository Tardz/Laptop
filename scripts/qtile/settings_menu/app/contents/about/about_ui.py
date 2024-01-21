import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class About:
    def __init__(self, content, app):
        self.content = content
        self.app = app
        self.about_content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        self.create_project_info()
        self.create_custom_menus()
        self.create_future_plans()
        self.create_version()


        self.app.list_elements[0]["box"] = self.about_content_box
        self.content.active_content_box = self.about_content_box

        self.content.main_content_scrolled_window.add(self.about_content_box)
    
    def create_project_info(self):
        info_card_title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        info_card_title_box.get_style_context().add_class("sub-content-title-box")

        title = Gtk.Label()
        title.get_style_context().add_class("sub-content-title")
        title.set_text("Project info")
        
        info_card_title_box.pack_start(title, False, False, 0)

        info_card_desc_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        info_card_desc_box.get_style_context().add_class("sub-content-desc-box")

        desc = Gtk.Label()
        desc.get_style_context().add_class("sub-content-desc")
        desc.set_text(
            "The goal of this project is to create a more integrated experience \n" + 
            "with qtile and other configurable software on Arch Linux. This is\n" + 
            "done by modififying the configuration files to obtain variables \n" +
            "from the json data generated from the settings menu. This allows\n" + 
            "us to configure the different software directly from the settings \n" +
            "menu." +
            "\n\n" + 
            "The settings menu acts as a bridge between different software which \n" + 
            "I personally use on my machine. Software like Alacritty, Dunst, Rofi\n" + 
            "and more."
            )
        
        info_card_desc_box.pack_start(desc, False, False, 0)

        self.about_content_box.pack_start(info_card_title_box, False, False, 0)
        self.about_content_box.pack_start(info_card_desc_box, False, False, 0)
        
    def create_custom_menus(self):
        info_card_title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        info_card_title_box.get_style_context().add_class("sub-content-title-box")

        title = Gtk.Label()
        title.get_style_context().add_class("sub-content-title")
        title.set_text("Custom menus")
        
        info_card_title_box.pack_start(title, False, False, 0)

        info_card_desc_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        info_card_desc_box.get_style_context().add_class("sub-content-desc-box")

        desc = Gtk.Label()
        desc.get_style_context().add_class("sub-content-desc")
        desc.set_text(
            "Another part of this project is the custom menus for the bar. Menus \n" + 
            "currently available are bluetooth, wifi, sound and power. All of\n" + 
            "these menus are linked to the icons within the qtile bar. The plan\n" +
            "is to make these menus customizable from the settings menu just like\n" +
            "the configuration files."
            )
        
        info_card_desc_box.pack_start(desc, False, False, 0)

        self.about_content_box.pack_start(info_card_title_box, False, False, 0)
        self.about_content_box.pack_start(info_card_desc_box, False, False, 0)

    def create_future_plans(self):
        info_card_title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        info_card_title_box.get_style_context().add_class("sub-content-title-box")

        title = Gtk.Label()
        title.get_style_context().add_class("sub-content-title")
        title.set_text("Future plans")
        
        info_card_title_box.pack_start(title, False, False, 0)

        info_card_desc_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        info_card_desc_box.get_style_context().add_class("sub-content-desc-box")

        desc = Gtk.Label()
        desc.get_style_context().add_class("sub-content-desc")
        desc.set_text(
            "Integrate more software into the settings menu and expand on the \n" + 
            "GUI bar configuration in qtile."
            )
        
        info_card_desc_box.pack_start(desc, False, False, 0)

        self.about_content_box.pack_start(info_card_title_box, False, False, 0)
        self.about_content_box.pack_start(info_card_desc_box, False, False, 0)
        
    def create_version(self):
        info_card_title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        info_card_title_box.get_style_context().add_class("sub-content-title-box")

        title = Gtk.Label()
        title.get_style_context().add_class("sub-content-title")
        title.set_text("Version")
        
        info_card_title_box.pack_start(title, False, False, 0)

        info_card_desc_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        info_card_desc_box.get_style_context().add_class("sub-content-desc-box")

        desc = Gtk.Label()
        desc.get_style_context().add_class("sub-content-desc")
        desc.set_text(
            "1.0 2024-01-20 By Jonathan Almstedt [Tardz]"
            )
        
        info_card_desc_box.pack_start(desc, False, False, 0)

        self.about_content_box.pack_start(info_card_title_box, False, False, 0)
        self.about_content_box.pack_start(info_card_desc_box, False, False, 0)