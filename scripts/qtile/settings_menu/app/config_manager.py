import os
import json

class ConfigManager:
    indent = 4
    list_elements = [
        {"title": "About",         "icon": "", "css": "about",         "box": None},
        {"title": "Themes",        "icon": "", "css": "themes",        "box": None},
        {"title": "General",       "icon": "", "css": "general",       "box": None},
        {"title": "Qtile",         "icon": "", "css": "qtile",         "box": None},
        {"title": "Menus",         "icon": "", "css": "menus",         "box": None},
        {"title": "Notifications", "icon": "", "css": "notifications", "box": None},
        {"title": "Power",         "icon": "", "css": "power",         "box": None},
        {"title": "Display",       "icon": "", "css": "display",       "box": None},
        {"title": "Backlight",     "icon": "", "css": "backlight",     "box": None},
        {"title": "Security",      "icon": "", "css": "security",      "box": None},
        {"title": "Storage",       "icon": "", "css": "storage",       "box": None},
        {"title": "Wifi",          "icon": "", "css": "wifi",          "box": None},
        {"title": "Bluetooth",     "icon": "", "css": "bluetooth",     "box": None},
        {"title": "Sound",         "icon": "", "css": "sound",         "box": None},
    ]

    @staticmethod
    def load_qtile_data(file_path):
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                qtile_data = json.load(file)
        else:
            qtile_data = {
                "top_bar_status": True, 
                "bottom_bar_status": True,

                "follow_mouse_focus": True,
                "bring_front_click": True,
                "cursor_warp": False,
                
                "auto_fullscreen": True,
                "auto_minimize": True,
                "reconfigure_screens": False,
                "scratchpad_focus_value": True,
                "focus_on_window_activation": "smart",
            }
            with open(file_path, "w") as file:
                json.dump(qtile_data, file, indent=ConfigManager.indent)
        
        return qtile_data

    @staticmethod
    def load_qtile_colors(file_path):
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                qtile_colors = json.load(file)
        else:
            qtile_colors = {
                "bar_background": "#242831.95", 
                "bar_border_background": "#717c99.9",
                "icon_1" : "#bf616a",
                "icon_2" : "#d08770",
                "icon_3" : "#ebcb8b",
                "icon_4" : "#a3be8c",
                "icon_5" : "#8fbcbb",
                "icon_6" : "#5e81ac",
                "icon_7" : "#9B98B7",
                "icon_8" : "#b48ead",
                "bubble_color" : "#606b86.9",
            }
            with open(file_path, "w") as file:
                json.dump(qtile_colors, file, indent=ConfigManager.indent)

        return qtile_colors

    @staticmethod
    def load_other_data(file_path):
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                other_data = json.load(file)
        else:
            other_data = {

            }
            with open(file_path, "w") as file:
                json.dump(other_data, file, indent=ConfigManager.indent)
        
        return other_data
    
    @staticmethod
    def write_config_to_file(file_path, config_data):
        with open(file_path, "w") as config_file:
            json.dump(config_data, config_file, indent=ConfigManager.indent)

    @staticmethod
    def get_list_elements():
        return ConfigManager.list_elements