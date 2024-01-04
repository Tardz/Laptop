import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Sound:
    def __init__(self, content, app):
        self.content = content
        self.app = app

        self.sound_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.app.list_elements[13]["box"] = self.sound_content_box