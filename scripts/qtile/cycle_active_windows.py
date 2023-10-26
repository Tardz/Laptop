#!/usr/bin/env python

import subprocess
import sys

app = sys.argv[1]
group = sys.argv[2]

windows_list = subprocess.check_output(["wmctrl", "-l"]).decode("utf-8")
print(windows_list)

filtered_windows = [line.split()[0] for line in windows_list.splitlines() if app in line.lower() and group in line.lower()]
print(filtered_windows)

active_window_info = subprocess.check_output(["xprop", "-root", "_NET_ACTIVE_WINDOW"]).decode("utf-8")

active_window = active_window_info.split(" ")[-1].strip()
active_window = "0x0" + active_window[2:]

# Find the index of the current window in the list
current_index = -1
for i, window_id in enumerate(filtered_windows):
    print(window_id)
    if window_id in active_window:
        current_index = i
        break

if current_index == -1:
    # Current window not found in the list
    exit(1)

# Calculate the index of the next window in a cyclic manner
next_index = (current_index + 1) % len(filtered_windows)

# Activate the next window in the list
subprocess.run(["wmctrl", "-i", "-a", filtered_windows[next_index]])