#!/usr/bin/env python

import json
import subprocess
import re
from datetime import datetime

dunstctl_command = "dunstctl history list"
output = subprocess.check_output(dunstctl_command, shell=True, text=True)

data = json.loads(output)

last_relevent_notification = ""

ignored_notifications = [
    "Time:", 
    "spotify"
]

if data['data'] != [[]]: 
    last_relevent_notification = data['data'][0][0]['summary']['data']
    for entry in data['data'][0]:
        appname = entry['appname']['data']

        if not any(keyword.lower() in appname.lower() for keyword in ignored_notifications):
            last_relevent_notification = appname
            break

print(last_relevent_notification)