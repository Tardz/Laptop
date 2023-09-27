declare -a options=(
'Google drive - https://drive.google.com/drive/home'
'TDDC93 - https://www.ida.liu.se/~TDDC88/index.en.shtml'
'TDDD86 - https://www.ida.liu.se/~TDDD86/index.sv.shtml'
'TDDD85 - https://www.ida.liu.se/~TDDD14/index.en.shtml'
'Ladok - https://www.student.ladok.se/student/app/studentwebb/start'
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

export options