#!/bin/bash

python -m venv ../iot-server-venv
../iot-server-venv/bin/pip install paho-mqtt
../iot-server-venv/bin/pip install mysql-connector-python
