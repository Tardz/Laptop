from qtile_extras.widget.decorations import BorderDecoration, RectDecoration
from libqtile.command.base import expose_command
from libqtile import qtile as Qtile
from libqtile.widget import base
from qtile_extras import widget
from libqtile.lazy import lazy
from xdg import IconTheme
from settings import *
import subprocess

widget_defaults = dict(
    font        = bold_font,
    fontsize    = widget_default_font_size,
    padding     = widget_default_padding,
    foreground  = widget_default_foreground_color,
)

extension_defaults = widget_defaults.copy()

def seperator(custom_padding=seperator_padding, background=None):
    return widget.Sep(
        background   = background,
        linewidth    = seperator_line_width,
        foreground   = bar_background_color,
        padding      = custom_padding,
        size_percent = 0,
    )

# Default padding_y = 9, Default padding_x = None
def left_decor(color, round=False, padding_x=None, padding_y=left_decor_padding):
    if laptop:
        radius = 6 if round else [4, 0, 0, 4]
    else:    
        radius = 5 if round else [4, 0, 0, 4]
        
    return [
        RectDecoration(
            colour    = color,
            radius    = radius,
            filled    = True,
            padding_x = padding_x,
            padding_y = padding_y,
        )
    ]

def power_button_decor(color, round=True, padding_x=0, padding_y=6):
    radius = 6 if round else [4, 0, 0, 4]
    if not laptop:
        radius = 5
    return [
        RectDecoration(
            colour    = color,
            radius    = radius,
            filled    = True,
            padding_x = padding_x,
            padding_y = padding_y,
        )
    ]

def clicked_decor(color, round=True, padding_x=None, padding_y=left_decor_padding):
    radius = 6 if round else [4, 0, 0, 4]
    if not laptop:
        radius = 5
    return RectDecoration(
            colour    = color,
            radius    = radius,
            filled    = True,
            padding_x = padding_x,
            padding_y = padding_y,
        )

def left_decor_hover(color, round=True, padding_x=2, padding_y=left_decor_padding + 2):
    radius = 6 if round else [4, 0, 0, 4]
    if not laptop:
        radius = 5
    return [
        RectDecoration(
            colour    = color,
            radius    = radius,
            filled    = True,
            padding_x = padding_x,
            padding_y = padding_y,
        )
    ]

def right_decor(color=right_decor_background, round=False, padding_x=0, padding_y=left_decor_padding):
    if laptop:
        radius = 6 if round else [0, 4, 4, 0]
    else:
        radius = 5 if round else [0, 4, 4, 0]
    return [
        RectDecoration(
            colour    = color,
            radius    = radius,
            filled    = True,
            group     = True,
            padding_x = padding_x,
            padding_y = padding_y,
        )
    ]

def active_window_decor(color=right_decor_background, round=True, padding_x=0, padding_y=6):
    if not laptop:
        radius = 5 if round else [0, 4, 4, 0]
    else:
        radius = 6 if round else [0, 4, 4, 0]
    return [
        RectDecoration(
            colour    = color,
            radius    = radius,
            filled    = True,
            group     = True,
            padding_x = padding_x,
            padding_y = padding_y,
        )
    ]

def task_list_decor(color=app_tray_color, radius=12, group=False, padding_x=0, padding_y=0):
    return RectDecoration(
        line_width            = bottom_widget_width,
        line_colour           = bar_border_color,
        colour                = color,
        radius                = radius,
        filled                = True,
        padding_y             = padding_y,
        padding_x             = padding_x,
        group                 = group,
        use_widget_background = False
    )

def icon_decor(color=bar_background_color, border_width=[3, 0, 3, 0]):
    return BorderDecoration(
        border_width = border_width,
        colour = color,
    )

def modify_window_name(text):
    parts = text.split('-')
    cleaned_parts = [part.strip() for part in parts]

    if len(cleaned_parts) >= 2:
        if cleaned_parts[-1] == "Visual Studio Code":
            return f"{cleaned_parts[0]}"
        return f"{cleaned_parts[-1]} - {cleaned_parts[0]}"
    elif len(cleaned_parts) == 1:
        return cleaned_parts[0]
    else:
        return ''

