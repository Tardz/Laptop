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
    seperator(-12),
    GroupBoxWidget(),
    seperator(),

    seperator(250),
    widget.Spacer(bar.STRETCH),
    # ActiveWindowIcon(),
    ActiveWindowWidget(),

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
    seperator(-12),

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
    seperator(-8),
    GroupBoxWidget(
        visible_groups = ["c", "m", "n"]
    ),
    seperator(),

    seperator(410),
    widget.Spacer(bar.STRETCH),
    
    # ActiveWindowIcon(),
    ActiveWindowWidget(),

    widget.Spacer(bar.STRETCH),

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
    seperator(-8),
], top_bar_size, margin = bar_margin_top, background = bar_background_color, border_width = bar_width_top, border_color = bar_border_color, opacity=1)

simple_style_1_dual_top_bar_2 = Bar([
    seperator(425),
    widget.Spacer(bar.STRETCH),
    ActiveWindowWidget(),
    widget.Spacer(bar.STRETCH),

    # GROUPBOX #
    seperator(),
    # widget.Spacer(bar.STRETCH),
    GroupBoxWidget(
        visible_groups = ["v", "d", "g"]
    ),
    seperator(-9),

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
    # AppTrayIcon("libreoffice-calc", "m", "libreoffice --calc"),
    # AppTrayIcon("libreoffice-writer", "m", "libreoffice --writer"),
    # AppTraySeperator(),
    AppTrayIcon("codeblocks", "", HOME + "/.config/rofi/files/launchers/apps/launcher.sh"),
    AppTrayIcon("codium", "", HOME + "/scripts/rofi/config/config_files.sh"),
    AppTrayIcon("automation", "", HOME + "/scripts/rofi/automation/laptop_version/main/automation.sh"),
    AppTrayIcon("search", "", HOME + "/scripts/rofi/search/search_web.sh"),
    AppTraySeperator(),
    AppTrayIcon("discord", "d", "discord"),
    AppTrayIcon("youtube", "c", "firefox youtube.com"),
    AppTrayIcon("vivaldi", "c", "vivaldi"),
    AppTrayIcon("file-manager", "n", "pcmanfm"),
    AppTraySeperator(),
    AppTrayIcon("system-run", "", "python3 " + os.path.expanduser("~/scripts/qtile/settings_menu/app/settings_menu.py")),
    AppTrayIcon("spotify", "", "spotify"),
    AppTrayIcon("alacritty", "", "alacritty"),
    AppTrayIcon("ticktick", "", "ticktick"),

], bottom_bar_size, margin = bar_1_margin_bottom, background = bar_background_color, border_width = bar_width_bottom, border_color = bar_border_color, opacity=1)

simple_style_dual_bottom_bar_2 = Bar([
    # APPTRAY #
    # AppTrayIcon("file-manager", "n", "pcmanfm"),
    AppTrayIcon("system-run", "", "python3 " + os.path.expanduser("~/scripts/qtile/settings_menu/app/settings_menu.py")),
    AppTrayIcon("spotify", "", "spotify"),
    AppTrayIcon("alacritty", "", "alacritty"),
    AppTrayIcon("ticktick", "", "ticktick"),
    AppTraySeperator(),
    AppTrayIcon("vscode", "v", "code"),
    AppTrayIcon("android-studio", "v", "android-studio"),
    AppTraySeperator(),
    AppTrayIcon("codeblocks", "", HOME + "/.config/rofi/files/launchers/apps/launcher.sh"),
    AppTrayIcon("codium", "", HOME + "/scripts/rofi/config/config_files.sh"),
    AppTrayIcon("automation", "", HOME + "/scripts/rofi/automation/laptop_version/main/automation.sh"),
    AppTrayIcon("search", "", HOME + "/scripts/rofi/search/search_web.sh"),
], bottom_bar_size, margin = bar_2_margin_bottom, background = bar_background_color, border_width = bar_width_bottom, border_color = bar_border_color, opacity=1)
