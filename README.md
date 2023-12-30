# Qtile and integrated menus

## About

#### Qtile conf

#### Scripts

#### Integrated Qtile menus

## Hardware and system information

**Device:** Asus rog g14 GA401QE 2021  

**OS:** Arch

**Kernel:** linux-g14

## Software
A brief overview of what software comprises my system

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

## Setup

#### Prerequisites
* qtile-extras

   ```sh
   sudo pacman -S qtile-extras
   ```

#### Installation 

* Clone the repo

   ```sh
   git clone https://github.com/Tardz/Laptop.git
   ```   
* Run install script located at Laptop/install.sh
  
   ```js
   ./install.sh
   ```
* Restart Qtile
  
   ```js
   qtile cmd-obj -o cmd -f restart
   ```
<code style="color : red">Attention</code>
!**Attention:**
The install script will rename your current qtile config on your system to "config.bak" but will still remain in the same directory. 

## Workflow

#### Keybindings
#### Groups
#### Window switching
#### Dual monitor handling

## Contact

## Acknowledgments

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

