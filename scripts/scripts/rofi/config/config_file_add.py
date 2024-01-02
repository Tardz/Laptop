#!/usr/bin/env python

import sys

arg = sys.argv[1]

with open('/home/jonalm/scripts/rofi/config/config_options.sh', 'r') as f:
    config_lines = f.readlines()

for i, line in enumerate(config_lines):
    if "declare -a options=" in line:
        break

start_index = i + 1

config_lines.insert(start_index, f"'{arg}'\n")
 
with open('/home/jonalm/scripts/rofi/config/config_options.sh', 'w') as f:
    f.writelines(config_lines)