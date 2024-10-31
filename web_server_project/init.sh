#!/bin/bash
# entrypoint.sh

# Exit the script if any command fails
set -e

#run initial db population
python manage.py populate_db

# Run database migrations
python manage.py makemigrations web_server
python manage.py migrate

# Start the Django application
exec python manage.py runserver 0.0.0.0:8000
