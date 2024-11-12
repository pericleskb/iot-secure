#!/bin/bash

source ../iot-device-venv/bin/activate

read -p "Enter device name: " name

python ../main.py $name
