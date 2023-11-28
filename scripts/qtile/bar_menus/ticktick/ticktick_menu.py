import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2
import jsonify

class TicktickMenu(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self, "OAuth2 Authorization", None, 0)

        content_area = self.get_content_area()
        self.webview = WebKit2.WebView()
        content_area.pack_start(self.webview, True, True, 0)

        self.webview.connect("load-changed", self.on_load_changed)

        authorization_url = "http://127.0.0.1:5000/login"  # Replace with your server's IP and port

        self.webview.load_uri(authorization_url)

        self.set_size_request(800, 600)

        self.show_all()

    def on_load_changed(self, webview, event):
        # Check if the page has finished loading
        if event == WebKit2.LoadEvent.FINISHED:
            current_uri = webview.get_uri()
            print(f"Current URI: {current_uri}")

            if "login" in current_uri:
                self.fetch_tasks()

    def fetch_tasks(self):
        import requests

        response = requests.get('http://127.0.0.1:5000/tasks')

        if response.status_code == 200:
            tasks = response.json()
            for task in tasks:
                print(task, "\n")
            # Process tasks as needed in your GTK app
        else:
            print(f"Error: {response.status_code}, {response.text}")

if __name__ == '__main__':
    win = TicktickMenu()
    Gtk.main()
