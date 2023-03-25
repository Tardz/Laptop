#!/usr/bin/env python

import subprocess

# Use xprop to get the WM_CLASS property of the window
p = subprocess.Popen(['xprop', '-notype', 'WM_CLASS'], stdout=subprocess.PIPE)
out, _ = p.communicate()

# Extract the WM_CLASS value from the output
wm_class = str(out).split('"')[1]

# Read the existing qtile config file
with open('/home/jonalm/.config/qtile/config.py', 'r') as f:
    config_lines = f.readlines()

# Find the index of the floating_layout line
i = config_lines.index('### FLOATING LAYOUT SETTINGS AND ASSIGNED APPS ###\n')

# Find the index of the next line after the float_rules list
start_index = i + 8

# Add the new match rule to the float_rules list
new_line = f'        Match(wm_class="{wm_class}"),\n'
config_lines.insert(start_index, new_line)

# Write the updated config file
with open('/home/jonalm/.config/qtile/config.py', 'w') as f:
    f.writelines(config_lines)

# Restart qtile
subprocess.run(["qtile", "cmd-obj", "-o", "cmd", "-f", "restart"])