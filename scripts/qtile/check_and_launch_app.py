#!/usr/bin/env python

import subprocess
import re
import sys

app = sys.argv[1]
specified_group = sys.argv[2]
specified_command = ""

if len(sys.argv) >= 4:
    specified_command = sys.argv[3]

data = subprocess.check_output(["qtile", "cmd-obj", "-o", "group", "-f", "info"]).decode().strip()

match = re.search(r"'name': '(\d+)'", data)

if match:
    group = match.group(1)
else:
    print("group not found. Error: ", match)
    exit

windows_start = data.find("'windows': [")
windows_end = data.find("]", windows_start) + 1
windows = data[windows_start:windows_end]

print(windows.lower(), group, app, specified_group)

words = app.split()
print(words[0])

if group == specified_group:
    if not app.lower() in windows.lower():
        # if "youtube" in app:
        #     subprocess.call(["qtile", "run-cmd", "brave", "https://www.youtube.com/"])
        # else:
        subprocess.run(specified_command + app, shell = True)
    # else:
        # subprocess.run(f"/home/jonalm/scripts/qtile/cycle_active_windows.py {app}", shell = True)
