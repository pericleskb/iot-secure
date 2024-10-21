if ! [ -f ~/ssl/certificates.conf ]; then
  mkdir ~/ssl/
  touch ~/ssl/certificates.conf
  printf "#ca_certs=path_to_authority_certificate\n#certfile=path_to_device_certificate\n#keyfile=path_to_device_key" >> ~/ssl/certificates.conf
esle
  echo "Configuration file already exists. Skip."
fi