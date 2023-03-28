#!/usr/bin/env python

import subprocess
import re
import sys

arg1 = sys.argv[1]
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

if not "Brave" in windows and group == "2":
    if "youtube" in arg1:
        subprocess.call(["qtile", "run-cmd", "brave", "https://www.youtube.com/"])
    else:
        subprocess.call(["qtile", "run-cmd", "brave"])
if not "jonalm" or not "Desktop" in windows and group == "4":
    subprocess.call(["qtile", "run-cmd", "pcmanfm"])
if not "Discord" in windows and group == "7":
    subprocess.call(["qtile", "run-cmd", "discord"])
if not "Thunderbird" in windows and group == "5":
    subprocess.call(["qtile", "run-cmd", "thunderbird"])
if not "Steam" in windows and group == "A":
    subprocess.call(["qtile", "run-cmd", "steam"])
