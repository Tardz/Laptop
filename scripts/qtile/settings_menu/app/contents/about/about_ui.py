import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class About:
    def __init__(self, content, app):
        self.content = content
        self.app = app

        self.about_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.app.list_elements[0]["box"] = self.about_content_box
        self.content.active_content_box = self.about_content_box

        self.content.main_content_scrolled_window.add(self.about_content_box)
