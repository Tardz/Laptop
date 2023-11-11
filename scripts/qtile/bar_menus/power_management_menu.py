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
            self.move(x - 190, y - 18)

        self.connect("focus-out-event", self.on_focus_out)
        self.connect("key-press-event", self.on_escape_press)

        self.inital_charge_limit = self.get_charge_limit()
        
        self.content_area = self.get_content_area()

        self.css()
        self.buttons()
        self.charge_limit()

        self.content_area.pack_start(self.options_main_box, True, True, 0)
        self.content_area.pack_start(self.charge_main_box, True, True, 0)
        self.content_area.set_name("root")
        self.set_name("root-root")
        
        self.show_all()

    def charge_limit(self):
        self.charge_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.charge_main_box.set_name("charge-main-box")

        charge_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        charge_title_box = Gtk.EventBox()
        charge_title_box.set_name("charge-box")

        charge_title = Gtk.Label()
        charge_title.set_text("Charge limit")
        charge_title.set_name("slider-title")
        charge_title.set_halign(Gtk.Align.START)

        charge_slider_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=7)

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

        charge_title_box.add(charge_title)
        charge_middle_box.add(charge_scale)
        charge_right_box.add(self.charge_percentage)

        charge_slider_box.pack_start(charge_middle_box, True, True, 0)
        charge_slider_box.pack_start(charge_right_box, False, False, 0)

        charge_box.pack_start(charge_title_box, True, True, 0)
        charge_box.pack_start(charge_slider_box, True, True, 0)

        self.charge_main_box.pack_start(charge_box, True, True, 0)

        charge_scale.connect("value-changed", self.update_display_value)

    def buttons(self):
        self.options_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        cpufreq_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        cpufreq_options_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        cpufreq_options_box.set_name("option-box")

        cpufreq_background_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        cpufreq_background_box.set_name("option-root-box")

        cpufreq_title_background_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        cpufreq_title_background_box.set_name("option-root-box")
        cpufreq_title = Gtk.Label()
        cpufreq_title.set_text("Cpu freq")
        cpufreq_title.set_name("option-box-title")
        cpufreq_title.set_halign(Gtk.Align.START)

        self.automatic_box = Gtk.EventBox()
        self.automatic_box.connect("enter-notify-event", self.on_mouse_enter)
        self.automatic_box.connect("enter-notify-event", self.on_mouse_leave)

        self.automatic_button = Gtk.Label()
        self.automatic_button.set_text("Automatic")

        self.powersave_box = Gtk.EventBox()
        self.powersave_box.connect("leave-notify-event", self.on_mouse_enter)
        self.powersave_box.connect("leave-notify-event", self.on_mouse_leave)

        self.powersave_button = Gtk.Label()
        self.powersave_button.set_text("Powersave")

        self.performance_box = Gtk.EventBox()
        self.performance_box.connect("leave-notify-event", self.on_mouse_enter)
        self.performance_box.connect("leave-notify-event", self.on_mouse_leave)

        self.performance_button = Gtk.Label()
        self.performance_button.set_text("Performance")

        self.automatic_box.add(self.automatic_button)
        self.powersave_box.add(self.powersave_button)
        self.performance_box.add(self.performance_button)

        fan_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        fan_options_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        fan_options_box.set_name("option-box")

        fan_background_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        fan_background_box.set_name("option-root-box")

        fan_title_background_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        fan_title_background_box.set_name("option-root-box")
        fan_mode_title = Gtk.Label()
        fan_mode_title.set_text("Fan mode")
        fan_mode_title.set_name("option-box-title")
        fan_mode_title.set_halign(Gtk.Align.START)

        self.quiet_box = Gtk.EventBox()
        self.quiet_box.connect("enter-notify-event", self.on_mouse_enter)
        self.quiet_box.connect("enter-notify-event", self.on_mouse_leave)

        self.quiet_button = Gtk.Label()
        self.quiet_button.set_text("Quiet")

        self.balanced_box = Gtk.EventBox()
        self.balanced_box.connect("leave-notify-event", self.on_mouse_enter)
        self.balanced_box.connect("leave-notify-event", self.on_mouse_leave)

        self.balanced_button = Gtk.Label()
        self.balanced_button.set_text("Balanced")

        self.loud_box = Gtk.EventBox()
        self.loud_box.connect("leave-notify-event", self.on_mouse_enter)
        self.loud_box.connect("leave-notify-event", self.on_mouse_leave)

        self.loud_button = Gtk.Label()
        self.loud_button.set_text("Loud")

        self.quiet_box.add(self.quiet_button)
        self.balanced_box.add(self.balanced_button)
        self.loud_box.add(self.loud_button)

        cpufreq_options_box.pack_start(self.automatic_box, True, True, 0)
        cpufreq_options_box.pack_start(self.powersave_box, True, True, 0)
        cpufreq_options_box.pack_start(self.performance_box, True, True, 0)
        cpufreq_background_box.pack_start(cpufreq_options_box, True, True, 0)

        fan_options_box.pack_start(self.quiet_box, True, True, 0)
        fan_options_box.pack_start(self.balanced_box, True, True, 0)
        fan_options_box.pack_start(self.loud_box, True, True, 0)
        fan_background_box.pack_start(fan_options_box, True, True, 0)

        cpufreq_title_background_box.pack_start(cpufreq_title, False, False, 0)
        cpufreq_box.pack_start(cpufreq_title_background_box, True, True, 0)
        cpufreq_box.pack_start(cpufreq_background_box, True, True, 0)

        fan_title_background_box.pack_start(fan_mode_title, False, False, 0)
        fan_box.pack_start(fan_title_background_box, True, True, 0)
        fan_box.pack_start(fan_background_box, True, True, 0)

        self.options_main_box.pack_start(cpufreq_box, True, True, 0)
        self.options_main_box.pack_start(fan_box, True, True, 0)

        self.automatic_box.connect("button-press-event", self.automatic_clicked)
        self.powersave_box.connect("button-press-event", self.powersave_clicked)
        self.performance_box.connect("button-press-event", self.performance_clicked)

        self.quiet_box.connect("button-press-event", self.quiet_clicked)
        self.balanced_box.connect("button-press-event", self.balanced_clicked)
        self.loud_box.connect("button-press-event", self.loud_clicked)

        self.update_active_cpufreq_button()
        self.update_active_fan_button()

        GLib.timeout_add(5000, self.update_active_cpufreq_button)
        GLib.timeout_add(5000, self.update_active_fan_button)


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

    def update_active_fan_button(self):
        button_list = [
            self.quiet_button,
            self.balanced_button,
            self.loud_button 
        ]
        
        box_list = [
            self.quiet_box,
            self.balanced_box,
            self.loud_box
        ]

        active_button = None
        active_box = None

        fan_mode = self.get_fan_mode()
        if fan_mode == "Quiet":
            active_button = self.quiet_button
            active_box = self.quiet_box
            self.quiet_button.set_name("option-button-active")       
            self.quiet_box.set_name("option-box-active")     
        elif fan_mode == "Balanced":
            active_button = self.balanced_button
            active_box = self.balanced_box
            self.balanced_button.set_name("option-button-active")
            self.balanced_box.set_name("option-box-active")     
        elif fan_mode == "Performance":
            active_button = self.loud_button
            active_box = self.loud_box
            self.loud_button.set_name("option-button-active")
            self.loud_box.set_name("option-box-active")     

        for button in button_list:
            if button != active_button:
                button.set_name("option-button-inactive")

        for box in box_list:
            if box != active_box:
                box.set_name("option-box-inactive")

        return True

    def update_active_cpufreq_button(self):
        button_list = [
            self.automatic_button,
            self.powersave_button,
            self.performance_button 
        ]
        
        box_list = [
            self.automatic_box,
            self.powersave_box,
            self.performance_box
        ]

        active_button = None
        active_box = None

        cpufreq_mode = self.read_cpufreq_mode()

        if cpufreq_mode == "nor":
            active_button = self.automatic_button
            active_box = self.automatic_box
            self.automatic_button.set_name("option-button-active")       
            self.automatic_box.set_name("option-box-active")     
        elif cpufreq_mode == "powersave":
            active_button = self.powersave_button
            active_box = self.powersave_box
            self.powersave_button.set_name("option-button-active")
            self.powersave_box.set_name("option-box-active")     
        elif cpufreq_mode == "performance":
            active_button = self.performance_button
            active_box = self.performance_box
            self.performance_button.set_name("option-button-active")
            self.performance_box.set_name("option-box-active")  

        for button in button_list:
            if button != active_button:
                button.set_name("option-button-inactive")

        for box in box_list:
            if box != active_box:
                box.set_name("option-box-inactive")

        return True
        
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
        pass
        # widget.add_css_class("option-box-hover")

    def on_mouse_leave(self, widget, event):
        pass
        # widget.remove_css_class("option-box-inactive")

    def read_cpufreq_mode(self):
        try:
            with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor", "r") as file:
                option = file.read().strip()
                return option
        except FileNotFoundError:
            return ""
        
    def get_fan_mode(self):
        fan_mode = subprocess.check_output("asusctl profile --profile-get | awk '{print $4}'", shell=True).decode("utf-8").strip()
        return fan_mode

    def automatic_clicked(self, widget, event):
        subprocess.call(["sudo auto-cpufreq --force=reset"], shell=True)
        self.update_active_cpufreq_button()

    def powersave_clicked(self, widget, event):
        subprocess.call(["sudo auto-cpufreq --force=powersave"], shell=True)
        self.update_active_cpufreq_button()

    def performance_clicked(self, widget, event):
        subprocess.call(["sudo auto-cpufreq --force=performance"], shell=True)
        self.update_active_cpufreq_button()

    def quiet_clicked(self, widget, event):
        subprocess.call(["asusctl profile --profile-set quiet"], shell=True)
        self.update_active_fan_button()

    def balanced_clicked(self, widget, event):
        subprocess.call(["asusctl profile --profile-set balanced"], shell=True)
        self.update_active_fan_button()

    def loud_clicked(self, widget, event):
        subprocess.call(["asusctl profile --profile-set performance"], shell=True)
        self.update_active_fan_button()

    def on_focus_out(self, widget, event):
        modified_value = self.charge_percentage.get_text().replace("%", "")
        if self.inital_charge_limit != int(modified_value):
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
