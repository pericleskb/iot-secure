#!/bin/bash
# entrypoint.sh

# Exit the script if any command fails
set -e

# Run database migrations
python manage.py makemigrations web_server
python manage.py migrate

#python iot_server/mqtt/measurementsSubscriber.py &

# Start the Django application
exec python manage.py runserver 0.0.0.0:8000
