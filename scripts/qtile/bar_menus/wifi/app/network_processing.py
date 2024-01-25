import subprocess
import json
import os

class NetworkProcessing:
    def get_wifi_on(self):
        wifi_state = subprocess.check_output(["nmcli",  "radio", "wifi"]).strip().decode("utf-8")
        if wifi_state == "enabled":
            return True
        elif wifi_state == "disabled":
            return False
        
    def get_networks(self):
        with open(os.path.expanduser('~/scripts/qtile/bar_menus/wifi/data/wifi_networks.json'), 'r') as json_file:
            networks = json.load(json_file)
        return networks
        
    def get_known_networks(self):
        known_networks_output = subprocess.check_output("nmcli connection show ", shell=True).decode("utf-8").strip()
        known_networks = []
        from io import StringIO
        import pandas as pd

        df = pd.read_fwf(StringIO(known_networks_output), header=0)

        data = df.to_dict(orient='records')

        for line in data:
            ssid = line["NAME"]
            type = line["TYPE"]

            if type == "wifi":
                known_networks.append({
                    "SSID": ssid, 
                    "STRENGTH": "", 
                    "CONNECTED": False, 
                    "KNOWN": True
                })
            
        return known_networks
    
    def get_networks_offline(self):
        nmcli_output = subprocess.check_output("nmcli device wifi list --rescan no", shell=True).decode("utf-8")
        known_networks = self.get_known_networks()
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

        return unique_networks
