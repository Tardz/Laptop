#!/usr/bin/env python

import json
import subprocess
import re
from datetime import datetime

count_output = subprocess.check_output(["dunstctl", "count"]).decode("utf-8")
currently_displayed_count = int(count_output.split("\n")[1].split(":")[1].strip())
history_count = count_output.split("\n")[2].split(":")[1].strip()

if currently_displayed_count > 0:
    subprocess.run(["dunstctl", "close-all"])
else: 
    dunstctl_command = "dunstctl history list"
    output = subprocess.check_output(dunstctl_command, shell=True, text=True)

    data = json.loads(output)

    notification_ids = []  # Store notification IDs

    # Assuming you have a loop here
    if data['data'] != [[]]: 
        subprocess.run(['notify-send', '-t', '0', '-a', 'notification_center_clear', '-h', "int:transient:1", '-u', 'low', "⠀", "<span size='large'><b>Notification Center</b></span>\n<span foreground='#5a677f' size='large'>━━━━━━━━━━━━━━━━━━━</span>\n<span foreground='#a3be8c' size='medium'><b>" + history_count + "</b></span> <span size='medium'>Available</span> [<span foreground='#81a1c1' size='small'><b>Clear</b></span>]"])
        for entry in data['data'][0]:
            message = entry['message']['data']

            appname = entry['appname']['data']
            if "Time" in appname:
                timestamp = appname
                timestamp = timestamp[len("Time:"):]
                # Convert the specific time to a datetime object
                specific_time = datetime.strptime(timestamp, "%H:%M:%S")

                # Get the current time
                current_time = datetime.now()

                # Calculate the time difference
                time_difference = current_time - specific_time

                # Extract hours, minutes, and seconds from the time difference
                hours, remainder = divmod(time_difference.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                timestamp = ""
                if hours > 0:
                    timestamp += f"{hours}h "
                if minutes > 0:
                    timestamp += f"{minutes}m "
                if seconds > 0 or not (hours or minutes):
                    timestamp += f"{seconds}s"

                timestamp = " <small>" + timestamp + " ago</small>"
            else:
                timestamp = ""

            # Use a regular expression to extract title and body
            match = re.search(r'<b>(.*?)<\/b>(.*)', message, re.DOTALL)

            if match:
                title = match.group(1)
                body = match.group(2).strip() + timestamp
            else:
                title = "No title found"
                body = "No body found"

            # Store the notification ID
            notification_id = entry['id']['data']
            notification_ids.append(notification_id)

            urgency = "low"

            print("title:", title)
            print("body:", body)

            subprocess.run(['notify-send', '-t', '0', '-h', "int:transient:1", '-u', urgency, title, body])
    else:
        subprocess.run(['notify-send', '-t', '0', '-h', "int:transient:1", '-u', 'low', "⠀", "<span size='large'><b>Notification Center</b></span>\n<span foreground='#5a677f' size='large'>━━━━━━━━━━━━━━━━━━━</span>\n<span foreground='#bf616a' size='medium'><b>" + history_count + "</b></span> <span size='medium'>Available</span>"])

