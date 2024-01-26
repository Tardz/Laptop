from qtile_extras.widget.decorations import BorderDecoration, RectDecoration
from libqtile.command.base import expose_command
from libqtile import qtile as Qtile
from libqtile.widget import base
from qtile_extras import widget
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
        background = background,
        linewidth = seperator_line_width,
        foreground = bar_background_color,
        padding = custom_padding,
        size_percent = 0,
    )

# Default padding_y = 9, Default padding_x = None
def left_decor(color, round=True, padding_x=None, padding_y=left_decor_padding):
    radius = 6 if round else [4, 0, 0, 4]
    if not laptop:
        radius = 5
    return [
        RectDecoration(
            colour = color,
            radius = radius,
            filled = True,
            padding_x = padding_x,
            padding_y = padding_y,
        )
    ]

def clicked_decor(color, round=True, padding_x=None, padding_y=left_decor_padding):
    radius = 6 if round else [4, 0, 0, 4]
    if not laptop:
        radius = 5
    return RectDecoration(
            colour = color,
            radius = radius,
            filled = True,
            padding_x = padding_x,
            padding_y = padding_y,
        )

def left_decor_hover(color, round=True, padding_x=2, padding_y=left_decor_padding + 2):
    radius = 6 if round else [4, 0, 0, 4]
    if not laptop:
        radius = 5
    return [
        RectDecoration(
            colour = color,
            radius = radius,
            filled = True,
            padding_x = padding_x,
            padding_y = padding_y,
        )
    ]

def right_decor(color=right_decor_background, round=True, padding_x=0, padding_y=left_decor_padding):
    radius = 6 if round else [0, 4, 4, 0]
    if not laptop:
        radius = 5
    return [
        RectDecoration(
            colour = color,
            radius = radius,
            filled = True,
            group = True,
            padding_x = padding_x,
            padding_y = padding_y,
        )
    ]

