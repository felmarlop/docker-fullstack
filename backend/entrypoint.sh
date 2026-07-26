#!/bin/sh

set -e

if [ "$INIT_APP" = "True" ]; then
    echo "Applying database migrations..."
    python manage.py migrate --noinput

    echo "Collecting static files..."
    python manage.py collectstatic --noinput

    echo "Setting up periodic tasks..."
    python manage.py setup_periodic_tasks
fi

echo "Starting application..."
exec "$@"
