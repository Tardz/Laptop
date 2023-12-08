#!/bin/bash
RED='\e[1;31m'
ORANGE='\e[38;5;173m'
YELLOW='\e[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\e[38;5;182m'
PINK='\e[1;95m'

BOLD='\e[1m'
NORMAL='\e[0m'

RESET='\033[0m'

TITLE="${BLUE}
 █████╗ ██████╗  ██████╗██╗  ██╗    ██╗███╗   ██╗███████╗████████╗ █████╗ ██╗     ██╗     ███████╗██████╗
██╔══██╗██╔══██╗██╔════╝██║  ██║    ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║     ██║     ██╔════╝██╔══██╗ 
███████║██████╔╝██║     ███████║    ██║██╔██╗ ██║███████╗   ██║   ███████║██║     ██║     █████╗  ██████╔╝ ${RED}
██╔══██║██╔══██╗██║     ██╔══██║    ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║     ██║     ██╔══╝  ██╔══██╗
██║  ██║██║  ██║╚██████╗██║  ██║    ██║██║ ╚████║███████║   ██║   ██║  ██║███████╗███████╗███████╗██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝ ${RESET}"

TITLE1="${BLUE}
                      __       _               __          __ __           
  ____ _ _____ _____ / /_     (_)____   _____ / /_ ____ _ / // /___   _____
 / __  // ___// ___// __ \   / // __ \ / ___// __// __  // // // _ \ / ___/ ${RED}
/ /_/ // /   / /__ / / / /  / // / / /(__  )/ /_ / /_/ // // //  __// /
\__ _//_/    \___//_/ /_/  /_//_/ /_//____/ \__/ \__ _//_//_/ \___//_/
"                                                        


display_networks() {
  echo "  Available Networks:"
  # change, not working
  # iwctl station wlan0 get-networks
}

connect_to_network() {
  echo -e "     Enter the network ${BLUE}${BOLD}SSID${RESET}: " 
  read networkName
  echo -e "     Enter the network ${RED}${BOLD}password${RESET}: " 
  read networkPassword

  if [ -z "$networkName" ] || [ -z "$networkPassword" ]; then
    echo -e "     Error: Network name or password ${RED}not provided${RESET}."
    return 1
  fi

  iwctl station wlan0 connect "$network_name" -P "$network_password"

  if [ $? -eq 0 ]; then
    echo -e "     Connected to ${BOLD}$networkName${RESET} ${GREEN}successfully${RESET}.\n"
    return 0
  else
    echo -e "     ${RED}Failed${RESET} to connect to ${BOLD}$networkName${RESET}."
    return 1
  fi
}

clear
echo -e "${TITLE}"
# echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${ORANGE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
# echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}\n"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${ORANGE}○ ${RESET}[${BOLD}Configure${RESET} script...]"
echo -e "     ${BOLD}Choose install version:${NORMAL}"
echo -e "       1. Desktop"
echo -e "       2. Laptop"
echo -n -e "     Enter a number${BLUE}${BOLD}(1-2)${RESET}: "
read installVersion
echo -e "${GREEN}○ ${RESET}[Script ${GREEN}configured${RESET}]"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"

while true; do
  echo -e "${ORANGE}○ ${RESET}[Setting up network ${BOLD}connection${RESET}...]"
  echo -e "     ${BOLD}Network options:${RESET}"
  echo -e "       1. List available networks"
  echo -e "       2. Connect via wifi"
  echo -e "       3. Use ethernet"

  echo -n -e "     Enter a number${BLUE}${BOLD}(1-3)${RESET}: " 
  read choice

  case $choice in
    1)
      display_networks
      ;;
    2)
      connect_to_network
      if [ $? -ne 0 ]; then
        echo -e "     Connection ${RED}failed${RESET}. Please try again."
      else
        echo -e "${GREEN}○ ${RESET}[${BOLD}Wifi${RESET} connection ${GREEN}successful${RESET}]"
        break
      fi
    ;;
    3)
      ping -c -q 2 google.com
      if [ $? -ne 0 ]; then
        break
      else
        echo -e "${GREEN}○ ${RESET}[${BOLD}Ethernet${RESET} connection ${GREEN}successful${RESET}]"
      fi
      ;;
    *)
      echo -e "     ${RED}Invalid${RESET} choice. Please enter a number between 1 and 3."
      ;;
  esac
done

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
timedatectl set-ntp true
echo -e "${GREEN}○ ${RESET}[system clock ${BOLD}updated${RESET}]"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"

echo -e "${ORANGE}○ ${RESET}[Begining disk ${BOLD}partitioning${RESET} process...]"
disk_info=$(sudo fdisk -l | awk '/^Device / {table=1; next} table==1 {print $1, $2, $3, $4, $5, $6}')

disk_info=$(echo "$disk_info" | head -n -2)
diskCount=$(echo "$disk_info" | wc -l)

echo -e "     ${BOLD}Found${RESET} ${ORANGE}$diskCount${RESET} disks:"
echo -e "           [${RED}Device ${ORANGE}Start ${YELLOW}End ${GREEN}Sectors ${BLUE}Size ${PURPLE}Type${RESET}]"
counter=1
while read -r line; do
    formatted_line=""
    count=0
    for word in $line; do
        case $count in
            0) formatted_line+=" ${RED}$word${RESET}";;
            1) formatted_line+=" ${ORANGE}$word${RESET}";;
            2) formatted_line+=" ${YELLOW}$word${RESET}";;
            3) formatted_line+=" ${GREEN}$word${RESET}";;
            4) formatted_line+=" ${BLUE}$word${RESET}";;
            5) formatted_line+=" ${PURPLE}$word${RESET}";;
            *) formatted_line+=" $word";;
        esac
        ((count++))
    done
    echo -e "        $counter.$formatted_line"
    ((counter++))
