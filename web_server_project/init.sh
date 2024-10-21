#!/bin/bash
# entrypoint.sh

# Exit the script if any command fails
set -e

# Run database migrations
python manage.py makemigrations web_server
python manage.py migrate

if ! [ -f "$HOME/ssl/certificates.conf" ]; then
  mkdir "$HOME/ssl/"
  touch "$HOME/ssl/certificates.conf"
  printf "#ca_certs=path_to_authority_certificate\n#certfile=path_to_device_certificate\n#keyfile=path_to_device_key" >> "$HOME/ssl/certificates.conf"
fi

python iot_server/mqtt/measurementsSubscriber.py &

# Start the Django application
exec python manage.py runserver 0.0.0.0:8000
