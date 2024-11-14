#!/bin/bash

source ../iot-server-venv/bin/activate

read -p "Enter private key encryption password: " password

python ../main.py $password