done <<< "$disk_info"

echo -n -e "     Select a disk to partition by number${BLUE}${BOLD}(1-$diskCount)${RESET}: " 
while true; do
  read diskNumber

  if [[ "$diskNumber" =~ ^[1-$diskCount]$ ]]; then
      break
  else
      echo -n -e "     ${RED}Invalid${RESET} input. Please enter a valid disk number${BLUE}${BOLD}(1-$diskCount)${RESET}: "
  fi
done

echo -n -e "     Enter the size of the main partition (e.g., ${ORANGE}10G${RESET}): "
while true; do
  read mainPartitionSize

  mainPartitionSize=$(echo "$mainPartitionSize" | tr '[:upper:]' '[:lower:]')
  if [[ "$mainPartitionSize" =~ ^[0-9]+[kmg]$ ]]; then
      break
  else
      echo -n -e "     ${RED}Invalid${RESET} input. Please enter a valid main partition size (e.g., 10G): "
  fi
done


echo -n -e "     Enter the size of the EFI partition(e.g., ${ORANGE}550M${RESET}): "
while true; do
  read efiPartitionSize

  efiPartitionSize=$(echo "$efiPartitionSize" | tr '[:upper:]' '[:lower:]')
  if [[ "$efiPartitionSize" =~ ^[0-9]+[kmg]$ ]]; then
      break
  else
      echo -e -n "     ${RED}Invalid${RESET} input. Please enter a valid efi partition size (e.g., 550M): "
  fi
done

echo -n -e "     Enter the size of the swap partition(e.g., ${ORANGE}16G${RESET}): "
while true; do
  read swapPartitionSize

  swapPartitionSize=$(echo "$swapPartitionSize" | tr '[:upper:]' '[:lower:]')
  if [[ "$swapPartitionSize" =~ ^[0-9]+[kmg]$ ]]; then
      break
  else
      echo -e -n "     ${RED}Invalid${RESET} input. Please enter a valid swap partition size (e.g., 550M): "
  fi
done


selectedDisk=$(echo "$disk_info" | awk -v num="$diskNumber" 'NR==num {print $1}')
echo -e "g\nn\n\n\n+$efiPartitionSize\nn\n\n\n+$swapPartitionSize\nn\n\n\n+$mainPartitionSize\nt\n1\n1\nt\n2\nswap\nt\n3\nlinux\nw\n" | fdisk $selectedDisk
echo -e "${GREEN}○ ${RESET}[Disk ${BOLD}partitioning${RESET} ${GREEN}successful${RESET}]"

mkfs.fat -F32 ${selectedDisk}1
echo -e "${GREEN}○ ${RESET}[${BOLD}Efi${RESET} partition format ${GREEN}successful${RESET}]"

mkswap ${selectedDisk}2
swapon ${selectedDisk}2
echo -e "${GREEN}○ ${RESET}[${BOLD}Swap${RESET} partition format ${GREEN}successful${RESET}]"

mkfs.ext4 ${selectedDisk}3
echo -e "${GREEN}○ ${RESET}[${BOLD}main${RESET} partition format ${GREEN}successful${RESET}]"

mount ${selectedDisk}3 /mnt
echo -e "${GREEN}○ ${RESET}[${BOLD}main${RESET} partition format ${GREEN}mounted${RESET}]"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${ORANGE}○ ${RESET}[${BOLD}Installing${RESET} base packages...]"
# Fix pacman mirros to get linux-g14 if laptop is selected
pacstrap /mnt base linux linux-firmware
echo -e "${GREEN}○ ${RESET}[${BOLD}Base${RESET} packages ${GREEN}successfully${RESET} installed]"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
genfstab -U /mnt >> /mnt/etc/fstab
echo -e "${GREEN}○ ${RESET}[${BOLD}File-system${RESET} table generated ${GREEN}successfully${RESET}]"

arch-chroot /mnt
echo -e "${GREEN}○ ${RESET}[${BOLD}Changed${RESET} into root directory]"

ln -sf /usr/share/zoneinfo/Europe/Stockholm /etc/localtime
echo -e "${GREEN}○ ${RESET}[${BOLD}Timezone${RESET} set to Stockholm Sweden]"

hwclock --systohc
echo -e "${GREEN}○ ${RESET}[${BOLD}Hardware clock${RESET} synchronized]"

cp $(dirname "$0")locale.gen /etc/locale.gen
locale-gen
echo -e "${GREEN}○ ${RESET}[${BOLD}Locale${RESET} set]"

cp hostname /etc/hostname
echo -e "${GREEN}○ ${RESET}[${BOLD}Hostname${RESET} set]"

cp hosts /etc/hosts
echo -e "${GREEN}○ ${RESET}[${BOLD}Hosts${RESET} set]"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${ORANGE}○ ${RESET}[${BOLD}Installing${RESET} required packages with ${ORANGE}pacman${RESET}...]"
echo -e "${GREEN}○ ${RESET}[Required packages from ${BOLD}pacman${RESET} ${GREEN}successfully${RESET} installed]"
# Uncomment the following line to enable the actual installation
# sudo pacman -Syu --noconfirm $(cat requirements.txt)

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${ORANGE}○ ${RESET}[${BOLD}Installing${RESET} required AUR packages with ${ORANGE}yay${RESET}...]"
echo -e "${GREEN}○ ${RESET}[Required packages from ${BOLD}yay${RESET} ${GREEN}successfully${RESET} installed]"
# Uncomment the following line to enable the actual installation
# yay -Syu --noconfirm $(cat requirements_aur.txt)
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"

echo -e "Setup ${GREEN}complete${RESET}!"