### ENVIROMENTAL VARIABLES ###
set -U fish_user_paths /home/jonalm/Documents/uni/2/pintos/utils $fish_user_paths
# export DUNSTRC=/home/jonalm/.config/dunst/dunstrc.ini
# set -U fish_user_paths /home/jonalm/android/Sdk/emulator/qemu/linux-x86_64/ $fish_user_paths
# set -x LD_LIBRARY_PATH /home/jonalm/android/Sdk/emulator/lib64 $LD_LIBRARY_PATH
# set -x LD_LIBRARY_PATH /home/jonalm/android/Sdk/emulator/lib64/qt/lib $LD_LIBRARY_PATH

### KEYBINDINGS ###
# function fish_user_key_bindings
# end

### PROGRAMS ON TERMINAL STARTUP ###
nitch

### FUNCTIONS ###
function code
    if test "$argv" = "."
        command code . | qtile cmd-obj -o group v -f toscreen
    else
        command code $argv
    end
end

### ALIAS ###
#alias code .='code . | qtile cmd-obj -o group 3 -f toscreen'
#alias .='cd ..'
alias l='ls -l'
alias ll="lsd"
alias p='sudo pacman'
alias pac='pacman -R $(pacman -Qtdq)'
alias rt='systemctl reboot'
alias sd='systemctl poweroff'
alias hb='systemctl hibernate'
alias rm='sudo rm -r'
alias nnn='nnn -d -e -H -r'
alias gg='git status'
alias xt='Xephyr -br -ac -noreset -screen 1440x900 :1 &'
alias x='XephDISPLAY=:1 qtile'
alias n='nvim'

alias intel="intellij-idea-ultimate-edition &"
alias update-grub="grub-mkconfig -o /boot/grub/grub.cfg"
