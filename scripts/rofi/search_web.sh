#!/bin/bash

BROWSER="brave"

declare -a options=(
"Youtube Search - https://www.youtube.com/results?search_query="
"ChatGPT - https://chat.openai.com/chat"
"Reddit - https://www.reddit.com/"
"Lisam - https://liuonline.sharepoint.com/sites/Lisam/SitePages/en/Home.aspx?wa=wsignin1.0"
"Teams - https://teams.microsoft.com/_#/school/conversations/General?threadId=19:d4vPu4k5Qrc3XefO-oW3J1y_RHCgS6JDw55eMEa4vlQ1@thread.tacv2&ctx=channel"
"PaperCut - https://portalliu.onricoh.se/app;jsessionid=node0xwrsf7jt0kj7h8epw02jnm2u4622.node0?service=page/UserSummary"
"Github - https://github.com/Tardz?tab=repositories"
"Liu Gitlab - https://gitlab.liu.se/"
)

display_options=$(printf '%s\n' "${options[@]}" | cut -d'-' -f1-1)

while [ -z "$engine" ]; do
    displayname=$(printf '%s\n' "${display_options[@]}" | rofi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-7'.rasi -dmenu -i -l 6 -p '') || exit
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

