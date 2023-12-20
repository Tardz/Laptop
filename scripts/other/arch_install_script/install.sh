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
      ping -c 2 -q google.com
      if [ $? -ne 0 ]; then
        echo -e "     Connection ${RED}failed${RESET}. Please try again."
      else
        echo -e "${GREEN}○ ${RESET}[${BOLD}Ethernet${RESET} connection ${GREEN}successful${RESET}]"
        break
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
disk_info=$(fdisk -l | grep "Disk /" | awk -F'[ :,]+' '{print $2, $3, $4}')

echo $disk_info

diskCount=$(echo "$disk_info" | wc -l)

echo -e "     ${BOLD}Found${RESET} ${ORANGE}$diskCount${RESET} disks:"
echo -e "        (0) Skip partitioning"
counter=1
while read -r line; do
    formatted_line=""
    count=0
    for word in $line; do
        case $count in
            0) formatted_line+=" ${RED}$word${RESET}";;
            1) formatted_line+=" ${ORANGE}$word${RESET}";;
            2) formatted_line+=" ${ORANGE}$word${RESET}";;
            *) formatted_line+=" $word";;
        esac
        ((count++))
    done
    echo -e "        ($counter)$formatted_line"
    ((counter++))
done <<< "$disk_info"

echo -n -e "     Select a disk to partition by number${BLUE}${BOLD}(1-$diskCount)${RESET}: " 
while true; do
    read diskNumber
    if [[ -z "$diskNumber" || "$diskNumber" -eq 0 ]]; then
        diskNumber=0  
        break
    elif [[ "$diskNumber" =~ ^[1-$diskCount]$ ]]; then
        break
    else
        echo -n -e "     ${RED}Invalid${RESET} input. Please enter a valid disk number${BLUE}${BOLD}(1-$diskCount)${RESET}: "
    fi
done

if [[ ! "$diskNumber" -eq 0 ]]; then
    echo -n -e "     Enter the size of the main partition(Default ${ORANGE}40G${RESET}): "
    while true; do
        read mainPartitionSize
        mainPartitionSize=$(echo "$mainPartitionSize" | tr '[:upper:]' '[:lower:]')
        
        if [[ -z "$mainPartitionSize" ]]; then
            mainPartitionSize="40g"
            break
        elif [[ "$mainPartitionSize" =~ ^[0-9]+[kmg]$ ]]; then
            break
        else
            echo -n -e "     ${RED}Invalid${RESET} input. Please enter a valid main partition size (e.g., ${ORANGE}40G${RESET}): "
        fi
    done


    echo -n -e "     Enter the size of the EFI partition(Default ${ORANGE}550M${RESET}): "
    while true; do
        read efiPartitionSize
        efiPartitionSize=$(echo "$efiPartitionSize" | tr '[:upper:]' '[:lower:]')

        if [[ -z "$efiPartitionSize" ]]; then
            efiPartitionSize="550m"
            break
        elif [[ "$efiPartitionSize" =~ ^[0-9]+[kmg]$ ]]; then
            break
        else
            echo -e -n "     ${RED}Invalid${RESET} input. Please enter a valid efi partition size (e.g., ${ORANGE}550M${RESET}: "
        fi
    done

    echo -n -e "     Enter the size of the swap partition(Default ${ORANGE}8g CHANGE LATERG${RESET}): "
    while true; do
        read swapPartitionSize
        swapPartitionSize=$(echo "$swapPartitionSize" | tr '[:upper:]' '[:lower:]')

        if [[ -z "$swapPartitionSize" ]]; then
            swapPartitionSize="550m"
            break
        elif [[ "$swapPartitionSize" =~ ^[0-9]+[kmg]$ ]]; then
            break
        else
            echo -e -n "     ${RED}Invalid${RESET} input. Please enter a valid swap partition size (e.g., ${ORANGE}8g CHANGE LATERG${RESET}): "
        fi
    done

    selectedDisk=$(echo "$disk_info" | awk -v num="$diskNumber" 'NR==num {print $1}')
    echo -e "g\nn\n\n\n+$efiPartitionSize\nn\n\n\n+$swapPartitionSize\nn\n\n\n+$mainPartitionSize\nt\n1\n1\nt\n2\nswap\nt\n3\nlinux\nw\n" | fdisk $selectedDisk
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}○ ${RESET}[Disk ${BOLD}partitioning${RESET} ${RED}failed${RESET}]"
        exit 1
    fi
    echo -e "${GREEN}○ ${RESET}[Disk ${BOLD}partitioning${RESET} ${GREEN}successful${RESET}]"

    mkfs.fat -F32 ${selectedDisk}1
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}○ ${RESET}[${BOLD}Efi${RESET} partition format ${RED}failed${RESET}]"
        exit 1
    fi
    echo -e "${GREEN}○ ${RESET}[${BOLD}Efi${RESET} partition format ${GREEN}successful${RESET}]"

    mkswap ${selectedDisk}2
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}○ ${RESET}[${BOLD}Swapon${RESET} ${RED}failed${RESET}]"
        exit 1
    fi
    echo -e "${GREEN}○ ${RESET}[${BOLD}Swap${RESET} partition format ${GREEN}successful${RESET}]"

    swapon ${selectedDisk}2
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}○ ${RESET}[${BOLD}Swapon${RESET} ${RED}failed${RESET}]"
        exit 1
    fi
    echo -e "${GREEN}○ ${RESET}[${BOLD}Swapon${RESET} ${GREEN}successful${RESET}]"

    mkfs.ext4 ${selectedDisk}3
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}○ ${RESET}[${BOLD}main${RESET} partition format ${RED}failed${RESET}]"
        exit 1
    fi
    echo -e "${GREEN}○ ${RESET}[${BOLD}main${RESET} partition format ${GREEN}successful${RESET}]"
