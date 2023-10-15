#!/usr/bin/env python

import json
import subprocess
import re
from datetime import datetime

count_output = subprocess.check_output(["dunstctl", "count"]).decode("utf-8")
currently_displayed_count = int(count_output.split("\n")[1].split(":")[1].strip())

if currently_displayed_count > 0:
    subprocess.run(["dunstctl", "close-all"])
else: 
    dunstctl_command = "dunstctl history list"
    output = subprocess.check_output(dunstctl_command, shell=True, text=True)

    data = json.loads(output)

    notification_ids = []  # Store notification IDs

    current_time = datetime.now()

    # Assuming you have a loop here
    for entry in data['data'][0]:
        message = entry['message']['data']

        # Use a regular expression to extract title and body
        match = re.search(r'<b>(.*?)<\/b>(.*)', message, re.DOTALL)

        if match:
            title = match.group(1)
            body = match.group(2).strip()
        else:
            title = "No title found"
            body = "No body found"

        # Store the notification ID
        notification_id = entry['id']['data']
        notification_ids.append(notification_id)

        urgency = "low"

        print("title:", title)
        print("body:", body)

        subprocess.run(['notify-send', '-t', '0', '-h', "int:transient:1", '-u', urgency, title, body, '-a', 'history_script'])

