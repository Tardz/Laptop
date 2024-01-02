#!/usr/bin/env python

import subprocess
import re

qtile_data = subprocess.check_output("qtile cmd-obj -o group -f info", shell=True).decode("utf-8")
qtile_data = qtile_data.replace("'", "\"")

match = re.search(r'"screen": (\d+)', qtile_data)
monitor_number = 0
screen_number = int(match.group(1))

if screen_number == 1:
    monitor_number = 1
else:
    monitor_number = 0

print(monitor_number)