import subprocess
import json
import sys
import os

def remove_pid_from_settings_data(pid_setting_names, qtile_data_file_path):
    import json
    try:
        with open(qtile_data_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    for pid_name in pid_setting_names:
        data[pid_name] = None

    with open(qtile_data_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def remove_pid_files(pid_file_paths):
    for pid_file_path in pid_file_paths:
        if os.path.isfile(pid_file_path):
            os.remove(pid_file_path)

if __name__ == '__main__':
    qtile_data_file_path = os.path.expanduser("~/settings_data/processes.json")

    volume_pid_file_path = os.path.expanduser("~/scripts/qtile/bar_menus/volume/volume_menu_pid_file.pid")
    bluetooth_pid_file_path = os.path.expanduser("~/scripts/qtile/bar_menus/bluetooth/bluetooth_menu_pid_file.pid")
    wifi_pid_file_path = os.path.expanduser("~/scripts/qtile/bar_menus/wifi/wifi_menu_pid_file.pid")

    pid_file_paths = [
        volume_pid_file_path,
        bluetooth_pid_file_path,
        wifi_pid_file_path
    ]

    pid_setting_names = [
        "volume_menu_pid",
        "bluetooth_menu_pid",
        "wifi_menu_pid"
    ]

    remove_pid_files(pid_file_paths)
    remove_pid_from_settings_data(pid_setting_names, qtile_data_file_path)

    sys.exit(0)