#!/bin/bash

source ../iot-device-venv/bin/activate

#!/bin/bash

# Define the file path
FILE="name.txt"
device_name=""

# Check if the file exists
if [[ -f "$FILE" ]]; then
    # File exists, read the first line
    first_line=$(head -n 1 "$FILE")

    if [[ -n "$first_line" ]]; then
        # First line is not empty, save it to a variable
        device_name="$first_line"
    else
        # First line is empty, prompt user for a name
        read -p "Enter device name: " name
        echo "$name" > "$FILE"
        device_name="$name"
    fi
else
    # File does not exist, prompt user for a name
    read -p "Enter device name: " name
    read user_name
    echo "$user_name" > "$FILE"
fi
echo ""
python ../main.py "$device_name" "$password"
