#!/bin/bash
if ! [ -f /root/ssl/certificates.conf ]; then
  mkdir /root/ssl/
  touch /root/ssl/certificates.conf
  printf "#ca_certs=path_to_authority_certificate\n#certfile=path_to_device_certificate\n#keyfile=path_to_device_key" >> /root/ssl/certificates.conf
else
  echo "Configuration file already exists. Skip."
fi