class PowerButton(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text            = "",
            font            = icon_font,
            foreground      = "#000000",
            fontsize        = icon_size + 6,
            padding         = widget_default_padding + 2,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/system/system_menu.py"))},
            decorations     = power_button_decor("#bf616a"),
        )
        
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class LayoutIcon(widget.CurrentLayoutIcon):
    def __init__(self):
        widget.CurrentLayoutIcon.__init__(
            self,
            custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
            scale             = layouticon_scale,
            decorations       = left_decor(icon_background_11),
        )

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class TickTickMenu(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text            = f"<span font='Font Awesome 6 free solid {icon_size}' foreground='{icon_foreground_10}' size='medium'></span>",
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/ticktick/launch.py"))},
            decorations     = left_decor(icon_background_10),
        )
        
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class BluetoothIcon(widget.TextBox, base.InLoopPollText):
    def __init__(self):
        base.InLoopPollText.__init__(
            self,
            # text            = "",
            font            = icon_font,
            fontsize        = icon_size + 8,
            foreground      = icon_foreground_1,
            background      = None,
            padding         = icon_padding + 4,
            update_interval = wifi_update_interval,
            mouse_callbacks = {"Button1": lambda: self.clicked()},
            decorations     = left_decor(round=True, color=icon_background_1),
        )
        self.signal_file_path = os.path.expanduser("~/scripts/qtile/bar_menus/bluetooth/signal_data.txt") 

        self.normal_foreground = self.foreground
        self.clicked_foreground = "#b48ead"

        self.active_background   = bar_border_color
        self.inactive_background = self.background

    def poll(self):
        bluetooth_state = subprocess.check_output("systemctl status bluetooth | grep Running", shell=True, stderr=subprocess.PIPE, text=True).strip()
        if "Running" in bluetooth_state:
            connected_devices_output = subprocess.check_output("bluetoothctl devices Connected", shell=True).decode("utf-8")
            lines = connected_devices_output.splitlines()

            if connected_devices_output:
                lines = connected_devices_output.splitlines()
                parts = lines[0].split(" ", 2)

                device_name = parts[2]

                if "Jonathans Bose QC35 II" in device_name:
                    return ""
                elif device_name == "Jonathans Pods - Find My":
                    return ""
                # elif device_name == "controller available":
                #     return "Error"
                else:
                    return ""
            
            else:
                return ""
            
    def clicked(self):
        global bluetooth_menu_pid
        if not bluetooth_menu_pid:
            Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/bluetooth/bluetooth_menu.py"))
        else:
            with open(self.signal_file_path, "w") as file:
                file.write("hide")
            os.kill(bluetooth_menu_pid, 15)

        self.foreground = self.clicked_foreground
        self.background = self.active_background
        self.bar.draw()

    @expose_command()
    def unclick(self):
        self.foreground = self.normal_foreground
        self.background = self.inactive_background
        self.bar.draw()

    @expose_command()
    def update_menu_pid(self):
        file_path = os.path.expanduser("~/settings_data/processes.json")
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                processes = json.load(file)
        
        global bluetooth_menu_pid
        bluetooth_menu_pid = processes.get("bluetooth_menu_pid", None)
    
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")
        self.bar.draw()

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")
        self.bar.draw()

class BluetoothWidget(widget.TextBox, base.InLoopPollText):
    def __init__(self):
        base.InLoopPollText.__init__(
            self,
            update_interval = wifi_update_interval,
            font            = bold_font,
            fontsize        = widget_default_font_size,
            padding         = widget_default_padding,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/bluetooth/bluetooth_menu.py"))},
            decorations     = right_decor()
        )

    def poll(self):
        try:
            bluetooth_state = subprocess.check_output("systemctl status bluetooth | grep Running", shell=True, stderr=subprocess.PIPE, text=True).strip()
            if "Running" in bluetooth_state:
                connected_devices_output = subprocess.check_output("bluetoothctl devices Connected", shell=True).decode("utf-8")
                lines = connected_devices_output.splitlines()

                if connected_devices_output:
                    lines = connected_devices_output.splitlines()

                    parts = lines[0].split(" ", 2)

                    device_name = parts[2]
                    headphone_icon = "<span font='Font Awesome 6 free solid {icon_size}' foreground='white' size='medium'> </span>"
                    airpods_icon = "<span font='Font Awesome 6 fvree solid 12' foreground='white' size='medium'> </span>"

                    if device_name == "N/A":
                        return
                    elif "Jonathans Bose QC35 II" in device_name:
                        return "Bose"
                    elif device_name == "Jonathans Pods - Find My":
                        return "AirPods"
                    elif device_name == "controller available":
                        return "Error"
                    else:
                        return device_name

        except subprocess.CalledProcessError as e:
            return "Off"

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")
        self.decorations = self.hover_decorator
        self.bar.draw()

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")
        self.decorations = self.normal_decorator
        self.bar.draw()

class VolumeIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text            = "",
            font            = icon_font,
            fontsize        = icon_size + 5,
            foreground      = icon_foreground_2,
            background      = None,
            padding         = icon_padding,
            mouse_callbacks = {"Button1": lambda: self.click()},
            decorations     = left_decor(icon_background_2),
        )

        self.normal_foreground = self.foreground
        self.clicked_foreground = "#9B98B7"

        self.active_background = bar_border_color
        self.inactive_background = self.background
        self.signal_file_path = os.path.expanduser("~/scripts/qtile/bar_menus/volume/signal_data.txt") 

    def click(self):
        global volume_menu_pid
        if not volume_menu_pid:
            Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/volume/volume_menu.py"))
        else:
            with open(self.signal_file_path, "w") as file:
                file.write("hide")
            os.kill(volume_menu_pid, 15)
        
        self.foreground = self.clicked_foreground
        self.background = self.active_background
        self.bar.draw()

    @expose_command()
    def unclick(self):
        self.foreground = self.normal_foreground
        self.background = self.inactive_background
        self.bar.draw()

    @expose_command()
    def update_menu_pid(self):
        file_path = os.path.expanduser("~/settings_data/processes.json")
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                processes = json.load(file)
        
        global volume_menu_pid
        volume_menu_pid = processes.get("volume_menu_pid", None)
        
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class VolumeWidget(widget.PulseVolume):
    def __init__(self):
        widget.PulseVolume.__init__(
            self,
            font = bold_font,
            fontsize = widget_default_font_size,
            padding = widget_default_padding,
            mouse_callbacks = {
                "Button1": lambda: Qtile.cmd_spawn(
                    "python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/volume/volume_menu.py")
                    )
                },
            decorations     = right_decor(),
        )
        
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class WifiIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text            = "",
            font            = icon_font,
            fontsize        = icon_size + 5,
            foreground      = icon_foreground_3,
            rounded         = True,
            mouse_callbacks = {"Button1": lambda: self.clicked()},
            decorations     = left_decor(icon_background_3),
            backgroubd      = None,
            padding         = icon_padding,
        )

        self.normal_foreground = self.foreground
        self.clicked_foreground = "#81A1C1"

        self.active_background = bar_border_color
        self.inactive_background = self.background

    def clicked(self):
        global wifi_menu_pid
        if not wifi_menu_pid:
            Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/wifi/wifi_menu.py"))
        else:
            os.kill(volume_menu_pid, 15)
            
        self.foreground = self.clicked_foreground
        self.background = self.active_background
        self.bar.draw()

    @expose_command()
    def unclick(self):
        self.foreground = self.normal_foreground
        self.background = self.inactive_background
        self.bar.draw()

    @expose_command()
    def update_menu_pid(self):
        file_path = os.path.expanduser("~/settings_data/processes.json")
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                processes = json.load(file)

        global wifi_menu_pid
        wifi_menu_pid = processes.get("wifi_menu_pid", None)
        
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class WifiWidget(widget.TextBox, base.InLoopPollText):
    def __init__(self):
        base.InLoopPollText.__init__(
            self,
            update_interval = wifi_update_interval,
            font            = bold_font,
            fontsize        = widget_default_font_size,
            padding         = widget_default_padding,
            mouse_callbacks = {
                "Button1": lambda: Qtile.cmd_spawn(
                    "python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/wifi/wifi_menu.py")
                    )
                },
            decorations     = right_decor(),
        )

    def poll(self):
        wifi_state = subprocess.check_output(["nmcli",  "radio", "wifi"]).strip().decode("utf-8")
        if wifi_state == "disabled":
            return "Off"

        connection_output = subprocess.check_output(['nmcli', '-t', '-f', 'NAME', 'connection', 'show', '--active'], text=True)
        connection_names = connection_output.strip().split('\n')

        if connection_names:
            ssid = connection_names[0]
            if ssid == "lo":
                return "Disconnected"
            elif ssid == "Wired connection 1":
                return "Ethernet"
            else:
                return ssid
        else:
            return "Error"
            
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")
        
class CpuTempIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text            = "",
            font            = icon_font,
            fontsize        = icon_size + 7,
            foreground      = icon_foreground_4,
            padding         = icon_padding,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/cpu/cpu_stats_menu.py"))},
            decorations     = left_decor(icon_background_4),
        )
        
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class CpuTempWidget(widget.ThermalSensor):
    def __init__(self):
        widget.ThermalSensor.__init__(
            self,
            format           = "{temp:.0f}{unit}",
            font             = bold_font,
            padding          = widget_default_padding,
            threshold        = 80.0,
            foreground_alert = "#bf616a",
            markup           = True,
            update_interval  = cpu_update_interval,
            mouse_callbacks  = {"Button1": lambda: Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/cpu/cpu_stats_menu.py"))},
            decorations      = right_decor(),
        )
        
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class CpuLoadIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text            = "",
            font            = icon_font,
            fontsize        = icon_size + 6,
            foreground      = icon_foreground_5,
            padding         = icon_padding,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/cpu/cpu_stats_menu.py"))},
            decorations     = left_decor(icon_background_5),
        )

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class CpuLoadWidget(widget.CPU):
    def __init__(self):
        widget.CPU.__init__(
            self,
            format          = "{load_percent}%",
            font            = bold_font,
            fontsize        = widget_default_font_size,
            padding         = widget_default_padding,
            markup          = True,
            update_interval = cpu_update_interval,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/cpu/cpu_stats_menu.py"))},
            decorations     = right_decor(),
        )
        
        self.normal_format = self.format
        self.hover_format  = "{load_percent}%{temp:.0f}{unit}"

    def mouse_enter(self, *args, **kwargs):
        self.format = self.hover_format
        self.bar.window.window.set_cursor("hand2")
        self.bar.draw()

    def mouse_leave(self, *args, **kwargs):
        self.format = self.normal_format
        self.bar.window.window.set_cursor("left_ptr")
        self.bar.draw()

class BatteryIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text            = "",
            font            = icon_font,
            fontsize        = icon_size + 5,
            padding         = icon_padding + 2,
            foreground      = icon_foreground_6,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/power/power_management_menu.py"))},
            decorations     = left_decor(icon_background_6),
        )
            
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class BatteryWidget(widget.Battery):
    def __init__(self):
        widget.Battery.__init__(
            self,
            format          = "{percent:2.0%}",
            font            = bold_font,
            fontsize        = widget_default_font_size,
            padding         = widget_default_padding,
            markup          = True,
            update_interval = battery_update_interval,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/power/power_management_menu.py"))},
            decorations     = right_decor(),
        )
            
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class BatteryIconWidget(widget.BatteryIcon):
    def __init__(self, decor=False):
        widget.BatteryIcon.__init__(
            self,
            theme_path      = os.path.expanduser("~/.config/qtile/battery_icons/horizontal/"),
            battery         = 0,
            scale           = 2.65,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/power/power_management_menu.py"))},
            decorations     = right_decor() if decor else right_decor(transparent),
        )
            
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class WattageIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text            = "",
            font            = icon_font,
            fontsize        = icon_size + 5,
            padding         = icon_padding,
            foreground      = icon_foreground_7,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/power/power_management_menu.py"))},
            decorations     = left_decor(icon_background_7),
        )

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class WattageWidget(widget.Battery):
    def __init__(self):
        widget.Battery.__init__(
            self,
            format          = "{watt:.2f}",
            font            = bold_font,
            fontsize        = widget_default_font_size,
            padding         = widget_default_padding,
            markup          = True,
            update_interval = battery_update_interval,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/power/power_management_menu.py"))},
            decorations     = right_decor(),
        )

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

notification_shown = False

class NotificationWidget(widget.TextBox, base.InLoopPollText):
    def __init__(self):
        base.InLoopPollText.__init__(
            self,
            font            = bold_font,
            fontsize        = widget_default_font_size,
            padding         = widget_default_padding,
            update_interval = wifi_update_interval,
            max_chars       = 6,
            decorations     = right_decor()
        )

        self.shown = False
        self.notification_message = None
        self.seen_notification_message = None

    def poll(self):
        global notification_shown
        self.notification_message = subprocess.check_output([os.path.expanduser('~/scripts/other/get_recent_urgent_notification.py')], text=True).strip()
        if self.notification_message and self.notification_message != self.seen_notification_message:
            notification_shown = True
            return self.notification_message
        else:
            notification_shown = False
            return ""

    def mouse_enter(self, *args, **kwargs):
        Qtile.cmd_spawn(os.path.expanduser("~/scripts/other/get_notifications.py"))

    def mouse_leave(self, *args, **kwargs):
        self.seen_notification_message = self.notification_message
        if self.notification_message:
            self.notification_message = None
        
        Qtile.cmd_spawn(os.path.expanduser("~/scripts/other/get_notifications.py"))
        self.poll()

class NotificationIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text            = "",
            font            = icon_font,
            fontsize        = icon_size + 5,
            foreground      = icon_foreground_8,
            padding         = icon_padding,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/other/get_notifications.py"))},
            decorations     = left_decor(color=icon_background_8, round=True),
        )

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")
        self.bar.draw()

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")
        self.bar.draw()

class BacklightIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text        = "",
            font        = icon_font,
            fontsize    = icon_size + 5,
            foreground  = icon_foreground_9,
            padding     = icon_padding + 1,
            decorations = left_decor(icon_background_9),
        )

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class BacklightWidget(widget.Backlight):
    def __init__(self):
        widget.Backlight.__init__(
            self,
            format          = "{percent:2.0%}",
            font            = bold_font,
            fontsize        = widget_default_font_size,
            padding         = widget_default_padding,
            markup          = True,
            backlight_name  = "amdgpu_bl1",
            brightness_file = "/sys/class/backlight/amdgpu_bl1/actual_brightness",
            update_interval = backlight_update_interval,
            decorations     = right_decor(),
        )

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class MenuIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text            = "",
            font            = icon_font,
            fontsize        = icon_size + 8,
            foreground      = text_color,
            padding         = widget_default_padding + 2,
            # mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/bar_menus/cpu/cpu_stats_menu.py"))},
            decorations     = right_decor(round=True),
        )
        
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class ClockIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text       = "",
            font       = icon_font,
            background = bar_background_color,
            foreground = icon_background_7,
            fontsize   = icon_size + 4,
            padding    = widget_default_padding - 4,
        )

