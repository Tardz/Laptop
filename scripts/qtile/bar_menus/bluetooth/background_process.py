import subprocess
import json
import os

class BackgroundProcess:
    def scan_devices(self):
        subprocess.run("bluetoothctl --timeout 10 scan on", shell = True)
        output = subprocess.check_output("hcitool scan", shell = True).decode("utf-8")
        return output

    def get_bluetooth_on(self):
        try:
            bluetooth_state = subprocess.check_output("systemctl status bluetooth | grep Running", shell=True, stderr=subprocess.PIPE, text=True).strip()
            if "Running" in bluetooth_state:
                return True
            else:
                return False
        except subprocess.CalledProcessError as e:
            return False
        
    def bluetooth_process(self):
        while True:
            if self.get_bluetooth_on():
                bluetooth_output = self.scan_devices()
                if bluetooth_output:
                    lines = bluetooth_output.splitlines()
                    unique_devices = []

                    for line in lines[1:]:
                        parts = line.split("\t", 2)
                        parts.pop(0)

                        device_name = parts[1]
                        device_addr = parts[0]

                        if device_name != "n/a":
                            unique_devices.append({"DEVICE": device_name, "MAC-ADDR": device_addr})
                
                with open(os.path.expanduser('~/scripts/qtile/bar_menus/bluetooth/bluetooth_devices.json'), 'w') as json_file:
                    json.dump(unique_devices, json_file, indent=2)
