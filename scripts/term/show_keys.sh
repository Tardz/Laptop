#!/bin/bash

# Read the config file and extract the relevant lines
key_lines=$(sed -n '/KEYS_START/,/KEYS_END/p' ~/.config/qtile/config.py)

# Remove unwanted lines
filtered_key_lines=$(echo "$key_lines" | grep -v "# " | grep -v "#Key" | grep -v "keys" | grep -v "#- " | grep -v "WINDOWS" | grep -v "format")

# Process the lines to extract the desired information
processed_key_lines=$(echo "$filtered_key_lines" |
    sed -e "s/^[ \t]*//" -e "s/^[Key(]*//" |
    sed -e 's/lazy.*desc//' |
    sed -e "s/lazy.layout.down()//" |
    sed -e "s/lazy.layout.up() //" |
    sed -e 's/]\,/] +/' |
    sed -e 's/",.*=/": /' |
    sed -e "s/:.'/: /" |
    sed -e "s/'),//" 
)

# Apply HTML tags for formatting
formatted_lines=$(echo "$processed_key_lines" |
    sed -e 's/"\([^"]*\)"/\<span style="color: #81a1c1;">&\<\/span>/g' |
    sed -e 's/#--\(.*\)--#/\<span style="color: #bf616a; font-size: 14px; font-weight: bold;">\1\<\/span>/' |
    sed -e 's/\bmod\b/\<span style="color: #d08770;">&\<\/span>/g' 
)

# Wrap the formatted lines in <pre> tags to preserve formatting
formatted_text="<h3 style=\"background-color: #383C4A; color: #bf616a; font-weight: bold; text-decoration: underline; padding: 15px 20px;\">
                ⌨️ Keybindings</h3><pre style=\"background-color: #383C4A; color: #ECEFF4; padding: 0px 20px;\">$formatted_lines</pre>"

# Apply CSS styles for customization
css_styles="
<style>
    body {
        background-color: #383C4A;
        color: #ECEFF4;
        margin: 0;
        padding: 0;
    }
    h1 {
        color: #A3BE8C;
        font-size: 18px;
        font-weight: bold;
        margin: 0;
        padding: 10px;
    }
    .content {
        padding: 10px;
    }
</style>
"

# Concatenate the CSS styles and formatted text
formatted_html="${css_styles}${formatted_text}"

# Display the formatted text using yad with HTML support
yad --text-info \
    --title "Keybindings" \
    --html \
    --undecorated \
    --no-headers \
    --no-buttons \
    --geometry=850x890 \
    --gtk3 \
    <<< "$formatted_html"