class ClockWidget(widget.Clock):
    def __init__(self, decor_color=right_decor_background):
        widget.Clock.__init__(
            self,
            format      = "%H:%M",
            font        = bold_font,
            padding     = widget_default_padding + 5,
            foreground  = text_color,
            fontsize    = widget_default_font_size + 1,
            decorations = right_decor(round=True),
        )

        self.normal_format = self.format
        self.hover_format = "%A %d %B %H:%M"

    def mouse_enter(self, *args, **kwargs):
        self.format = self.hover_format
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.format = self.normal_format
        self.bar.window.window.set_cursor("left_ptr")
        
class AppTrayIcon(widget.Image):
    def __init__(self, icon_name="", group="", app=""):
        global icon_theme_name
        icon_path = IconTheme.getIconPath(icon_name, 48, icon_theme_name)
        widget.Image.__init__(
            self,
            filename        = icon_path,
            margin_x        = 5,
            margin_y        = 5,
            scaling         = 0.7,
            background      = transparent,
            decorations     = [task_list_decor(group=True)],
            mouse_callbacks = {"Button1": lambda: self.click(group, app)},
        )

        self.margin_normal = self.margin_y
        self.margin_hover = self.margin_y - 2
        self.margin_clicked = self.margin_hover - 2
        self.none_check_apps = [
            "vivaldi youtube.com",
            "alacritty",
            "python3 " + os.path.expanduser("~/scripts/qtile/settings_menu/app/settings_menu.py")
        ]
        self.scratchpad_apps = [
            "spotify",
            "ticktick"
        ]
    def click(self, group, app):
        if group:
            Qtile.groups_map[group].cmd_toscreen()
            if app in self.scratchpad_apps:
                Qtile.groups_map["9"].dropdown_toggle(app)
            elif app in self.none_check_apps:
                Qtile.cmd_spawn(app)
            else:
                Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/check_and_launch_app.py " + app + " " + group))
        else:
            Qtile.cmd_spawn(app)
        self.margin_y = self.margin_clicked

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")
        self.margin_y = self.margin_hover
        self.bar.draw()

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")
        self.margin_y = self.margin_normal
        self.bar.draw()

class AppTraySeperator(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text        = "|",
            font        = icon_font,
            fontsize    = icon_size + 15,
            foreground  = app_tray_seperator_color,
            background  = transparent,
            padding     = 2,
            decorations = [task_list_decor(group=True)],
        )

class LaunchTray(widget.LaunchBar):
    def __init__(self):
        widget.LaunchBar.__init__(
            self,
            progs = [
                ("vscode", "code"),
                ("android-studio", "android-studio"),
                ("discord", "discord"),
                ("youtube", "firefox youtube.com"),
                ("firefox", "python3 /home/jonalm/scripts/qtile/check_and_launch_app.py firefox c"),
                ("thunderbird", "thunderbird"),
                ("file-manager", "pcmanfm"),
                ("|", ""),
                ("spotify", "spotify"),
                ("alacritty-simple", "alacritty"),
                ("ticktick", "ticktick"),
                ("|", ""),
                ("system-run", "python3 " + os.path.expanduser("~/scripts/qtile/settings_menu/app/settings_menu.py")),
                ("search", "alacritty"),
            ],
            background = transparent,
            padding = 10,
            icon_size = 65,
            theme_path = "/usr/share/icons/WhiteSur/",
            decorations = [task_list_decor(group=True)],
            mouse_callbacks = {"Button1": lambda: self.click()},
        )
    
    def click(self):
        pass

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")
        self.bar.draw()

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")
        self.bar.draw()

class ActiveWindowOptionWidget(widget.TextBox):
    def __init__(self, text="", foreground=text_color, fontsize=widget_default_font_size + 2):
        widget.TextBox.__init__(
            self,
            text       = text,
            font       = normal_font,
            background = bar_background_color,
            fontsize   = fontsize - 1,
            padding    = widget_default_padding + 14,
            foreground = foreground,
            markup     = True,
        )
        self.normal_foreground = self.foreground
        self.hover_foreground = text_color

        self.normal_fontsize = self.fontsize
        self.hover_fontsize = self.fontsize + 50

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")
        self.foreground = self.hover_foreground
        self.fontsize = self.hover_fontsize
        self.bar.draw()

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")
        self.foreground = self.normal_foreground
        self.fontsize = self.normal_fontsize
        self.bar.draw()