fi

mount ${selectedDisk}3 /mnt
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[${RED}Failed${RESET} to ${BOLD}mount${RESET} partition]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[${BOLD}main${RESET} partition ${GREEN}mounted${RESET}]"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${ORANGE}○ ${RESET}[${BOLD}Installing${RESET} base packages...]"
# Fix pacman mirros to get linux-g14 if laptop is selected
pacstrap /mnt base linux linux-firmware --noconfirm
echo -e "${GREEN}○ ${RESET}[${BOLD}Base${RESET} packages ${GREEN}successfully${RESET} installed]"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
genfstab -U /mnt >> /mnt/etc/fstab
echo -e "${GREEN}○ ${RESET}[${BOLD}File-system${RESET} table generated ${GREEN}successfully${RESET}]"

# mount --rbind /sys /mnt/sys
# mount --make-rslave /mnt/sys
# mount --rbind /proc /mnt/proc
# mount --make-rslave /mnt/proc
# mount --rbind /dev /mnt/dev
# mount --make-rslave /mnt/dev

cp -r locale.gen /mnt/etc/locale.gen
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[Could ${RED}not${RESET} copy and send ${BOLD}locale.gen${RESET}]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[${BOLD}Locale${RESET} sent to disk]"

cp -r hosts /mnt/etc/hosts
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[Could ${RED}not${RESET} copy and send ${BOLD}hosts${RESET}]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[${BOLD}Hosts${RESET} sent to disk]"

cp -r hostname /mnt/etc/hostname
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[Could ${RED}not${RESET} copy and send ${BOLD}hostname${RESET}]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[${BOLD}Hostname${RESET} sent to disk]"

echo -n -e "  ${BOLD}Enter${RESET} a new root password: "
read rootPasswrd
while true; do
    echo -n -e "  ${BOLD}Retype${RESET} password: "
    read retypedRootPasswrd

    if [[ ! -z "$retypedRootPasswrd" && "$retypedRootPasswrd" == "$rootPasswrd" ]]; then
        break
    else
        echo -e -n "  ${RED}Invalid${RESET} password. Please try again: "
    fi
done

echo -n -e "  ${BOLD}Create${RESET} a new user, enter a name: "
read userName
echo -n -e "  ${BOLD}Enter${RESET} a new password for ${ORANGE}$userName${RESET}: "
read userPasswrd
while true; do
    echo -n -e "  ${BOLD}Retype${RESET} password: "
    read retypedUserPasswrd

    if [[ ! -z "$retypedUserPasswrd" && "$retypedUserPasswrd" == "$userPasswrd" ]]; then
        break
    else
        echo -e -n "  ${RED}Invalid${RESET} password. Please try again: "
    fi
done

packageList=$(tr '\n' ' ' < "packages.txt")
aurPackageList=$(tr '\n' ' ' < "packages.txt")

