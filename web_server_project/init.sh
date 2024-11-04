#!/bin/bash
# entrypoint.sh

# Exit the script if any command fails
set -e

# Run database migrations
python manage.py makemigrations web_server
python manage.py migrate

#bash iot_server/scripts/install.sh
#python iot_server/main.py

# Start the Django application
exec python manage.py runserver 0.0.0.0:8000
