#!/bin/bash
echo -n -e "${BOLD}Restart${RESET} is needed to continue the ${GREEN}installation${RESET}, restart now?${ORANGE}(y/n)${RESET}: "
read choice

if [[ "$choice" == "y" ]]; then
    umount -l /mnt
    shutdown now
fi