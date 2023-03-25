#!/usr/bin/env python

import subprocess
import re
import sys

subprocess.call(["qtile", "cmd-obj", "-o", "cmd", "-f", "next_screen"])

data = subprocess.check_output(["qtile", "cmd-obj", "-o", "group", "-f", "info"]).decode().strip()

match = re.search(r"'name': '(\d+)'", data)

if match:
    next_screen_group = match.group(1)
else:
    print("group not found. Error: ", match)
    exit

print(next_screen_group)
print(type(next_screen_group))