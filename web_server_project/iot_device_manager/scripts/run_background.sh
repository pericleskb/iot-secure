#!/bin/bash

source ../iot-server-venv/bin/activate

read -s -p "Enter private key encryption password: " password
echo ""
# Run the rest of the script in the background
(
    python ../main.py $password > /dev/null &
) & disown