def task_list_decor(color=bar_background_color, radius=12 if laptop else 5, group=False, padding_x=0, padding_y=0):
    return RectDecoration(
        line_width = bottom_widget_width,
        line_colour = bar_border_color,
        colour = color,
        radius = radius,
        filled = True,
        padding_y = padding_y,
        padding_x = padding_x,
        group = group,
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
            return f"Code - {cleaned_parts[0]}"
        return f"{cleaned_parts[-1]} - {cleaned_parts[0]}"
    elif len(cleaned_parts) == 1:
        return cleaned_parts[0]
    else:
        return ''

class PowerButton(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text = f"<span font='Font Awesome 6 free solid {icon_size}' foreground='{icon_foreground_12}' size='medium'></span>",
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/system/system_menu.py")},
            decorations = left_decor(icon_background_12),
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
            text        = f"<span font='Font Awesome 6 free solid {icon_size}' foreground='{icon_foreground_10}' size='medium'></span>",
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/ticktick/launch.py")},
            decorations = left_decor(icon_background_10),
        )
        
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class BluetoothIcon(widget.TextBox):
    def __init__(self):
        self.normal_decorator = left_decor(icon_background_1)
        self.hover_decorator = left_decor(bar_border_color)
        widget.TextBox.__init__(
            self,
            text            = "",
            font            = icon_font,
            fontsize        = icon_size + 8,
            foreground      = icon_foreground_1,
            background      = None,
            padding         = 20,
            mouse_callbacks = {"Button1": lambda: self.clicked()},
            decorations     = self.normal_decorator,
        )

        self.active_background = bar_border_color
        self.inactive_background = self.background
    
    def clicked(self):
        Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/bluetooth/bluetooth_menu.py")
        self.background = self.active_background
        self.bar.draw()

    @expose_command()
    def unclick(self):
        self.background = self.inactive_background
        self.bar.draw()
    
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
            padding         = widget_default_padding,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/bluetooth/bluetooth_menu.py")},
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
            padding         = 20,
            mouse_callbacks = {"Button1": lambda: self.clicked()},
            decorations     = left_decor(icon_background_2),
        )

        self.active_background = bar_border_color
        self.inactive_background = self.background

    def clicked(self):
        Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/volume/volume_menu.py")
        self.background = self.active_background
        self.bar.draw()

    @expose_command()
    def unclick(self):
        self.background = self.inactive_background
        self.bar.draw()
        
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class VolumeWidget(widget.PulseVolume):
    def __init__(self):
        widget.PulseVolume.__init__(
            self,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/volume/volume_menu.py")},
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
            padding         = 20,
        )

        self.active_background = bar_border_color
        self.inactive_background = self.background

    def clicked(self):
        Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/wifi/wifi_menu.py")
        self.background = self.active_background
        self.bar.draw()

    @expose_command()
    def unclick(self):
        self.background = self.inactive_background
        self.bar.draw()
        
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
            padding         = widget_default_padding,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/wifi/wifi_menu.py")},
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
            padding = widget_default_padding + 2,
            text = f"<span font='Font Awesome 6 free solid {icon_size + 1}' foreground='{icon_foreground_4}'size='medium'></span>",
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/cpu/cpu_stats_menu.py")},
            decorations = left_decor(icon_background_4),
        )
        
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class CpuTempWidget(widget.ThermalSensor):
    def __init__(self):
        widget.ThermalSensor.__init__(
            self,
            format = "{temp:.0f}{unit}",
            threshold = 80.0,
            foreground_alert = "#bf616a",
            markup = True,
            update_interval = cpu_update_interval,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/cpu/cpu_stats_menu.py")},
            decorations = right_decor(),
        )
        
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class CpuLoadIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text = f"<span font='Font Awesome 6 free solid {icon_size}' foreground='{icon_foreground_5}'size='medium'></span>",
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/cpu/cpu_stats_menu.py")},
            decorations = left_decor(icon_background_5),
        )

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class CpuLoadWidget(widget.CPU):
    def __init__(self):
        widget.CPU.__init__(
            self,
            format = "{load_percent}%",
            markup = True,
            update_interval = cpu_update_interval,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/cpu/cpu_stats_menu.py")},
            decorations = right_decor(),
        )
        
        self.normal_format = self.format
        self.hover_format = "{load_percent}%{temp:.0f}{unit}"

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
            text = f"<span font='Font Awesome 6 free solid {icon_size}' foreground='{icon_foreground_6}'size='medium'></span>",
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/power/power_management_menu.py")},
            decorations = left_decor(icon_background_6),
        )
            
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class BatteryWidget(widget.Battery):
    def __init__(self):
        widget.Battery.__init__(
            self,
            format = "{percent:2.0%}",
            markup = True,
            update_interval = battery_update_interval,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/power/power_management_menu.py")},
            decorations = right_decor(),
        )
            
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class BatteryIconWidget(widget.BatteryIcon):
    def __init__(self, decor=False):
        widget.BatteryIcon.__init__(
            self,
            theme_path = "/home/jonalm/.config/qtile/battery_icons/horizontal/",
            battery = 0,
            scale = 2.8,
            # update_interval = battery_update_interval,
            padding         = 20,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/power/power_management_menu.py")},
            decorations = right_decor() if decor else right_decor(transparent),
        )
            
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class WattageIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text = f"<span font='Font Awesome 6 free solid {icon_size}' foreground='{icon_foreground_7}'size='medium'></span>",
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/power/power_management_menu.py")},
            decorations=left_decor(icon_background_7),
        )

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class WattageWidget(widget.Battery):
    def __init__(self):
        widget.Battery.__init__(
            self,
            format = "{watt:.2f}",
            markup = True,
            update_interval = battery_update_interval,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/bar_menus/power/power_management_menu.py")},
            decorations = right_decor(),
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
            update_interval = wifi_update_interval,
            max_chars = 6,
            decorations = right_decor()
        )

        self.shown = False
        self.notification_message = None
        self.seen_notification_message = None

    def poll(self):
        global notification_shown
        self.notification_message = subprocess.check_output(['/home/jonalm/scripts/other/get_recent_urgent_notification.py'], text=True).strip()
        if self.notification_message and self.notification_message != self.seen_notification_message:
            notification_shown = True
            return self.notification_message
        else:
            notification_shown = False
            return ""

    def mouse_enter(self, *args, **kwargs):
        Qtile.cmd_spawn("/home/jonalm/scripts/other/get_notifications.py")

    def mouse_leave(self, *args, **kwargs):
        self.seen_notification_message = self.notification_message
        if self.notification_message:
            self.notification_message = None
        
        Qtile.cmd_spawn("/home/jonalm/scripts/other/get_notifications.py")
        self.poll()

class NotificationIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text            = "",
            font            = icon_font,
            fontsize        = icon_size + 5,
            foreground      = icon_foreground_8,
            padding         = 20,
            decorations     = left_decor(icon_background_8),
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/other/get_notifications.py")},
        )

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")
        # if not notification_shown:
        #     Qtile.cmd_spawn("/home/jonalm/scripts/other/get_notifications.py")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")
        # if not notification_shown:
        #     Qtile.cmd_spawn("/home/jonalm/scripts/other/get_notifications.py")

class BacklightIcon(widget.TextBox):
    def __init__(self):
        widget.TextBox.__init__(
            self,
            text        = f"<span font='Font Awesome 6 free solid {icon_size}' foreground='{icon_foreground_9}'size='medium'></span>",
            padding     = 20,
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
            format = "{percent:2.0%}",
            markup = True,
            backlight_name = "amdgpu_bl1",
            brightness_file = "/sys/class/backlight/amdgpu_bl1/actual_brightness",
            update_interval = backlight_update_interval,
            decorations = right_decor(),
        )

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class ClockWidget(widget.Clock):
    def __init__(self, decor_color=right_decor_background):
        widget.Clock.__init__(
            self,
            format = "%A %d %B %H:%M",
            font = bold_font,
            foreground = text_color,
            fontsize = widget_default_font_size,
            decorations = right_decor(decor_color),
            padding = widget_default_padding + 6
        )

# def launch_app_from_bar(check_command):
#     group_name = check_command[1]
#     group = Qtile.groups_map.get(group_name)
#     if group:
#         group.cmd_toscreen()
#         group.cmd_focus()
#     Qtile.cmd_run(check_command[0])
    # qtile.cmd_spawn(["/home/jonalm/scripts/qtile/check_and_launch_app.py", check_command[0], check_command[1], check_command[2]])

class AppTrayIcon(widget.TextBox):
    def __init__(self, icon="", foreground=text_color, check_command=None, launch=None):
        # if check_command:
        #     mouse_callback = {"Button1": launch_app_from_bar(check_command)} if check_command else {"Button1": lambda: Qtile.cmd_spawn(launch)}
        # elif launch:
            # mouse_callback = {"Button1": lambda: Qtile.cmd_run(launch)}
        mouse_callback = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/settings_menu/app/settings_menu.py &")}
        widget.TextBox.__init__(
            self,
            text = f"<span font='Font Awesome 6 free solid' size='medium'>{icon}</span>",
            fontsize = icon_size + 14,
            padding = widget_default_padding + 14,
            foreground = foreground,
            background = transparent,
            markup = True,
            mouse_callbacks = mouse_callback,
            decorations = [task_list_decor(group=True)],
        )
        self.normal_foreground = self.foreground
        self.hover_foreground = text_color

        self.normal_fontsize = self.fontsize
        self.hover_fontsize = self.fontsize + 50

        self.normal_padding = self.padding
        self.hover_padding = self.padding - 2

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")
        self.foreground = self.hover_foreground
        # self.padding = self.hover_padding
        self.fontsize = self.hover_fontsize
        self.bar.draw()

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")
        self.foreground = self.normal_foreground
        # self.padding = self.normal_padding
        self.fontsize = self.normal_fontsize
        self.bar.draw()

class ActiveWindowOptionWidget(widget.TextBox):
    def __init__(self, text="", foreground=text_color, fontsize=widget_default_font_size + 2):
        widget.TextBox.__init__(
            self,
            text = text,
            font = normal_font,
            background = bar_background_color,
            fontsize = fontsize,
            padding = widget_default_padding + 14,
            foreground = foreground,
            markup = True,
        )
        self.normal_foreground = self.foreground
        self.hover_foreground = text_color

        self.normal_fontsize = self.fontsize
        self.hover_fontsize = self.fontsize + 50

        self.normal_padding = self.padding
        self.hover_padding = self.padding - 2
    
    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")
        self.foreground = self.hover_foreground
        # self.padding = self.hover_padding
        self.fontsize = self.hover_fontsize
        self.bar.draw()

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")
        self.foreground = self.normal_foreground
        # self.padding = self.normal_padding
        self.fontsize = self.normal_fontsize
        self.bar.draw()

