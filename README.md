# Qtile On Laptop 
**(Under progress, do not install)**
## Preview
<p align="center">
  <img src="https://github.com/Tardz/Laptop/blob/main/readme_images/desktop_screenshot_modified.png" alt="Image 1" width="850" />
  <img src="https://github.com/Tardz/Laptop/blob/main/readme_images/desktop_screenshot.png" alt="Image 1" width="850" />
</p>

<p align="center">
  <img src="https://github.com/Tardz/Laptop/blob/main/readme_images/wifi_menu_screenshot_modified.png" alt="Image 1" width="350" />
  <img src="https://github.com/Tardz/Laptop/blob/main/readme_images/bluetooth_menu_screenshot_modified.png" alt="Image 2" width="350" />
  <img src="https://github.com/Tardz/Laptop/blob/main/readme_images/volume_menu_screenshot_modified.png" alt="Image 3" width="350" />
</p>

<p align="center">
  <img src="https://github.com/Tardz/Laptop/blob/main/readme_images/settings_menu_screenshot_modified.png" alt="Image 1" width="750" />
</p>

## About

### Qtile conf

### Scripts
**The structure of the scripts dir and how things are connected.**

![Static Badge](https://img.shields.io/badge/Drive-none?style=for-the-badge&color=%23bf616a)

These scripts automatically get executed when adding to the search menu aswell as on startup to keep everything up to date.  

**[Scripts used by search menu]**

* **Bisync drive** - Syncs the cloud to match the local directory
* **Sync drive** - Syncs the local directory to match the cloud

![Static Badge](https://img.shields.io/badge/Qtile-none?style=for-the-badge&color=%23ebcb8b)

**[Scripts used by Qtile]**

* **Floating**
   * Remove floating (py) - 
   * Remove floating (sh) - 
   * Add floating (py) - 
   * Add floating (sh) - 
* **Groups**
   * Remove group match (py) - 
   * Remove group match (sh) - 
   * Update group match (py) - 
   * Update group match (sh) - 
* **Check and launch app** - 
* **Cycle active windows** - 
* **Get bluetooth on** - 
* **Get next screen group** - 
* **Mute or unmute** - 

![Static Badge](https://img.shields.io/badge/Rofi-none?style=for-the-badge&color=%23a3be8c)

**[Scripts used by Rofi]**

* **Automation**
   * Automation -  
   * Revert files - 
   * Save files - 
   * Automation options - 
* **Config** 
   * Config file add (py) - 
   * Config file add (sh) -  
   * Config file remove (py) - 
   * Config file remove (sh) - 
   * Config files - 
   * Config options - 
* **Search**
   * Search add (py) - 
   * Search add (sh) - 
   * Search remove (py) -  
   * Search remove (sh) -  
   * Search web -  

![Static Badge](https://img.shields.io/badge/Systemd-none?style=for-the-badge&color=%238fbcbb)

**[Scripts used by Systemd]**

* **Suspend then shutdown** -

![Static Badge](https://img.shields.io/badge/Udev-none?style=for-the-badge&color=%239B98B7)

**[Scripts used by Udev]**

* **Power change** -

![Static Badge](https://img.shields.io/badge/Term-none?style=for-the-badge&color=%2381A1C1)

* **Reset screens** -
* **Show Keybindings** -

![Static Badge](https://img.shields.io/badge/Other-none?style=for-the-badge&color=%23d08770)

* **Arch install script** - Installs arch with my personal configs **[In progress]**
* **Check internet** - Checks internet connection and displays dunst notification
* **Get current screen** - Prints current focused screen by index
* **Get notifications** - Displays the most recent notifications
* **Get recent urgent notification** - Used by bar widget to get the most recent urgent notification to display

### Integrated Qtile menus

## Hardware and system information
A brief overview of what software and hardwareI am using.


<p align="start">
  <img src="https://github.com/Tardz/Laptop/blob/main/software_sheet_screenshot.png" alt="Image 1" width="340" />
  <img src="https://github.com/Tardz/Laptop/blob/main/info_sheet_screenshot.png" alt="Image 1" width="340" height="315" />
</p>

## Setup

### Prerequisites
* qtile-extras

   ```sh
   sudo pacman -S qtile-extras
   ```

### Installation 
Installation is quite simple but in case someone needs it I created an install script to get up and running. To manually install move the config file from the git repo to your qtile folder with the name "config.py" and be sure to move the scripts folder to your home directory for the qtile menus to function.

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

**NOTE:** The install script will rename your current qtile config on your system to "config.bak" but it will still remain in the same directory. 

### Uninstallation
To uninstall simply delete the current config and rename your previous config within the qtile directory to "config.py" instead of "config.bak", then delete the scripts directory located at your home root. Restart qtile to read from your old config.

* Remove current config
  
   ```sh
   rm config.py
   ```

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
