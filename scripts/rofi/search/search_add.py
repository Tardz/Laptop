#!/usr/bin/env python

import sys

arg = sys.argv[1]

with open('Insync/johalm123@gmail.com/Google%20Drive/Arch_delat/search_options.sh', 'r') as f:
    web_search_lines = f.readlines()

for i, line in enumerate(web_search_lines):
    if "declare -a options=" in line:
        break

start_index = i + 1

web_search_lines.insert(start_index, f"'{arg}'\n")
 
with open('Insync/johalm123@gmail.com/Google\ Drive/Arch_delat/search_options.sh', 'w') as f:
    f.writelines(web_search_lines)