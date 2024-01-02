#!/usr/bin/env python

import subprocess
import re
import sys

subprocess.call(["qtile", "cmd-obj", "-o", "cmd", "-f", "next_screen"])

data = subprocess.check_output(["qtile", "cmd-obj", "-o", "group", "-f", "info"]).decode().strip()

match = re.search(r"'name': '([^']+)',", data)

next_screen_group = None

if match:
    next_screen_group = match.group(1)
else:
    print("group not found. Error: ", match)
    sys.exit(1)

print(next_screen_group)
sys.exit(0)