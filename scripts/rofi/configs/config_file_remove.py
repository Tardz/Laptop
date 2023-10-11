#!/usr/bin/env python

import sys

arg = sys.argv[1]

with open('/home/jonalm/scripts/rofi/config/config_options.sh', 'r') as f:
    config_options_lines = f.readlines()

for i, line in enumerate(config_options_lines):
    if arg in line:
        break

config_options_lines.pop(i)

with open('/home/jonalm/scripts/rofi/config/config_options.sh', 'w') as f:
    f.writelines(config_options_lines)