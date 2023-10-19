#!/usr/bin/env python

import subprocess

p = subprocess.Popen(['xprop', '-notype', 'WM_CLASS'], stdout=subprocess.PIPE)
out, _ = p.communicate()

wm_class = str(out).split('"')[1]

if not wm_class:
    exit(1)

with open('/home/jonalm/.config/qtile/config.py', 'r') as f:
    config_lines = f.readlines()

line_index = None
for i, line in enumerate(config_lines):
    if f'Match(wm_class = "{wm_class}")' in line:
        line_index = i
        break 

if not line_index:
    print(wm_class)
    exit(2)
    
config_lines.pop(line_index)

with open('/home/jonalm/.config/qtile/config.py', 'w') as f:
    f.writelines(config_lines)

subprocess.run(["qtile", "cmd-obj", "-o", "cmd", "-f", "restart"])

print(wm_class)