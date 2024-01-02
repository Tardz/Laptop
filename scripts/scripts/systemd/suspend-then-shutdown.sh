#!/bin/sh
delay=$((2*3600))
start=$(date +%s)
rtcwake -s $delay -m mem
end=$(date +%s)
if [ $((end-start)) -ge $delay ]; then
        systemd-run --on-active=5 systemctl poweroff
fi
