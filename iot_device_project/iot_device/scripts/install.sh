#!/bin/bash

python ../files/create_default_files.py
python -m venv ../iot-device-venv
../iot-device-venv/bin/pip install paho-mqtt
