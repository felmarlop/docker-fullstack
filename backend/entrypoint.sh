#!/bin/sh

set -e

if [ "$RUN_INITIAL_COMMANDS" = "True" ]; then
    echo "Applying database migrations..."
    python manage.py migrate --noinput

    echo "Setting up periodic tasks..."
    python manage.py setup_periodic_tasks
fi

echo "Starting application..."
exec "$@"
