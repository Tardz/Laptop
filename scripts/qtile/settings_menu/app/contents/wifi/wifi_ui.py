import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Wifi:
    def __init__(self, content, app):
        self.content = content
        self.app = app
        
        self.wifi_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.app.list_elements[10]["box"] = self.wifi_content_box