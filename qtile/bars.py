from widgets import (
    PowerButton, LayoutIcon, TickTickMenu, BluetoothIcon, 
    BluetoothWidget, VolumeIcon, VolumeWidget, WifiIcon, 
    WifiWidget, CpuTempIcon, CpuTempWidget, CpuLoadIcon, 
    CpuLoadWidget, BatteryIcon, BatteryWidget, BatteryIconWidget,
    WattageIcon, WattageWidget, NotificationWidget, NotificationIcon,
    BacklightIcon, BacklightWidget, ClockWidget, AppTrayIcon, 
    ActiveWindowOptionWidget, ActiveWindowIcon, ActiveWindowWidget, 
    NothingWidget, GroupBoxWidget, WindowCountWidget, seperator, 
    task_list_settings, LaunchTray, AppTraySeperator
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
], bottom_bar_size, margin = bar_margin_bottom, background = bar_background_color, border_width = bar_width_bottom, border_color = bar_border_color, opacity=1)

simple_style_single_top_bar_1 = Bar([
    seperator(-12),
    GroupBoxWidget(),
    # widget.TaskList(**task_list_settings),
    seperator(),

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
    seperator(),
    CpuLoadIcon(),

    # URGENT NOTIFICATION #
    seperator(),
    NotificationIcon(),

    # BACKLIGHT #
    seperator(),
    BacklightIcon(),

    # BATTERY #
    seperator(10),
    BatteryIconWidget(),

    # TIME #
    seperator(10),
    ClockWidget(decor_color=transparent),
    seperator(-12),

], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

simple_style_single_top_bar_2 = Bar([
    seperator(-12),
    GroupBoxWidget(),
    # widget.TaskList(**task_list_settings),
    seperator(),

    widget.Spacer(bar.STRETCH),
    ClockWidget(decor_color=transparent),
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

    # TICKTICK #
    # seperator(),
    # TickTickMenu(),

    # CPU LOAD #
    seperator(),
    CpuLoadIcon(),
    CpuLoadWidget(),

    # URGENT NOTIFICATION #
    seperator(),
    NotificationIcon(),

    # BACKLIGHT #
    seperator(),
    BacklightIcon(),
    BacklightWidget(),

    # BATTERY #
    seperator(),
    BatteryIcon(),
    BatteryWidget(),

    # TIME #
    seperator(-6),

], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

simple_style_single_bottom_bar = Bar([
    # APPTRAY #
    # widget.Spacer(bar.STRETCH),
    # LaunchTray(),
    AppTrayIcon("vscode", "v", "code"),
    AppTrayIcon("android-studio", "v", "android-studio"),
    AppTrayIcon("discord", "d", "discord"),
    AppTrayIcon("youtube", "c", "firefox youtube.com"),
    AppTrayIcon("firefox", "c", "firefox"),
    AppTrayIcon("thunderbird", "n", "thunderbird"),
    AppTrayIcon("file-manager", "n", "pcmanfm"),
    AppTraySeperator(),
    AppTrayIcon("spotify", "", "spotify"),
    AppTrayIcon("alacritty-simple", "", "alacritty"),
    AppTrayIcon("ticktick", "", "ticktick"),
    AppTraySeperator(),
    AppTrayIcon("system-run", "", "python3 " + os.path.expanduser("~/scripts/qtile/settings_menu/app/settings_menu.py")),
    AppTrayIcon("search"),

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

    # TICKTICK #
    # seperator(),
    # TickTickMenu(),

    # CPU LOAD #
    seperator(),
    CpuLoadIcon(),

    # URGENT NOTIFICATION #
    seperator(),
    NotificationIcon(),

    # BACKLIGHT #
    seperator() if laptop else NothingWidget(),
    BacklightIcon() if laptop else NothingWidget(),

    # BATTERY #
    seperator() if laptop else NothingWidget(),
    BatteryIconWidget() if laptop else NothingWidget(),

    # TIME #
    seperator(-2),
    ClockWidget(decor_color=transparent),
    # seperator(),

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
], bottom_bar_size, margin = bar_margin_bottom, background = bar_background_color, border_width = bar_width_bottom, border_color = bar_border_color, opacity=1)