class ActiveWindowIcon(widget.TextBox):
    def __init__(self, foreground=text_color):
        widget.TextBox.__init__(
            self,
            text            = "",
            font            = icon_font,
            fontsize        = icon_size + 6,
            padding         = widget_default_padding,
            background      = bar_background_color,
            foreground      = text_color,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 " + os.path.expanduser("~/scripts/qtile/settings_menu/app/settings_menu.py"))},
        )

    def mouse_enter(self, *args, **kwargs):
        self.text = ""
        self.padding = widget_default_padding + 2
        self.bar.window.window.set_cursor("hand2")
        self.bar.draw()

    def mouse_leave(self, *args, **kwargs):
        self.text = ""
        self.padding = widget_default_padding + 3
        self.bar.window.window.set_cursor("left_ptr")
        self.bar.draw()

class ActiveWindowWidget(widget.WindowName):
    def __init__(self, foreground=text_color):
        widget.WindowName.__init__(
            self,
            background         = bar_background_color,
            font               = bold_font,
            fontsize           = widget_default_font_size + 1,
            format             = "{name}",
            foreground         = foreground,
            empty_group_string = "Desktop",
            padding            = widget_default_padding,
            parse_text         = self.modify_text,
            max_chars          = 200,
        )

    def modify_text(self, text):
        if "—" in text:
            parts = text.split(" — ")
        else:
            parts = text.split(" - ")
        
        app_name = parts[-1].title()

        return app_name

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")
        self.bar.draw()

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")
        self.bar.draw()

class NothingWidget(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            padding  = 0,
            fontsize = 0,
        )

task_list_settings = dict(
    font                = bold_font,
    fontsize            = widget_default_font_size + 1,
    padding_y           = widget_default_padding if laptop else widget_default_padding - 2,
    margin_y            = task_list_margin,
    borderwidth         = task_list_border_width,
    spacing             = task_list_spacing,
    icon_size           = task_list_icon_size,
    rounded             = True,
    markup_floating     = "<span font='Font Awesome 6 free solid 14' foreground='#A7BEAE' size='medium'> 缾 </span>{}",
    markup_minimized    = "<span font='Font Awesome 6 free solid 14' foreground='#b16286' size='medium'> 絛 </span>{}",
    markup_maximized    = "<span font='Font Awesome 6 free solid 14' foreground='#b16286' size='medium'> 类 </span>{}",
    # title_width_method  = "uniform",
    urgent_alert_method = "border",
    highlight_method    = 'block',
    parse_text          = modify_window_name,
    border              = "#4b5662",
    # background          = transparent,
    foreground          = "#d8dee9",
    unfocused_border    = "#3f4752",
    # window_name_location = True,
    # unfocused_border    = transparent,
    theme_mode          = "preferred",
    theme_path          = "/usr/share/icons/WhiteSur-dark/",
)

group_box_settings = dict(
    #margin                      = groupbox_margin,
    padding_x                   = 10,
    padding_y                   = groupbox_padding_y,
    borderwidth                 = True,
    rounded                     = True,
    disable_drag                = False,
    hide_unused                 = False,
    font                        = icon_font,
    fontsize                    = widget_default_font_size + 3,
    highlight_method            = "block",
    active                      = "#4b5662",
    # active                      = "#4b5662",
    # inactive                    = "#4b5662",
    inactive                    = "#1d2125",
    block_highlight_text_color  = text_color,
    highlight_color             = "#000000",
    this_current_screen_border  = right_decor_background,
    this_screen_border          = right_decor_background,
    other_current_screen_border = group_box_other_border_color,
    other_screen_border         = group_box_other_border_color,
    foreground                  = "#4b5662",
    urgent_border               = group_box_urgentborder_color,
)

class GroupBoxWidget(widget.GroupBox):
    def __init__(self, visible_groups=None):
        widget.GroupBox.__init__(
            self,
            **group_box_settings, 
            visible_groups = visible_groups
        )

class WindowCountWidget(widget.WindowCount):
    def __init__(self):
        widget.WindowCount.__init__(
            self,
            padding     = widget_default_padding + 16, 
            background  = transparent, 
            show_zero   = True, 
            fontsize    = widget_default_font_size + 2,
            decorations = [task_list_decor()]
        )

#!###################################################################################
#!  Taken from Yonnji, github: https://github.com/Yonnji/qtile_config/tree/master  ##
#!###################################################################################

# class App(object):
#     cmd = None
#     window = None

# class PinnedApp(App):
#     def __init__(self, desktop, name, icon, cmd):
#         self.desktop = desktop
#         self.name = name
#         self.icon = icon
#         self.cmd = cmd

#     def clone(self):
#         return PinnedApp(desktop=self.desktop, name=self.name, icon=self.icon, cmd=self.cmd)

#     def matches_window(self, window):
#         win_classes = window.get_wm_class() or []

#         if self.get_name() == window.name:
#             return True

#         if self.get_wm_class() and self.get_wm_class() in win_classes:
#             return True

#         for cl in win_classes:
#             if self.name.lower() == cl.lower():
#                 return True

#             if self.get_name().lower().startswith(cl.lower()):
#                 return True

#             if self.get_icon().lower().startswith(cl.lower()):
#                 return True

#         return False

