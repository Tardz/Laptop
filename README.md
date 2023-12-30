# Qtile On Laptop **(Under progress, do not install)**

## About

### Qtile conf

### Scripts
**The structure of my scripts dir and how things are connected.**

![Static Badge](https://img.shields.io/badge/Drive-none?style=for-the-badge&color=%23bf616a)

These scripts automatically get executed when adding to the search menu and also on startup to keep everything up to date.  

**[Scripts used by search menu]**

* **Bisync drive** - Syncs the cloud to match the local directory
* **Sync drive** - Syncs the local directory to match the cloud

![Static Badge](https://img.shields.io/badge/Other-none?style=for-the-badge&color=%23d08770)

* **Arch install script** - Installs arch with my personal configs **[In progress]**
* **Check internet** - Checks internet connection and displays dunst notification
* **Get current screen** - Prints current focused screen by index
* **Get notifications** - Displays the most recent notifications
* **Get recent urgent notification** - Used by bar widget to get the most recent urgent notification to display

![Static Badge](https://img.shields.io/badge/Qtile-none?style=for-the-badge&color=%23ebcb8b)

**[Scripts used by Qtile]**

* **Floating**
   * Remove floating (py) - 
   * Remove floating (sh) - 
   * Add floating (py) - 
   * Add floating (sh) - 
* **Groups** 
* **Check and launch app** - 
* **Cycle active windows** - 
* **Get bluetooth on** - 
* **Get next screen group** - 
* **Mute or unmute** - 

![Static Badge](https://img.shields.io/badge/Rofi-none?style=for-the-badge&color=%23a3be8c)

![Static Badge](https://img.shields.io/badge/Systemd-none?style=for-the-badge&color=%238fbcbb)

![Static Badge](https://img.shields.io/badge/Term-none?style=for-the-badge&color=%2381A1C1)

![Static Badge](https://img.shields.io/badge/Udev-none?style=for-the-badge&color=%239B98B7)


### Integrated Qtile menus

## Hardware and system information
A brief overview of what software and hardwareI am using.

| Category           | Info                        |
|--------------------|-----------------------------|
|![Static Badge](https://img.shields.io/badge/Device-none?style=for-the-badge&logo=windows%20terminal&logoColor=%23bf616a&color=%23353b4a)|Asus rog g14 GA401QE 2021|
|![Static Badge](https://img.shields.io/badge/Os-none?style=for-the-badge&logo=windows%20terminal&logoColor=%23d08770&color=%23353b4a)|Arch|
|![Static Badge](https://img.shields.io/badge/Kernel-none?style=for-the-badge&logo=windows%20terminal&logoColor=%23ebcb8b&color=%23353b4a)|linux-g14|
|![Static Badge](https://img.shields.io/badge/Window%20manager-none?style=for-the-badge&logo=power%20virtual%20agents&logoColor=%23a3be8c&color=%23353b4a)|Qtile|
|![Static Badge](https://img.shields.io/badge/Display%20server-none?style=for-the-badge&logo=visual%20studio%20code&logoColor=%238fbcbb&color=%23353b4a)|X11|
|![Static Badge](https://img.shields.io/badge/Boot%20loader-none?style=for-the-badge&logo=files&logoColor=%2381A1C1&color=%23353b4a)|Grub|

| Category           | Software                    |
|--------------------|-----------------------------|
|![Static Badge](https://img.shields.io/badge/Terminal-none?style=for-the-badge&logo=windows%20terminal&logoColor=%23bf616a&color=%23353b4a)|Alacritty|
|![Static Badge](https://img.shields.io/badge/Shell-none?style=for-the-badge&logo=windows%20terminal&logoColor=%23d08770&color=%23353b4a)|Fish|
|![Static Badge](https://img.shields.io/badge/Fetch-none?style=for-the-badge&logo=windows%20terminal&logoColor=%23ebcb8b&color=%23353b4a)|Neofetch|
|![Static Badge](https://img.shields.io/badge/Notifications-none?style=for-the-badge&logo=power%20virtual%20agents&logoColor=%23a3be8c&color=%23353b4a)|Dunst|
|![Static Badge](https://img.shields.io/badge/Code%20Editor-none?style=for-the-badge&logo=visual%20studio%20code&logoColor=%238fbcbb&color=%23353b4a)|Visual Studio Code|
|![Static Badge](https://img.shields.io/badge/File%20manager-none?style=for-the-badge&logo=files&logoColor=%2381A1C1&color=%23353b4a)|Ranger|
|![Static Badge](https://img.shields.io/badge/Browser-none?style=for-the-badge&logo=firefox%20browser&logoColor=%239B98B7&color=%23353b4a)|Firefox|

## Setup

### Prerequisites
* qtile-extras

   ```sh
   sudo pacman -S qtile-extras
   ```

### Installation 
Installation is quite simple but in case someone needs it I created a install script to get up and running. To manually install move the config file from the git repo to your qtile folder with the name "config.py" and be sure to move the scripts folder to your home directory for the qtile menus to function.

* Clone the repo

   ```sh
   git clone https://github.com/Tardz/Laptop.git
   ```   
* Move into the Laptop directory
  
   ```sh
   cd Laptop/
   ```
* Run install script located at Laptop/install.sh
  
   ```sh
   ./install.sh
   ```

* Remove the git repo **(optional)**
  
   ```sh
   cd ..
   rm -r Laptop/
   ```

* Restart Qtile
  
   ```sh
   qtile cmd-obj -o cmd -f restart
   ```

**NOTE:** The install script will rename your current qtile config on your system to "config.bak" but will still remain in the same directory. 

### Uninstallation
To uninstall simply rename your previous config within the qtile directory to "config.py" instead of "config.bak" and then delete the scripts directory located at your home root. Restart qtile to read from your old config.

* Rename config file
  
   ```sh
   mv config.bak config.py
   ```

* Remove scripts directory
  
   ```sh
   rm -r scripts/
   ```

* Restart Qtile
  
   ```sh
   qtile cmd-obj -o cmd -f restart
   ```


## Workflow

### Keybindings
### Groups
### Window switching
### Dual monitor handling

## Contact

## Acknowledgments

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.
