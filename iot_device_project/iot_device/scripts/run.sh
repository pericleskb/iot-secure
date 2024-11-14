#!/bin/bash

source ../iot-device-venv/bin/activate

read -p "Enter device name: " name
read -p "Enter private key encryption password: " password

python ../main.py $name $password
