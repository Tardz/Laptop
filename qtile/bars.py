from widgets import (
    PowerButton, LayoutIcon, TickTickMenu, BluetoothIcon, 
    BluetoothWidget, VolumeIcon, VolumeWidget, WifiIcon, 
    WifiWidget, CpuTempIcon, CpuTempWidget, CpuLoadIcon, 
    CpuLoadWidget, BatteryIcon, BatteryWidget, BatteryIconWidget,
    WattageIcon, WattageWidget, NotificationWidget, NotificationIcon,
    BacklightIcon, BacklightWidget, ClockWidget, AppTrayIcon, 
    ActiveWindowOptionWidget, ActiveWindowIcon, ActiveWindowWidget, 
    NothingWidget, GroupBoxWidget, WindowCountWidget, seperator, 
    task_list_settings
)
from qtile_extras import widget
from libqtile.bar import Bar
from libqtile import bar
from settings import *


box_style_single_top_bar = Bar([
    # POWERBUTTON # 
    seperator(-3),
    PowerButton(),

    # LAYOUTICON # 
    seperator(),
    LayoutIcon(),

    # TICKTICK MENU #
    seperator(),
    TickTickMenu(),

    widget.Spacer(bar.STRETCH),

    # BLUETOOTH #
    BluetoothIcon(),
    BluetoothWidget(),
    seperator(),

    # VOLUME #
    VolumeIcon(),
    VolumeWidget(),
    seperator(),

    #  WIFI #
    WifiIcon(),
    WifiWidget(),

    # CPU TEMP #
    seperator(),
    CpuTempIcon(),
    CpuTempWidget(),

    # CPU LOAD #
    seperator(),
    CpuLoadIcon(),
    CpuLoadWidget(),

    # BATTERY #
    seperator(),
    BatteryIcon(),
    BatteryIconWidget(decor=True),

    # WATTAGE #
    seperator(),
    WattageIcon(),
    WattageWidget(),

    # URGENT NOTIFICATION #
    seperator(),
    NotificationIcon(),
    NotificationWidget(),

    # BACKLIGHT #
    seperator(),
    BacklightIcon(),
    BacklightWidget(),

    # TIME #
    seperator(),
    ClockWidget(),
    seperator(-5),

], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

box_style_single_bottom_bar = Bar([
    # GROUPBOX #
    GroupBoxWidget(),
    
    # TASKLIST #
    seperator(background=transparent),
    widget.TaskList(**task_list_settings),

    # APPS #
    seperator(background=transparent),
    AppTrayIcon("", app_tray_icon_color_1, ["firefox", "c", ""]),
    AppTrayIcon("", app_tray_icon_color_2, ["code", "v", ""]),
    AppTrayIcon("", app_tray_icon_color_3, ["pcmanfm", "n", ""]),
    AppTrayIcon("", app_tray_icon_color_4, launch="spotify"),
    AppTrayIcon(" ", app_tray_icon_color_5, launch="python3 ~/scripts/qtile/settings_menu/app/settings_menu.py"),

], bottom_bar_size, margin = bar_margin_bottom, background = bar_background_color, border_width = bar_width_bottom, border_color = bar_border_color, opacity=1)

box_style_dual_top_bar_1 = Bar([
    widget.Spacer(bar.STRETCH),
    
    # BLUETOOTH #
    BluetoothIcon(),
    BluetoothWidget(),
    
    # VOLUME #
    seperator(),
    VolumeIcon(),
    VolumeWidget(),

    #  WIFI #
    seperator(),
    WifiIcon(),
    WifiWidget(),

    # CPU TEMP #
    seperator(),
    CpuTempIcon(),
    CpuTempWidget(),

    # CPU LOAD #
    seperator(),
    CpuLoadIcon(),
    CpuLoadWidget(),

    # BATTERY #
    seperator() if laptop else NothingWidget(),
    BatteryIcon() if laptop else NothingWidget(),
    BatteryWidget() if laptop else NothingWidget(),

    # WATTAGE #
    seperator() if laptop else NothingWidget(),
    WattageIcon() if laptop else NothingWidget(),
    WattageWidget() if laptop else NothingWidget(),

    # URGENT NOTIFICATION #
    seperator(),
    NotificationIcon(),
    NotificationWidget(),

    # BACKLIGHT #
    seperator() if laptop else NothingWidget(),
    BacklightIcon() if laptop else NothingWidget(),
    BacklightWidget() if laptop else NothingWidget(),

    # TIME #
    seperator(),
    ClockWidget(),
    seperator(),

], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

box_style_dual_top_bar_2 = Bar([
    # POWERBUTTON #
    seperator(),
    PowerButton(),

    # LAYOUTICON #
    seperator(),
    LayoutIcon(),

    # TICKTICK MENU #
    seperator(),
    TickTickMenu(),

    widget.Spacer(bar.STRETCH),

], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

box_style_dual_bottom_bar_1 = Bar([
    # APPS #
    AppTrayIcon("", icon_background_2, ["firefox", "c", ""]),
    AppTrayIcon("", icon_background_3, ["code", "v", ""]),
    AppTrayIcon("", icon_background_7, ["pcmanfm", "n", ""]),
    AppTrayIcon("", icon_background_8, launch="spotify"),
    AppTrayIcon(" ", icon_background_9, launch="~/scripts/qtile/settings_menu/app/settings_menu.py"),

    # WINDOWCOUNT #
    seperator(background=transparent),
    WindowCountWidget(),

    # TASKLIST #
    seperator(background=transparent),
    widget.TaskList(**task_list_settings),

    # GROUPBOX #
    seperator(background=transparent),
    GroupBoxWidget(),

], bottom_bar_size, margin = bar_margin_bottom, background = bar_background_color, border_width = bar_width_bottom, border_color = bar_border_color, opacity=1)

box_style_dual_bottom_bar_2 = Bar([
    # GROUPBOX #
    GroupBoxWidget(),

    # TASKLIST #
    seperator(background=transparent),
    widget.TaskList(**task_list_settings),

    # WINDOWCOUNT #
    seperator(background=transparent),
    WindowCountWidget(),

    # APPS #
    seperator(background=transparent),
    AppTrayIcon("", icon_background_2, ["firefox", "c", ""]),
    AppTrayIcon("", icon_background_3, ["code", "v", ""]),
    AppTrayIcon("", icon_background_7, ["pcmanfm", "n", ""]),
    AppTrayIcon("", icon_background_8, launch="spotify"),
    AppTrayIcon(" ", icon_background_9, launch="python3 /home/jonalm/scripts/qtile/settings_menu/app"),

], bottom_bar_size, margin = bar_margin_bottom, background = bar_background_color, border_width = bar_width_bottom, border_color = bar_border_color, opacity=1)

simple_style_single_top_bar = Bar([
    ActiveWindowIcon(),
    ActiveWindowWidget(),
    # ActiveWindowOptionWidget("File"),
    # ActiveWindowOptionWidget("Edit"),
    # ActiveWindowOptionWidget("View"),
    # ActiveWindowOptionWidget("Go"),
    # ActiveWindowOptionWidget("Window"),

    widget.Spacer(bar.STRETCH),

    # BLUETOOTH #
    BluetoothIcon(),
    seperator(),

    # VOLUME #
    VolumeIcon(),
    seperator(),

    #  WIFI #
    WifiIcon(),

    # TICKTICK #
    # seperator(),
    # TickTickMenu(),

    # CPU LOAD #
    # seperator(),
    # CpuLoadIcon(),

    # URGENT NOTIFICATION #
    seperator(),
    NotificationIcon(),

    # BACKLIGHT #
    seperator(),
    BacklightIcon(),

    # BATTERY #
    seperator(),
    BatteryIconWidget(),

    # TIME #
    seperator(22),
    ClockWidget(decor_color=transparent),
    seperator(4),

], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

simple_style_single_bottom_bar = Bar([
    # GROUPBOX #
    # GroupBoxWidget(),
    
    # TASKLIST #
    widget.TaskList(**task_list_settings),
    seperator(background=transparent),
    
    # APPTRAY #
    AppTrayIcon("", app_tray_icon_color_1, ["firefox", "c", ""]),
    AppTrayIcon("", app_tray_icon_color_2, ["code", "v", ""]),
    AppTrayIcon("", app_tray_icon_color_3, ["pcmanfm", "n", ""]),
    AppTrayIcon("", app_tray_icon_color_4, launch="spotify"),
    AppTrayIcon(" ", app_tray_icon_color_5, launch="python3 ~/scripts/qtile/settings_menu/app/settings_menu.py"),

], bottom_bar_size, margin = bar_margin_bottom, background = bar_background_color, border_width = bar_width_bottom, border_color = bar_border_color, opacity=1)

simple_style_dual_top_bar_1 = Bar([
    widget.Spacer(bar.STRETCH),

     # BLUETOOTH #
    BluetoothIcon(),
    seperator(),

    # VOLUME #
    VolumeIcon(),
    seperator(),

    #  WIFI #
    WifiIcon(),

    # URGENT NOTIFICATION #
    seperator(),
    NotificationIcon(),

    # TIME #
    seperator(),
    ClockWidget(decor_color=transparent),
    seperator(4),

], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

simple_style_dual_top_bar_2 = Bar([
    ActiveWindowIcon(),
    ActiveWindowWidget(),

    widget.Spacer(bar.STRETCH),

], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

simple_style_dual_bottom_bar_1 = Bar([
    # GROUPBOX #
    # GroupBoxWidget(),
    
    # TASKLIST #
    widget.TaskList(**task_list_settings),
    seperator(background=transparent),
    
    # APPTRAY #
    AppTrayIcon("", app_tray_icon_color_1, ["firefox", "c", ""]),
    AppTrayIcon("", app_tray_icon_color_2, ["code", "v", ""]),
    AppTrayIcon("", app_tray_icon_color_3, ["pcmanfm", "n", ""]),
    AppTrayIcon("", app_tray_icon_color_4, launch="spotify"),
    AppTrayIcon(" ", app_tray_icon_color_5, launch="python3 ~/scripts/qtile/settings_menu/app/settings_menu.py"),

], bottom_bar_size, margin = bar_margin_bottom, background = bar_background_color, border_width = bar_width_bottom, border_color = bar_border_color, opacity=1)

simple_style_dual_bottom_bar_2 = Bar([
    # GROUPBOX #
    GroupBoxWidget(),

    # TASKLIST #
    seperator(background=transparent),
    widget.TaskList(**task_list_settings),

    # WINDOWCOUNT #
    seperator(background=transparent),
    WindowCountWidget(),

    # APPS #
    seperator(background=transparent),
    AppTrayIcon("", icon_background_2, ["firefox", "c", ""]),
    AppTrayIcon("", icon_background_3, ["code", "v", ""]),
    AppTrayIcon("", icon_background_7, ["pcmanfm", "n", ""]),
    AppTrayIcon("", icon_background_8, launch="spotify"),
    AppTrayIcon(" ", icon_background_9, launch="python3 /home/jonalm/scripts/qtile/settings_menu/app"),

], bottom_bar_size, margin = bar_margin_bottom, background = bar_background_color, border_width = bar_width_bottom, border_color = bar_border_color, opacity=1)
