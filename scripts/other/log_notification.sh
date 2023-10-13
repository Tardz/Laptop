#!/bin/bash

logfile="~/scripts/other/notification_log.txt"

dunstctl subscribe | while read -r line; do
    echo "$line" >> "$logfile"
done