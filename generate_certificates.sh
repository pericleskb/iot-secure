#!/bin/bash

# This script is meant to be run on the web server.
# A certificate authority will be generated which will sign the certificates
# of the broker, the iot server and of the iot devices.

python create_default_files.py

read -p "You are about to generate the certificate authority and the certificates needed for your IoT network. [Enter] "
read -p "First the CA needed to sign the certificates will be generated. [Enter] "

read -p "Enter path to store certificates: " path

printf "Certificates will be generated in $path"

mkdir $path

#generate ca and crt and key
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout $path/ca.key -out $path/ca.crt -subj "/CN=raspberrypi.local" -addext "subjectAltName=DNS:raspberrypi.local"

#copy crt & key to eclipse's mosquitto appropriate directory
#we copy because we need to keep ca.key & ca.crt handy to sign client certificates
sudo cp $path/ca.key $path/ca.crt /etc/mosquitto/ca_certificates/

# Check if files copied successfully
if [ $? -eq 0 ]; then
    echo ""
    echo "CA's key and certificate created and copied successfully in /etc/mosquitto/ca_certificates/"
else
    echo ""
    echo "Error generating CA's key and certificate."
    exit 1
fi

echo ""
read -p "Next you need to fill in the details for the certificate of the MQTT broker. [Enter] "

#generate broker keys and certificate
folderpath="${path}/broker/"
mkdir ${folderpath}
openssl ecparam -name prime256v1 -genkey -out $folderpath/broker_private_key.pem
openssl req -new -key $folderpath/broker_private_key.pem -out $folderpath/ecdsa_request.csr
openssl x509 -req -in $folderpath/ecdsa_request.csr -CA $path/ca.crt -CAkey $path/ca.key -CAcreateserial -out $folderpath/broker_certificate.pem -days 365
openssl ec -in $folderpath/broker_private_key.pem -aes256 -out $folderpath/broker_private_key_encrypted.pem

#move broker's encrypted key and certificate to eclipse's mosquitto appropriate directory
sudo mv $folderpath/broker_certificate.pem $folderpath/broker_private_key_encrypted.pem /etc/mosquitto/certs/

#change permissions
sudo chmod 644 /etc/mosquitto/certs/broker_private_key_encrypted.pem

# Check if files moved successfully
if [ $? -eq 0 ]; then
    echo ""
    echo "Broker's key and certificate created and copied successfully in /etc/mosquitto/certs/"
else
    echo ""
    echo "Error generating broker's key and certificate."
    exit 1
fi
rm -r $folderpath

echo ""
read -p "Next you need to fill in the details for the certificates of your IoT server. [Enter] "

#generate iot server's certificate
folderpath="${path}/iot_server/"
mkdir ${folderpath}
openssl ecparam -name prime256v1 -genkey -out "${folderpath}/manager_private_key.pem"
openssl req -new -key "${folderpath}/manager_private_key.pem" -out "${folderpath}/ecdsa_request.csr"
openssl x509 -req -in "${folderpath}/ecdsa_request.csr" -CA $path/ca.crt -CAkey $path/ca.key -CAcreateserial -out "${folderpath}/manager_certificate.pem" -days 365
openssl ec -in "${folderpath}/manager_private_key.pem" -aes256 -out "${folderpath}/manager_private_key_encrypted.pem"
rm ${folderpath}/ecdsa_request.csr $folderpath/manager_private_key.pem

echo ""
read -p "Next you need to fill in the details for the certificates for each of your IoT devices. [Enter] "

echo ""
read -p "Enter number of devices you want to generate certificates for: " number

if [ -z "$number" ]; then
    echo "Please provide the number of devices you want to generate certificates for."
    exit 1
fi

for i in $(seq 1 $number);
do
    filename="iot_device_${i}"
    foldername="${path}/iot_device_${i}"
    mkdir ${foldername}
    #generate device keys and certificate
    openssl ecparam -name prime256v1 -genkey -out "${foldername}/${filename}_private_key.pem"
    openssl req -new -key "${foldername}/${filename}_private_key".pem -out "${foldername}/ecdsa_request.csr"
    openssl x509 -req -in "${foldername}/ecdsa_request.csr" -CA $path/ca.crt -CAkey $path/ca.key -CAcreateserial -out "${foldername}/${filename}_certificate.pem" -days 365
    openssl ec -in "${foldername}/${filename}_private_key.pem" -aes256 -out "${foldername}/${filename}_private_key_encrypted.pem"
    rm $foldername/ecdsa_request.csr $foldername/$filename_private_key.pem
done

rm $path/ca.srl

sudo systemctl stop mosquitto

echo ""
echo "Please set the path of your certificates in iot_secure/certificates.conf in your home directory for your IoT server and devices."

