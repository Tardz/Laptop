#!/usr/bin/env python

import re
import subprocess

p = subprocess.Popen(['xprop', '-notype', 'WM_CLASS'], stdout=subprocess.PIPE)
out, _ = p.communicate()

wm_class = str(out).split('"')[1]

if not wm_class:
    exit(1)

with open('/home/jonalm/.config/qtile/config.py', 'r') as f:
    config_lines = f.readlines()

data = subprocess.check_output(["qtile", "cmd-obj", "-o", "group", "-f", "info"]).decode().strip()
match = re.search(r"'name': '([^']+)',", data)

if match:
    group = match.group(1)
else:
    exit(2)

for line in config_lines:
    if f'            Match(wm_class = ["{wm_class}"]),' in line:
        print(wm_class)
        exit(3)

for i, line in enumerate(config_lines):
    if f"Group('{match.group(1)}'," in line:
        break

start_i = i + 1

new_line = f'            Match(wm_class = ["{wm_class}"]),\n'
config_lines.insert(start_i, new_line)

with open('/home/jonalm/.config/qtile/config.py', 'w') as f:
    f.writelines(config_lines)

subprocess.run(["qtile", "cmd-obj", "-o", "cmd", "-f", "restart"])

print(wm_class)