#     def get_name(self):
#         return self.desktop['Desktop Entry']['Name']

#     def get_icon(self):
#         return self.desktop['Desktop Entry']['Icon']

#     def get_wm_class(self):
#         if 'StartupWMClass' in self.desktop['Desktop Entry']:
#             return self.desktop['Desktop Entry']['StartupWMClass']


# class UnpinnedApp(App):
#     def __init__(self, window):
#         self.window = window


# class Dock(IconTextMixin, AppMixin, widget.TaskList):
#     def __init__(self, **config):
#         base._Widget.__init__(self, bar.STRETCH, **config)
#         self.add_defaults(widget.TaskList.defaults)
#         self.add_defaults(base.PaddingMixin.defaults)
#         self.add_defaults(base.MarginMixin.defaults)
#         self._notifications = {}
#         self._icons_cache = {}
#         self._box_end_positions = []
#         self.markup = False
#         self.clicked = None
#         if self.spacing is None:
#             self.spacing = self.margin_x

#         self.add_callbacks({'Button1': lambda: self.select_window()})
#         self.add_callbacks({'Button2': lambda: self.select_window(run=True)})
#         self.add_callbacks({'Button3': lambda: self.select_window(run=True)})

#         self._fallback_icon = None
#         icon = get_icon_path(
#             'application-x-executable',
#             size=self.icon_size, theme=self.theme_path)
#         if icon:
#             self._fallback_icon = self.get_icon_surface(icon, self.icon_size)

#         self.other_border = config.get('other_border', self.border)

#         self.pinned = []
#         flatpaks = dict(self.get_flatpaks())
#         for pinned_name in config.get('pinned_apps', []):
#             if pinned_name in flatpaks:
#                 desktop = flatpaks[pinned_name]
#                 surface = self.get_flatpak_icon(pinned_name, desktop)
#                 if surface:
#                     app = PinnedApp(
#                         desktop=desktop, name=pinned_name,
#                         icon=surface, cmd=f'flatpak run {pinned_name}')
#                     self.pinned.append(app)

#             else:
#                 for desktop_path, desktop in self.get_desktop_files():
#                     if os.path.basename(desktop_path) != f'{pinned_name}.desktop':
#                         continue

#                     icon = get_icon_path(
#                         desktop['Desktop Entry']['Icon'], size=self.icon_size,
#                         theme=self.theme_path)
#                     if icon:
#                         cmd = desktop['Desktop Entry']['Exec']
#                         cmd = re.sub(r'%[A-Za-z]', '', cmd)
#                         surface = self.get_icon_surface(icon, self.icon_size)
#                         app = PinnedApp(
#                             desktop=desktop, name=pinned_name,
#                             icon=surface, cmd=cmd)
#                         self.pinned.append(app)

#                     break

#     async def _config_async(self):
#         if notifier is None:
#             return

#         await notifier.register(self.on_notification, set(), on_close=self.on_close)

#     def on_notification(self, notification):
#         pid = -1
#         name = None
#         if 'sender-pid' in notification.hints:
#             pid = notification.hints['sender-pid'].value
#         if 'desktop-entry' in notification.hints:
#             name = notification.hints['desktop-entry'].value

#         window = None
#         for app in self.windows:
#             if app.window:
#                 if app.window.get_pid() == pid:
#                     window = app.window
#                     break

#                 if app.window.name == name:
#                     window = app.window
#                     break

#                 for cl in (app.window.get_wm_class() or []):
#                     if cl == name:
#                         window = app.window
#                         break

#         if window:
#             if window not in self._notifications:
#                 self._notifications[window] = 0
#             self._notifications[window] += 1

#         # logger.warning(notification)
#         # logger.warning(notification.id)
#         # logger.warning(notification.app_name)
#         # logger.warning(notification.body)
#         # logger.warning(notification.hints.get('sender-pid'))
#         # self.qtile.call_soon_threadsafe(self.update, notification)

#     def on_close(self, notification_id):
#         pass

#     def box_width(self, text):
#         return 0

#     def get_taskname(self, app):
#         if app.window:
#             if app.window in self._notifications:
#                 return str(self._notifications[app.window])

#     def calc_box_widths(self):
#         apps = self.windows
#         if not apps:
#             return []

#         icons = [self.get_window_icon(app) for app in apps]
#         names = [self.get_taskname(app) for app in apps]
#         width_boxes = [(self.icon_size + self.padding_x) for icon in icons]
#         return zip(apps, icons, names, width_boxes)

#     @property
#     def windows(self):
#         pinned_apps = [app.clone() for app in self.pinned]
#         unpinned_apps = []

#         for group in self.qtile.groups:
#             for window in group.windows:
#                 for i, app in enumerate(pinned_apps):
#                     if app.matches_window(window):
#                         if app.window:
#                             app = app.clone()
#                             pinned_apps.insert(i + 1, app)
#                         app.window = window
#                         break
#                 else:
#                     unpinned_apps.append(UnpinnedApp(window))

