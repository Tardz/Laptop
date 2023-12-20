#!/bin/bash


cd home/$userName
su -c "git clone https://aur.archlinux.org/yay.git" $userName
cd yay
sudo -u $userName makepkg -si

echo -e "${ORANGE}○ ${RESET}[${BOLD}Installing${RESET} required AUR packages with ${ORANGE}yay${RESET}...]"
su -c "yay -S --noconfirm $aurPackageList" $userName
echo -e "${GREEN}○ ${RESET}[Required packages from ${BOLD}yay${RESET} ${GREEN}successfully${RESET} installed]"


systemctl enable NetworkManager
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[${RED}Failed${RESET} to enable ${BOLD}NetworkManager${RESET}]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[${BOLD}NetworkManager${RESET} enabled ${GREEN}successfully${RESET}]"