# > /dev/null 2>&1
arch-chroot /mnt <<EOF 

ln -sf /usr/share/zoneinfo/Europe/Stockholm /etc/localtime
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[Could ${RED}not${RESET} set ${BOLD}Timezone${RESET} to ${ORANGE}Stockholm Sweden${RESET}]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[${BOLD}Timezone${RESET} set to Stockholm Sweden]"

hwclock --systohc
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[Clock synchronization ${RED}failed${RESET}]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[${BOLD}Hardware clock${RESET} synchronized]"

locale-gen
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[${ORANGE}Locale${RESET} ${BOLD}generation${RESET} ${RED}failed${RESET}]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[${ORANGE}Locale${RESET} ${BOLD}generated${RESET}]"

# echo "$rootPasswrd\n$retypedRootPasswrd\n" | passwd root
echo 'root:$rootPasswrd' | chpasswd
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[Root ${RED}password${RESET} ${BOLD}change${RESET} ${RED}failed${RESET}]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[Root ${BOLD}password${RESET} ${GREEN}changed${RESET}]"

useradd -m $userName
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[User ${RED}$userName${RESET} ${BOLD}creation${RESET} ${RED}failed${RESET}]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[User ${BOLD}$userName${RESET} ${GREEN}created${RESET}]"

# echo "$userPasswrd\n$retypedUserPasswrd\n" | passwd $userName
echo '$userName:$userPasswrd' | chpasswd
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[$userName ${RED}password${RESET} ${BOLD}change${RESET} ${RED}failed${RESET}]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[User ${BOLD}$userName${RESET} ${GREEN}set${RESET}]"

usermod -aG wheel,audio,video,optical,storage,docker,sudo,network $userName
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[Adding ${BOLD}$userName${RESET} to groups ${RED}failed${RESET}]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[${GREEN}Added${RESET} ${BOLD}$userName${RESET} to groups]"

echo -e "${ORANGE}○ ${RESET}[${BOLD}Updating${RESET} system packages...]"
pacman -Syu --noconfirm archlinux-keyring
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[${BOLD}System${RESET} packages ${RED}faild${RESET} to update]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[${BOLD}System${RESET} packages ${GREEN}update${RESET} successfull]"

echo -e "${ORANGE}○ ${RESET}[${BOLD}Installing${RESET} required packages with ${ORANGE}pacman${RESET}...]"
pacman -Sy --noconfirm $packageList
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[Required packages from ${BOLD}pacman${RESET} ${RED}faild${RESET} to install]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[Required packages from ${BOLD}pacman${RESET} ${GREEN}successfully${RESET} installed]"

mkdir /boot/efi
mount "$disk_info"1 /boot/efi
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[${RED}Failed${RESET} to ${BOLD}mount${RESET} /boot/efi to efi partition]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[${BOLD}/boot/efi${RESET} ${GREEN}successfully${RESET} mounted]"

grub-install --target=x86_64-efi --bootloader-id=grub_uefi --recheck
mount "$disk_info"1 /boot/efi
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[${RED}Failed${RESET} to ${BOLD}install${RESET} grub]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[${BOLD}grub${RESET} ${GREEN}successfully${RESET} installed]"

grub-mkconfig -o /boot/grub/grub.cfg
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[${RED}Failed${RESET} to ${BOLD}update${RESET} grub]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[${BOLD}grub${RESET} ${GREEN}successfully${RESET} updated]"

echo "$userName ALL=(ALL) NOPASSWD" | sudo EDITOR="tee -a" visudo
echo "$userName ALL=(ALL) NOPASSWD: /usr/bin/makepkg" | sudo EDITOR="tee -a" visudo
if [[ $? -ne 0 ]]; then
    echo -e "${RED}○ ${RESET}[${BOLD}Sudoers${RESET} file ${RED}failed${RESET} to configure]"
    exit 1
fi
echo -e "${GREEN}○ ${RESET}[${BOLD}Sudoers${RESET} file ${GREEN}successfully${RESET} configured]"
EOF

echo -e "Setup ${GREEN}complete${RESET}!"

echo -n -e "${BOLD}Restart${RESET} is needed to continue the ${GREEN}installation${RESET}, restart now?${ORANGE}(y/n)${RESET}: "
read choice

if [[ "$choice" == "y" ]]; then
    umount -l /mnt
    shutdown now
fi