class ActiveWindowIcon(widget.TextBox):
    def __init__(self, foreground=text_color):
        widget.TextBox.__init__(
            self,
            text = "",
            fontsize = icon_size + 9,
            padding = widget_default_padding + 18,
            background = bar_background_color,
            mouse_callbacks = {"Button1": lambda: Qtile.cmd_spawn("python3 /home/jonalm/scripts/qtile/settings_menu/app/settings_menu.py")}
        )

    def mouse_enter(self, *args, **kwargs):
        self.bar.window.window.set_cursor("hand2")

    def mouse_leave(self, *args, **kwargs):
        self.bar.window.window.set_cursor("left_ptr")

class ActiveWindowWidget(widget.WindowName):
    def __init__(self, foreground=text_color):
        widget.WindowName.__init__(
            self,
            background = bar_background_color,
            font = bold_font,
            fontsize = widget_default_font_size + 1,
            padding = 0,
            format = "{name}",
            foreground = foreground,
            empty_group_string = "Desktop",
            parse_text = self.modify_text,
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
            padding = 0,
            fontsize = 0,
        )

task_list_settings = dict(
    font                = bold_font,
    fontsize            = widget_default_font_size + 1,
    padding_y           = widget_default_padding + 9 if laptop else widget_default_padding - 2,
    margin              = task_list_margin - 1,
    borderwidth         = task_list_border_width,
    spacing             = task_list_spacing,
    icon_size           = task_list_icon_size,
    rounded             = True,
    markup_floating     = "<span font='Font Awesome 6 free solid {icon_size}' foreground='#A7BEAE' size='medium'> 缾 </span>{}",
    markup_minimized    = "<span font='Font Awesome 6 free solid {icon_size}' foreground='#b16286' size='medium'> 絛 </span>{}",
    markup_maximized    = "<span font='Font Awesome 6 free solid {icon_size}' foreground='#b16286' size='medium'> 类 </span>{}",
    title_width_method  = "uniform",
    urgent_alert_method = "border",
    highlight_method    = 'block',
    parse_text          = modify_window_name,
    border              = bar_border_color,
    background          = transparent,
    foreground          = "#d8dee9",
    unfocused_border    = bar_background_color,
    theme_mode          = "preferred",
    # theme_path          = "/usr/share/icons/Adwaita",
    decorations         = [task_list_decor()],
)

group_box_settings = dict(
    # margin                      = groupbox_margin,
    padding_x                   = 20,
    padding_y                   = 5,
    margin_x                    = 24,
    borderwidth                 = True,
    rounded                     = True,
    disable_drag                = False,
    hide_unused                 = True,
    font                        = icon_font,
    highlight_method            = "block",
    active                      = bar_border_color,
    inactive                    = bar_background_color,
    block_highlight_text_color  = "#000000",
    highlight_color             = "#000000",
    this_current_screen_border  = "#bf616a",
    this_screen_border          = bar_border_color,
    other_current_screen_border = group_box_other_border_color,
    other_screen_border         = group_box_other_border_color,
    foreground                  = group_box_foreground_color,
    urgent_border               = group_box_urgentborder_color,
)

class GroupBoxWidget(widget.GroupBox):
    def __init__(self):
        widget.GroupBox.__init__(
            self,
            **group_box_settings, 
            # background = transparent, 
            # decorations = [task_list_decor()]
        )

class WindowCountWidget(widget.WindowCount):
    def __init__(self):
        widget.WindowCount.__init__(
            self,
            padding = widget_default_padding + 16, 
            background = transparent, 
            show_zero = True, 
            fontsize = widget_default_font_size + 2,
            decorations = [task_list_decor()]
        )