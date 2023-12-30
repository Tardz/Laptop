# Qtile On Laptop

## About

### Qtile conf

### Scripts

### Integrated Qtile menus

## Hardware and system information

**Device:** Asus rog g14 GA401QE 2021  

**OS:** Arch

**Kernel:** linux-g14

## Software
A brief overview of what software is on my system.

| Category           | Software                    |
|--------------------|-----------------------------|
| Window Manager     | Qtile                       |
| Terminal Emulator  | Alacritty                   |
| Fetch              | Neofetch                    |
| Code Editor        | Visual Studio Code          |
| Shell              | Fish                        |
| Web Browser        | Firefox                     |
| File Manager       | Ranger                      |
| Notifications      | Dunst                       |
| Display server     | X11                         |
| Boot loader        | Grub                        |

## Setup

### Prerequisites
* qtile-extras

   ```sh
   sudo pacman -S qtile-extras
   ```

### Installation 
Installation is quite simple but in case someone needs it I created an install script to get up and running. To manually install, move the config file from the git repo to your qtile folder with the name "config.py" and be sure to move the scripts folder to your home directory for the qtile menus to function.

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
To uninstall simply rename your previous config within the qtile directory to "config.py" instead of "config.bak" and then delete the scripts directory located at your home root. Then restart qtile to read from your old config.

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
