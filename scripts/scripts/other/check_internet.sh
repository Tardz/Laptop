#!/bin/sh

# Check for an active internet connection
if ! ping -q -c 1 -W 1 google.com >/dev/null; then
    # No internet connection
    notify-send -u critical -t 3000 "No Internet Connection" "Failed to synchronize due to a lack of internet connectivity."
    exit 1
else
    exit 0
fi
