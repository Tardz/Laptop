#!/usr/bin/env python

import subprocess

# Use xprop to get the WM_CLASS property of the window
p = subprocess.Popen(['xprop', '-notype', 'WM_CLASS'], stdout=subprocess.PIPE)
out, _ = p.communicate()

# Extract the WM_CLASS value from the output
wm_class = str(out).split('"')[1]

if not wm_class:
    exit(1)

# Read the existing qtile config file
with open('/home/jonalm/.config/qtile/config.py', 'r') as f:
    config_lines = f.readlines()

# Find the index of the line to be removed
line_index = None
for i, line in enumerate(config_lines):
    if f'Match(wm_class = ["{wm_class}"])' in line:
        line_index = i
        break

if not line_index:
    print(wm_class)
    exit(2)

# Remove the line
config_lines.pop(line_index)

# Write the updated config file
with open('/home/jonalm/.config/qtile/config.py', 'w') as f:
    f.writelines(config_lines)

# Restart qtile
subprocess.run(["qtile", "cmd-obj", "-o", "cmd", "-f", "restart"])

print(wm_class)