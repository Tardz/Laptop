from widgets import (
    PowerButton, LayoutIcon, TickTickMenu, BluetoothIcon, 
    BluetoothWidget, VolumeIcon, VolumeWidget, WifiIcon, 
    WifiWidget, CpuTempIcon, CpuTempWidget, CpuLoadIcon, 
    CpuLoadWidget, BatteryIcon, BatteryWidget, BatteryIconWidget,
    WattageIcon, WattageWidget, NotificationWidget, NotificationIcon,
    BacklightIcon, BacklightWidget, ClockWidget, AppTrayIcon, 
    ActiveWindowOptionWidget, ActiveWindowIcon, ActiveWindowWidget, 
    NothingWidget, GroupBoxWidget, WindowCountWidget, seperator, 
    task_list_settings, LaunchTray, AppTraySeperator, ClockIcon,
    MenuIcon
)
from qtile_extras import widget
from libqtile.bar import Bar
from libqtile import bar
from settings import *

### Single monitor ###
simple_style_1_single_top_bar = Bar([
    seperator(-10),
    GroupBoxWidget(),
    seperator(),

    widget.Spacer(),
    # ActiveWindowIcon(),
    ActiveWindowWidget(width=bar.CALCULATED),
    widget.Spacer(),

    # BLUETOOTH #
    BluetoothIcon(),
    seperator(),

    # VOLUME #
    VolumeIcon(),
    seperator(),

    #  WIFI #
    WifiIcon(),

    # CPU LOAD #
    seperator(),
    CpuLoadIcon(),
    
    # CPU TEMP #
    seperator(),
    CpuTempIcon(),

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
    seperator(8),
    ClockWidget(decor_color=transparent),
    seperator(-10),

], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

shapes_style_1_single_top_bar = Bar([
    seperator(-10, background="#35353b"),
    GroupBoxWidget(background="#35353b"),
    seperator(background="#35353b"),

    widget.Image(
        filename = "~/.config/qtile/Assets/1_grey.png",
        padding = -1
    ),

    widget.Spacer(background="#35353b"),
    # ActiveWindowIcon(),
    ActiveWindowWidget(width=bar.CALCULATED, background="#35353b"),
    widget.Spacer(background="#35353b"),

    widget.Image(
        filename = "~/.config/qtile/Assets/2_grey.png",
        padding = -1
    ),

    # BLUETOOTH #
    BluetoothIcon(background="#35353b"),
    seperator(background="#35353b"),

    # VOLUME #
    VolumeIcon(background="#35353b"),
    seperator(background="#35353b"),

    #  WIFI #
    WifiIcon(background="#35353b"),

    # CPU LOAD #
    seperator(background="#35353b"),
    CpuLoadIcon(background="#35353b"),
    
    # CPU TEMP #
    seperator(background="#35353b"),
    CpuTempIcon(background="#35353b"),

    # URGENT NOTIFICATION #
    seperator(background="#35353b"),
    NotificationIcon(background="#35353b"),

    # BACKLIGHT #
    seperator(background="#35353b"),
    BacklightIcon(background="#35353b"),

    # BATTERY #
    seperator(10, background="#35353b"),
    BatteryIconWidget(background="#35353b"),

    # TIME #
    seperator(8, background="#35353b"),
    ClockWidget(decor_color=transparent, background="#35353b"),
    seperator(-10, background="#35353b"),

], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

simple_style_2_single_top_bar = Bar([
    seperator(-6),
    ClockWidget(decor_color=transparent),

    seperator(-12),
    GroupBoxWidget(),
    seperator(),

    # ClockIcon(),
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

    # WATTAGE #
    seperator(),
    WattageIcon(),
    WattageWidget(),

    # BATTERY #
    seperator(),
    BatteryIcon(),
    BatteryWidget(),

    # URGENT NOTIFICATION #
    seperator(),
    NotificationIcon(),

    # BACKLIGHT #
    seperator(),
    BacklightIcon(),
    BacklightWidget(),

    seperator(),
    MenuIcon(),

    # TIME #
    seperator(-6),

], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

simple_style_single_bottom_bar = Bar([
    # APPTRAY #
    # AppTrayIcon("libreoffice-calc", "m", "libreoffice --calc"),
    # AppTrayIcon("libreoffice-writer", "m", "libreoffice --writer"),
    # AppTraySeperator(),
    AppTrayIcon("vscode", "v", "code"),
    AppTrayIcon("android-studio", "v", "android-studio"),
    AppTrayIcon("discord", "d", "discord"),
    AppTrayIcon("youtube", "c", "vivaldi youtube.com"),
    AppTrayIcon("vivaldi", "c", "vivaldi"),
    AppTrayIcon("file-manager", "n", "pcmanfm"),
    AppTraySeperator(),
    AppTrayIcon("system-run", "", "python3 " + os.path.expanduser("~/scripts/qtile/settings_menu/app/settings_menu.py")),
    AppTrayIcon("spotify", "", "spotify"),
    AppTrayIcon("alacritty", "", "alacritty"),
    AppTrayIcon("ticktick", "", "ticktick"),
    AppTraySeperator(),
    AppTrayIcon("codeblocks", "", HOME + "/.config/rofi/files/launchers/apps/launcher.sh"),
    AppTrayIcon("codium", "", HOME + "/scripts/rofi/config/config_files.sh"),
    AppTrayIcon("automation", "", HOME + "/scripts/rofi/automation/laptop_version/main/automation.sh"),
    AppTrayIcon("search", "", HOME + "/scripts/rofi/search/search_web.sh"),

], bottom_bar_size, margin = bar_margin_bottom, background = bar_background_color, border_width = bar_width_bottom, border_color = bar_border_color, opacity=1)

### Dual monitor ###
simple_style_1_dual_top_bar_1 = Bar([
    # GROUPBOX #
    seperator(-4),
    GroupBoxWidget(
        visible_groups = ["c", "m", "n"]
    ),
    # widget.Image( # From Darkkal44, github: https://github.com/Darkkal44/Cozytile/tree/main #
    #     filename='~/.config/qtile/Assets/5.png',
    #     padding = -1
    # ),

    widget.Spacer(),
    ActiveWindowWidget(width=bar.CALCULATED),
    widget.Spacer(),

    # BLUETOOTH #
    seperator(),
    BluetoothIcon(),

    # VOLUME #
    seperator(),
    VolumeIcon(),

    #  WIFI #
    seperator(),
    WifiIcon(),

    # TICKTICK #
    # seperator(),
    # TickTickMenu(),

    # CPU LOAD #
    seperator(),
    CpuLoadIcon(),

    # CPU TEMP #
    seperator(),
    CpuTempIcon(),

    # URGENT NOTIFICATION #
    seperator(),
    NotificationIcon(),

    # BACKLIGHT #
    seperator() if laptop else NothingWidget(), 
    BacklightIcon() if laptop else NothingWidget(),

    # BATTERY #
    seperator() if laptop else NothingWidget(),
    BatteryIcon() if laptop else NothingWidget(),

    # TIME #
    ClockWidget(decor_color=transparent),
    seperator(-4),
], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

simple_style_1_dual_top_bar_2 = Bar([
    # TIME #
    seperator(-4),
    ClockWidget(decor_color=transparent),

    # BATTERY #
    seperator() if laptop else NothingWidget(),
    BatteryIcon() if laptop else NothingWidget(),

    # BACKLIGHT #
    seperator() if laptop else NothingWidget(), 
    BacklightIcon() if laptop else NothingWidget(),

    # URGENT NOTIFICATION #
    NotificationIcon(),
    seperator(),
    
    # CPU TEMP #
    CpuTempIcon(),
    seperator(),
    
    # CPU LOAD #
    CpuLoadIcon(),
    seperator(),
    
    #  WIFI #
    WifiIcon(),
    seperator(),
    
    # VOLUME #
    VolumeIcon(),
    seperator(),

    # BLUETOOTH #
    BluetoothIcon(),
    seperator(),

    widget.Spacer(),
    ActiveWindowWidget(width=bar.CALCULATED),
    widget.Spacer(),

    # GROUPBOX #
    GroupBoxWidget(
        visible_groups = ["v", "d", "g"]
    ),
    seperator(-4),

], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

simple_style_2_dual_top_bar_1 = Bar([
    # GROUPBOX #
    seperator(-9),
    GroupBoxWidget(
        visible_groups = ["c", "m", "n"]
    ),
    seperator(),
    widget.Spacer(bar.STRETCH),

    # BLUETOOTH #
    seperator(),
    BluetoothWidget(),
    BluetoothIcon(),

    # VOLUME #
    seperator(),
    VolumeIcon(),
    VolumeWidget(),

    #  WIFI #
    seperator(),
    WifiIcon(),
    WifiWidget(),

    # TICKTICK #
    # seperator(),
    # TickTickMenu(),

    # CPU LOAD #
    seperator(),
    CpuLoadIcon(),
    CpuLoadWidget(),

    # CPU TEMP #
    seperator(),
    CpuTempIcon(),
    CpuTempWidget(),

    # URGENT NOTIFICATION #
    seperator(),
    NotificationIcon(),

    # BACKLIGHT #
    seperator() if laptop else NothingWidget(), 
    BacklightIcon() if laptop else NothingWidget(),
    BacklightWidget() if laptop else NothingWidget(),

    # BATTERY #
    seperator() if laptop else NothingWidget(),
    BatteryIcon() if laptop else NothingWidget(),
    BatteryWidget() if laptop else NothingWidget(),

    # MENU #
    seperator(),
    MenuIcon(),
    seperator(-4),
], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

simple_style_2_dual_top_bar_2 = Bar([
    # TIME #
    seperator(-4),
    ClockWidget(decor_color=transparent),
    widget.Spacer(bar.STRETCH),

    # GROUPBOX #
    seperator(),
    widget.Spacer(bar.STRETCH),
    GroupBoxWidget(
        visible_groups = ["v", "d", "g"]
    ),
    seperator(-9),

], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

simple_style_dual_bottom_bar_1 = Bar([
    # APPTRAY #
    AppTrayIcon("codeblocks", "", HOME + "/.config/rofi/files/launchers/apps/launcher.sh"),
    AppTrayIcon("codium", "", HOME + "/scripts/rofi/config/config_files.sh"),
    AppTrayIcon("automation", "", HOME + "/scripts/rofi/automation/laptop_version/main/automation.sh"),
    AppTrayIcon("search", "", HOME + "/scripts/rofi/search/search_web.sh"),
    AppTraySeperator(),
    AppTrayIcon("youtube", "c", "vivaldi youtube.com"),
    AppTrayIcon("vivaldi", "c", "vivaldi"),
    AppTrayIcon("file-manager", "n", "pcmanfm"),
    AppTraySeperator(),
    AppTrayIcon("system-run", "", "python3 " + os.path.expanduser("~/scripts/qtile/settings_menu/app/settings_menu.py")),
    AppTrayIcon("spotify", "", "spotify"),
    AppTrayIcon("alacritty", "", "alacritty"),
    AppTrayIcon("ticktick", "", "ticktick"),

], bottom_bar_size, margin = bar_1_margin_bottom, background = transparent, border_width = bar_width_bottom, border_color = bar_border_color, opacity=1)

simple_style_dual_bottom_bar_2 = Bar([
    # APPTRAY #
    AppTrayIcon("system-run", "", "python3 " + os.path.expanduser("~/scripts/qtile/settings_menu/app/settings_menu.py")),
    AppTrayIcon("spotify", "", "spotify"),
    AppTrayIcon("alacritty", "", "alacritty"),
    AppTrayIcon("ticktick", "", "ticktick"),
    AppTraySeperator(),
    AppTrayIcon("discord", "d", "discord"),
    AppTrayIcon("vscode", "v", "code"),
    AppTrayIcon("android-studio", "v", "android-studio"),
    AppTraySeperator(),
    AppTrayIcon("codeblocks", "", HOME + "/.config/rofi/files/launchers/apps/launcher.sh"),
    AppTrayIcon("codium", "", HOME + "/scripts/rofi/config/config_files.sh"),
    AppTrayIcon("automation", "", HOME + "/scripts/rofi/automation/laptop_version/main/automation.sh"),
    AppTrayIcon("search", "", HOME + "/scripts/rofi/search/search_web.sh"),
], bottom_bar_size, margin = bar_2_margin_bottom, background = transparent, border_width = bar_width_bottom, border_color = bar_border_color, opacity=1)
