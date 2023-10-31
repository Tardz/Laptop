import gi
gi.require_version('Gtk', '3.0')
import subprocess
import os
from Xlib import display 
from gi.repository import Gtk, Gdk, GLib

class Power_managment_menu(Gtk.Dialog):
    def __init__(self):
        self.pid_file = "/home/jonalm/scripts/qtile/bar_menus/power_managment_pid_file.pid"
        Gtk.Dialog.__init__(self, "Custom Dialog", None, 0)
        self.set_default_size(400, 60)

        x, y = self.get_mouse_position()

        if x and y:
            self.move(x - 190, y - 50)

        self.connect("focus-out-event", self.on_focus_out)
        self.connect("key-press-event", self.on_escape_press)

        
        self.content_area = self.get_content_area()

        self.css()
        self.buttons()
        self.charge_limit()

        self.content_area.pack_start(self.charge_main_box, True, True, 0)
        self.content_area.pack_start(self.options_main_box, True, True, 0)
        self.content_area.set_name("root")
        self.set_name("root")
        
        self.show_all()

    def charge_limit(self):
        self.charge_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.charge_main_box.set_name("charge-main-box")

        charge_left_box = Gtk.EventBox()
        charge_left_box.set_name("charge-box")

        charge_title = Gtk.Label()
        charge_title.set_text("Charge")
        charge_title.set_name("slider-title")
        charge_title.set_halign(Gtk.Align.START)

        charge_middle_box = Gtk.EventBox()
        charge_middle_box.set_name("charge-box")

        charge_adjustment = Gtk.Adjustment(value=self.get_charge_limit(), lower=50, upper=100, step_increment=10, page_increment=10)
        charge_scale = Gtk.HScale.new(charge_adjustment)
        charge_scale.set_digits(0)
        charge_scale.set_draw_value(False)

        charge_right_box = Gtk.EventBox()
        charge_right_box.set_name("charge-box")
                
        self.charge_percentage = Gtk.Label()
        self.charge_percentage.set_name("charge-percentage")
        self.charge_percentage.set_text(str(self.get_charge_limit()) + "%")
        self.charge_percentage.set_halign(Gtk.Align.START)

        charge_left_box.add(charge_title)
        charge_middle_box.add(charge_scale)
        charge_right_box.add(self.charge_percentage)
        
        self.charge_main_box.pack_start(charge_left_box, False, False, 0)
        self.charge_main_box.pack_start(charge_middle_box, True, True, 0)
        self.charge_main_box.pack_start(charge_right_box, False, True, 0)

        charge_scale.connect("value-changed", self.update_display_value)        

    def buttons(self):
        self.options_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        automatic_box = Gtk.EventBox()
        automatic_box.set_name("option-box-inactive")
        automatic_box.connect("enter-notify-event", self.on_mouse_enter)
        automatic_box.connect("enter-notify-event", self.on_mouse_leave)

        automatic_button = Gtk.Label()
        automatic_button.set_text("Automatic")
        automatic_button.connect("button-press-event", self.automatic_clicked)
        automatic_button.set_name("option-button-inactive")

        powersave_box = Gtk.EventBox()
        powersave_box.set_name("option-box-inactive")
        powersave_box.connect("leave-notify-event", self.on_mouse_enter)
        powersave_box.connect("leave-notify-event", self.on_mouse_leave)

        powersave_button = Gtk.Label()
        powersave_button.set_text("Powersave")
        powersave_button.connect("button-press-event", self.powersave_clicked)
        powersave_button.set_name("option-button-inactive")     

        performance_box = Gtk.EventBox()
        performance_box.set_name("option-box-inactive")
        performance_box.connect("leave-notify-event", self.on_mouse_enter)
        performance_box.connect("leave-notify-event", self.on_mouse_leave)

        performance_button = Gtk.Label()
        performance_button.set_text("Performance")
        performance_button.connect("button-press-event", self.performance_clicked)

        performance_button.set_name("option-button-inactive")

        option = self.read_option_from_file()

        if option == "nor":
            automatic_button.set_name("option-button-active")       
            automatic_box.set_name("option-box-active")     
        elif option == "powersave":
            powersave_button.set_name("option-button-active")
            powersave_box.set_name("option-box-active")     
        elif option == "performance":
            performance_button.set_name("option-button-active")
            performance_box.set_name("option-box-active")     

        automatic_box.add(automatic_button)
        powersave_box.add(powersave_button)
        performance_box.add(performance_button)

        self.options_main_box.pack_start(automatic_box, True, True, 0)
        self.options_main_box.pack_start(powersave_box, True, True, 0)
        self.options_main_box.pack_start(performance_box, True, True, 0)

        automatic_box.connect("button-press-event", self.automatic_clicked)
        powersave_box.connect("button-press-event", self.powersave_clicked)
        performance_box.connect("button-press-event", self.performance_clicked)

    def css(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        provider.load_from_path("/home/jonalm/scripts/qtile/bar_menus/power_managment_styles.css")
        visual = screen.get_rgba_visual()
        self.content_area.set_visual(visual)
        self.set_visual(visual)

    def update_display_value(self, widget):
        value = int(widget.get_value())
        self.charge_percentage.set_text(str(value) + "%")
        
    def get_charge_limit(self):
        charge_limit_line = subprocess.check_output("cat /etc/asusd/asusd.ron | grep bat_charge_limit", shell=True, stderr=subprocess.PIPE, text=True).strip()
        start_index = charge_limit_line.find("bat_charge_limit: ")
        charge_limit = None

        if start_index != -1:
            charge_limit_str = charge_limit_line[start_index + len("bat_charge_limit: "):].strip()
            charge_limit = int(charge_limit_str.rstrip(','))

        return charge_limit

    def get_mouse_position(self):
        try:
            d = display.Display()
            s = d.screen()
            root = s.root
            root.change_attributes(event_mask=0x10000)
            pointer = root.query_pointer()
            x, y = pointer.root_x, pointer.root_y
            return x, y
        except Exception:
            return None, None
        
    def on_mouse_enter(self, widget, event):
        widget.add_css_class("option-box-hover")

    def on_mouse_leave(self, widget, event):
        widget.remove_css_class("option-box-inactive")

    def read_option_from_file(self):
        try:
            with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor", "r") as file:
                option = file.read().strip()
                return option
        except FileNotFoundError:
            return ""

    def automatic_clicked(self, widget, event):
        subprocess.call(["sudo auto-cpufreq --force=reset"], shell=True)
        self.exit_remove_pid()        

    def powersave_clicked(self, widget, event):
        subprocess.call(["sudo auto-cpufreq --force=powersave"], shell=True)
        self.exit_remove_pid()

    def performance_clicked(self, widget, event):
        subprocess.call(["sudo auto-cpufreq --force=performance"], shell=True)
        subprocess.call(["notify-send -a $current_time -u low -t 3000 'Search option added' 'Option: <span foreground='#a3be8c' size='medium'>$WebName</span>'"], shell=True)
        self.exit_remove_pid()

    def on_focus_out(self, widget, event):
        modified_value = self.charge_percentage.get_text().replace("%", "")
        subprocess.run(["asusctl", "-c", modified_value]) 
        self.exit_remove_pid()

    def on_escape_press(self, widget, event):
        keyval = event.keyval
        if keyval == Gdk.KEY_Escape or keyval == Gdk.KEY_Escape_L:
            self.on_focus_out(widget, event)

    def exit_remove_pid(self):
        pid = None
        try:
            with open(self.pid_file, "r") as file:
                pid = int(file.read().strip())
            try:
                os.remove(self.pid_file)
                os.kill(pid, 15)
            except ProcessLookupError:
                pass
        finally:
            exit(0)

pid_file = "/home/jonalm/scripts/qtile/bar_menus/power_managment_pid_file.pid"
dialog = None

try:
    if os.path.isfile(pid_file):
        with open(pid_file, "r") as file:
            pid = int(file.read().strip())
        try:
            os.remove(pid_file)
            os.kill(pid, 15)            
        except ProcessLookupError:
            pass
    else:
        with open(pid_file, "w") as file:
            file.write(str(os.getpid()))
        dialog = Power_managment_menu()    
        Gtk.main()
except Exception as e:
    print(f"An error occurred: {e}")
