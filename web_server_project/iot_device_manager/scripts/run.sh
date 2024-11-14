#!/bin/bash

source ../iot-server-venv/bin/activate

read -s -p "Enter private key encryption password: " password
echo ""
python ../main.py $password
