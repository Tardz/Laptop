import gi
gi.require_version('Gtk', '3.0')

from multiprocessing import Process
from gi.repository import Gtk
import subprocess
import time
import json
import os

from network_processing import NetworkProcessing
from options_window import OptionWindow
from eventhandler import EventHandler
from main_window import MainWindow

class WifiMenu:
    def __init__(self, pid_file_path, wifi_process):
        self.pid_file_path = pid_file_path
        self.wifi_process = wifi_process

        self.network_processing = NetworkProcessing()
        self.event_handler = EventHandler()
        self.main_window = MainWindow(self)
        
        Gtk.main()

def get_known_networks():
    known_networks_output = subprocess.check_output("nmcli connection show ", shell=True).decode("utf-8")
    lines = known_networks_output.splitlines()
    known_networks = []

    for line in lines[1:]:
        parts = line.split()
        ssid = parts[0]

        known_networks.append(ssid)
        
    return known_networks

def get_wifi_on():
    wifi_state = subprocess.check_output(["nmcli",  "radio", "wifi"]).strip().decode("utf-8")
    if wifi_state == "enabled":
        return True
    elif wifi_state == "disabled":
        return False

def wifi_process():
    while True:
        if get_wifi_on():
            nmcli_output = subprocess.check_output("nmcli device wifi list", shell=True).decode("utf-8")
            known_networks = get_known_networks()
            if nmcli_output:
                lines = nmcli_output.splitlines()
                unique_networks = []

                seen_ssids = set()

                for line in lines[1:]:
                    parts = line.split()
                    connected = False
                    network_known = False
                    connected_marker = parts[0]

                    if connected_marker == "*":
                        parts.pop(0)
                        connected = True
                    
                    ssid = parts[1]
                    strength = parts[7]

                    if ssid == "--" or "▂" not in strength:
                        ssid = None
                    elif ssid in known_networks:
                            network_known = True
                            ssid = ssid

                    if ssid and (ssid not in seen_ssids or connected):
                        if strength == "▂▄▆_":
                            strength = "▂▄▆▂"
                        elif strength == "▂▄__":
                            strength = "▂▄▂▂"                        
                        elif strength == "▂___":
                            strength = "▂▂▂▂"

                        unique_networks.append({
                            "SSID": ssid, 
                            "STRENGTH": strength, 
                            "CONNECTED": connected, 
                            "KNOWN": network_known
                        })
                        seen_ssids.add(ssid)

                unique_networks.sort(key=lambda x: (not x["CONNECTED"], not x["KNOWN"]))

            with open(os.path.expanduser('~/scripts/qtile/bar_menus/wifi/data/wifi_networks.json'), 'w') as json_file:
                json.dump(unique_networks, json_file, indent=2)

            time.sleep(4)
        else:
            time.sleep(4)

if __name__ == '__main__':
    pid_file_path = os.path.expanduser("~/scripts/qtile/bar_menus/wifi/wifi_menu_pid_file.pid")
    dialog = None

    try:
        if os.path.isfile(pid_file_path):
            with open(pid_file_path, "r") as file:
                pid = int(file.read().strip())
            try:
                os.remove(pid_file_path)
                os.kill(pid, 15)    
            except ProcessLookupError:
                pass
        else:
            with open(pid_file_path, "w") as file:
                file.write(str(os.getpid()))

            process = Process(target=wifi_process)
            process.start()

            WifiMenu(pid_file_path, process)
                    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        exit(0)