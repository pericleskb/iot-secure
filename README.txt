The goal of this project is to create a secure and versatile IoT system
where the user is in control of the security settings of the network.
The project provides the user with a web dashboard where the user can 
control the system's security settings and change them on the fly.

This project consists of the following software modules:
1. Eclipse MQTT Broker
2. Django Web Server
3. MariaDB
4. IoT Server. An MQTT client to manage communication with IoT devices
5. IoT Devices. MQTT clients that collect data and send them to the server.

For now only Debian Linux on RaspberryPis is supported.

The project is setup so that the first 4 elements run on the same machine.
The IoT device code can run on any number of devices.

Follow the instuctions below to set up the project.

## Setting up the server machine. ##

# Prerequisites
1. Install Docker
2. Install Python

# Setting up MQTT Broker
3. To set up the MQTT broker follow only the first part of the installation instructions here https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/.
4. Then replace the contents of /etc/mosquitto/mosquitto.conf with the contents in mosquitto.conf, located at this project's root dir (same dir as this README file).

# Set up server host name
5. Make sure the machine that will act as a server is using avahi mdns and can be located in the local network with the hostname "raspberrypi.local".

# Generate SSL certificates 
6. In order to use SSL with this project you will need to create a Certificate Authority and self sign the certificates of all the devices in your mqtt network.
   This is achieved easily by running the bash script generate_certificates.sh, again located in the project's root directory. Follow any instruction on the command line.
   First you need to fill in a path (absolute or relative) where the certificates generated will be stored.
   First this script will produce the certifacte authority's key and certificate and copy them to the appropriate directory where they can be used by the Eclipse MQTT Broker. 
   For this it will prompt you to fill the details of the Broker's certificate. Make sure to fill in the same details for all certificates that will be produced during this process.
   IMPORTANT: When prompted for the CN (Common Name) please enter "raspberrypi.local".
   IMPORTANT: You will be asked to provide a PEM password. This is the password that will encrypt the private key, so it will be stored securely. 
              Remember this password as you will need to provide it to the program at a later step.
   After the broker's certificates have been produced, the script will copy to the appropriate directory where they can be used by the Eclipse MQTT Broker.
   Then the process of generating certificates will be repeated for the IoT server and IoT devices. Fill in the same details as you did with the MQTT Broker.
   The certificates for the IoT server and devices will reside in the path you specified on the first step of the script.

# Provide certificates for the IoT Server
7. A configuration file has been generated in your home directory at ~/iot_secure/certificates.conf
   In order for the IoT server to locate its certificates you need to provide their path in their configuration file. 
   You can use the path they were generated in or move them elsewhere.
   Also fill in the PEM password you used during the certificate generation process.
    
# Start mosquitto broker from terminal
8. sudo mosquitto -c /etc/mosquitto/mosquitto.conf
    
# Install and run the web server and MariaDB using docker and provide PEM password
9. Go to iot-secure/web_server_project and run "sudo docker compose up --build"

# Install prerequisites for IoT Server
10. Navigate to iot-secure/web_server_project/iot_server/scripts through the command line and execute install.sh located in 

# Run IoT Server
11. Execute run.sh located in the same folder

## Setting up IoT devices ##
For each IoT device that will run on raspberrypi device you need to do the following.

# Installing
1. Copy the code from iot-secure/iot_device_project/iot_device in the machine
2. Copy the device's certificates generated for this specific device, from the server to the device in your selected folder
3. Run the install.sh bash script located in iot-secure/iot_device_project/iot_device/scripts
4. Edit configuratio file in home dir ~/iot_secure/certificates.conf as you did for the IoT Server

# Running
5. Run "bash run.sh" from the scripts directory
