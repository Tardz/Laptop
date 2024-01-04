import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class General:
    def __init__(self, content, app):
        self.content = content
        self.app = app

        self.general_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.app.list_elements[2]["box"] = self.general_content_box