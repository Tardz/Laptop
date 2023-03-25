#!/bin/bash

BROWSER="brave"

declare -a options=(
"Youtube Search - https://www.youtube.com/results?search_query="
"ChatGPT - https://chat.openai.com/chat"
"Reddit - https://www.reddit.com/"
)

display_options=$(printf '%s\n' "${options[@]}" | cut -d'-' -f1-1)

while [ -z "$engine" ]; do
    displayname=$(printf '%s\n' "${display_options[@]}" | rofi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-7'.rasi -dmenu -i -l 3 -p '') || exit
    engine=$(echo "$options" | cut -d' ' -f1-1)
done

for option in "${options[@]}"; do
    option_formated=$(echo "$option" | cut -d'-' -f1-1)
    if [[ "$displayname" == "$option_formated" ]]; then
        url=$(echo "$option" | cut -d'-' -f2- )
        search=$(echo "$option" | cut -d' ' -f2)
        if [[ "$search" == "Search" ]]; then
            while [ -z "$query" ]; do
                query=$(rofi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-7-search'.rasi -dmenu -i -l 2 -p '') || exit
            done
            qtile cmd-obj -o group 2 -f toscreen
            $BROWSER "$url""$query"
            exit 1
        fi
    fi
done

qtile cmd-obj -o group 2 -f toscreen
$BROWSER "$url"
exit 1