#         return pinned_apps + unpinned_apps

#     def select_window(self, run=False):
#         if self.clicked:
#             app = self.clicked
#             w = app.window
#             self._notifications.pop(w, None)

#             if (run and app.cmd) or not w:
#                 qtile.spawn(app.cmd)
#                 return

#             if w is w.group.current_window and self.bar.screen.group.name == w.group.name:
#                 # if not w.minimized:
#                 #     w.minimized = True
#                 w.toggle_minimize()

#             else:
#                 for i, screen in enumerate(qtile.screens):
#                     if screen == w.group.screen:
#                         qtile.focus_screen(i)
#                         break
#                 w.group.toscreen()
#                 w.group.focus(w, False)

#                 if w.minimized:
#                     w.minimized = False
#                 if w.floating:
#                     w.bring_to_front()

#     def get_window_icon(self, app):
#         if isinstance(app, PinnedApp):
#             return app.icon

#         w = app.window
#         icon = super().get_window_icon(w)
#         if icon:
#             return icon

#         for cl in w.get_wm_class() or []:
#             for appid, desktop in self.get_flatpaks():
#                 name = desktop['Desktop Entry']['Name']
#                 wmclass = desktop['Desktop Entry'].get('StartupWMClass')
#                 if cl.lower() == name.lower() or cl.lower() == wmclass:
#                     icon = desktop['Desktop Entry']['Icon']
#                     surface = self.get_flatpak_icon(appid, desktop)
#                     if surface:
#                         self._icons_cache[w.wid] = surface
#                         return surface

#             for desktop_path, desktop in self.get_desktop_files():
#                 name = desktop['Desktop Entry']['Name']
#                 wmclass = desktop['Desktop Entry'].get('StartupWMClass')
#                 if cl.lower() == name.lower() or cl.lower() == wmclass:
#                     icon = desktop['Desktop Entry']['Icon']
#                     surface = self.get_icon_surface(icon, self.icon_size)
#                     if surface:
#                         self._icons_cache[w.wid] = surface
#                         return surface

#         return self._fallback_icon

#     def drawbox(self, offset, text, bordercolor, textcolor, width=None, rounded=False,
#                 block=False, icon=None):
#         self.drawer.set_source_rgb(bordercolor or self.background or self.bar.background)

#         x = offset
#         y = (self.bar.height - (self.icon_size + self.padding_y * 2)) // 2
#         w = self.icon_size + self.padding_x * 2
#         h = self.icon_size + self.padding_y * 2

#         if not block:
#             x += w // 4
#             y = 0
#             w = w // 2
#             h = self.padding_y

#         if bordercolor:
#             if rounded:
#                 self.drawer.rounded_fillrect(x, y, w, h, self.borderwidth)
#             else:
#                 self.drawer.fillrect(x, y, w, h, self.borderwidth)

#         if icon:
#             self.draw_icon(icon, offset)

#         if text:
#             self.layout.text = text
#             framed = self.layout.framed(self.borderwidth, self.urgent_border, self.padding_x, self.padding_y / 2, textcolor)
#             framed.draw_fill(offset, self.padding_y * 2 + self.icon_size - framed.height, rounded)

#     def draw_icon(self, surface, offset):
#         if not surface:
#             return

#         self.drawer.ctx.save()
#         self.drawer.ctx.translate(offset + self.padding, (self.bar.height - self.icon_size) // 2)
#         self.drawer.ctx.set_source(surface)
#         self.drawer.ctx.paint()
#         self.drawer.ctx.restore()

#     def draw(self):
#         self.drawer.clear(self.background or self.bar.background)
#         offset = self.margin_x

#         self._box_end_positions = []
#         for app, icon, task, bw in self.calc_box_widths():
#             self._box_end_positions.append(offset + bw)
#             border = self.unfocused_border or None

#             w = app.window
#             if w:
#                 if w.urgent and not task:
#                     # border = self.urgent_border
#                     task = '!'
#                 elif w is w.group.current_window:
#                     if self.bar.screen.group.name == w.group.name and self.qtile.current_screen == self.bar.screen:
#                         border = self.border
#                         self._notifications.pop(w, None)
#                     elif self.qtile.current_screen == w.group.screen:
#                         border = self.other_border
#                         self._notifications.pop(w, None)
#             else:
#                 border = None

#             textwidth = (
#                 bw - 2 * self.padding_x - ((self.icon_size + self.padding_x) if icon else 0)
#             )
#             self.drawbox(
#                 offset,
#                 task,
#                 border,
#                 border,
#                 rounded=self.rounded,
#                 block=self.highlight_method == 'block',
#                 width=textwidth,
#                 icon=icon,
#             )
#             offset += bw + self.spacing

#         self.drawer.draw(offsetx=self.offset, offsety=self.offsety, width=self.width)
