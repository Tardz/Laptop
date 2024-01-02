#!/usr/bin/env python

import subprocess
import sys
import os

new_directory = '/home/jonalm/scripts/qtile'
os.chdir(new_directory)

app = sys.argv[1]
specified_group = sys.argv[2]
specified_command = ""

if len(sys.argv) >= 4:
    specified_command = sys.argv[3]

data = subprocess.check_output(["qtile", "cmd-obj", "-o", "group", "-f", "info"]).decode().strip()

windows_start = data.find("'windows': [")
windows_end = data.find("]", windows_start) + 1
windows = data[windows_start:windows_end]

if not app.lower() in windows.lower():
    print(f"running: {app}, {specified_command}")
    subprocess.run(f"{specified_command} {app}", shell = True)
    # else:
        # subprocess.call(f"/home/jonalm/scripts/qtile/cycle_active_windows.py {app} {specified_group}", shell = True)

exit(0)