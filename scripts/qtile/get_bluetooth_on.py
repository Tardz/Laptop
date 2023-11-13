#!/usr/bin/env python

import subprocess
import sys

try:
    bluetooth_state = subprocess.check_output("systemctl status bluetooth | grep Running", shell=True, stderr=subprocess.PIPE, text=True).strip()
    if "Running" in bluetooth_state:
        print("on")
    else:
        print("off")
except subprocess.CalledProcessError as e:
    print("off")