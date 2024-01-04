#!/bin/sh
group_name=$(qtile-cmd -o cmd -f 'print(self.current_group.name)')
windows=$(xdotool search --onlyvisible --class "qtile-$group_name")
for win_id in $windows; do
    win_title=$(xdotool getwindowname $win_id)
    echo $win_title
done