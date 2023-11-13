#!/usr/bin/env python

import subprocess
import re
import sys

try:
    bluetooth_state = subprocess.check_output("systemctl status bluetooth | grep Running", shell=True, stderr=subprocess.PIPE, text=True).strip()
    if "Running" in bluetooth_state:
        connected_devices_output = subprocess.check_output("bluetoothctl devices Connected", shell=True).decode("utf-8")
        lines = connected_devices_output.splitlines()
        trusted_devices = self.get_trusted_devices()
        
        if connected_devices_output:
            lines = connected_devices_output.splitlines()

            parts = lines[0].split(" ", 2)

            device_name = parts[2]
            
            if device_name == "N/A":
                return 
            else:
                return device_name
        
except subprocess.CalledProcessError as e:
    return "Off"