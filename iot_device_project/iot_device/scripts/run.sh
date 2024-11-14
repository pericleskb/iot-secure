#!/bin/bash

source ../iot-device-venv/bin/activate

read -p "Enter device name: " name
read -s -p "Enter private key encryption password: " password
echo ""
python ../main.py $name $password
