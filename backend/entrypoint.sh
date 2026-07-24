#!/bin/sh

set -e

if [ "$RUN_INITIAL_COMMANDS" = "True" ]; then
    echo "Applying database migrations..."
    python manage.py migrate --noinput

    echo "Collecting static files..."
    python manage.py collectstatic --noinput

    echo "Setting up periodic tasks..."
    python manage.py setup_periodic_tasks
fi

echo "Starting application..."
exec "$@"
