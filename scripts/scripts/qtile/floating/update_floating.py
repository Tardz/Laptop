#!/usr/bin/env python

import subprocess

p = subprocess.Popen(['xprop', '-notype', 'WM_CLASS'], stdout=subprocess.PIPE)
out, _ = p.communicate()

wm_class = str(out).split('"')[1]

if not wm_class:
    exit(1)

with open('/home/jonalm/.config/qtile/config.py', 'r') as f:
    config_lines = f.readlines()

wm_class_exists = any(f'Match(wm_class = "{wm_class}"),' in line for line in config_lines)

if wm_class_exists:
    print(wm_class)
    exit(2)
else:
    i = config_lines.index('### FLOATING LAYOUT SETTINGS AND ASSIGNED APPS ###\n')

    start_index = i + 8

    new_line = f'        Match(wm_class = "{wm_class}"),\n'
    config_lines.insert(start_index, new_line)

    with open('/home/jonalm/.config/qtile/config.py', 'w') as f:
        f.writelines(config_lines)

    subprocess.run(["qtile", "cmd-obj", "-o", "cmd", "-f", "restart"])

print(wm_class)