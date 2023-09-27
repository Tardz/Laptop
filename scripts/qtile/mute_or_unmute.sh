#!/bin/bash

# Check if audio is muted
if pactl list sinks | grep -q "Mute: yes"; then
    # If muted, unmute
    pactl set-sink-mute @DEFAULT_SINK@ 0
    echo "Audio unmuted"
else
    # If not muted, mute
    pactl set-sink-mute @DEFAULT_SINK@ 1
    echo "Audio muted"
fi