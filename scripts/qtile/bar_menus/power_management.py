import gi
gi.require_version('Gtk', '3.0')
import subprocess
from gi.repository import Gtk, Gdk

class CustomDialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self, "Custom Dialog", None, 0)
        self.set_default_size(100, 40)
        self.move(1985, 0)  # Set the x and y position
        self.connect("focus-out-event", self.on_focus_out)

        option = self.read_option_from_file()

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        # Create buttons with different styles
        powersave_button = Gtk.Button("Powersave")
        powersave_button.connect("clicked", self.on_powersave_button_clicked)
        style = powersave_button.get_style_context()
        style.add_class("powersave")
        powersave_button.set_hexpand(True)
        powersave_button.set_vexpand(True)
        
        performance_button = Gtk.Button("Performance")
        performance_button.connect("clicked", self.on_performance_button_clicked)
        style = performance_button.get_style_context()
        style.add_class("performance")
        performance_button.set_hexpand(True)
        performance_button.set_vexpand(True)

        if option == "powersave":
            self.set_button_style(powersave_button, "#4f586e")
        else:
            self.set_button_style(performance_button, "#4f586e")

        # Add buttons to the dialog
        hbox.pack_start(powersave_button, True, True, 0)
        hbox.pack_start(performance_button, True, True, 0)
        
        content_area = self.get_content_area()
        content_area.add(hbox)

        self.show_all()

    def read_option_from_file(self):
        try:
            with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor", "r") as file:
                option = file.read().strip()
                return option
        except FileNotFoundError:
            return ""
        
    def set_button_style(self, button, color):
        css = f"button {{ background-color: {color}; }}"
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css.encode())
        context = button.get_style_context()
        context.add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def on_powersave_button_clicked(self, button):
        subprocess.call(["sudo auto-cpufreq --force=powersave"], shell=True)
        self.hide()

    def on_performance_button_clicked(self, button):
        subprocess.call(["sudo auto-cpufreq --force=performance"], shell=True)
        self.hide()

    def on_focus_out(self, widget, event):
        self.destroy()

### fix toggle ###
##################
dialog = CustomDialog()
Gtk.main()






