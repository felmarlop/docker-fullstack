#!/bin/sh

set -e

# Validate runtime environment
if [ -z "$ENVIRONMENT" ]; then
    echo "ENVIRONMENT is not defined."
    exit 1
fi

if [ "$ENVIRONMENT" = "dev" ] || [ "$ENVIRONMENT" = "prod" ]; then
    echo "Applying database migrations..."
    python manage.py migrate --noinput

    echo "Setting up periodic tasks..."
    python manage.py setup_periodic_tasks
fi

if [ "$ENVIRONMENT" = "dev" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

echo "Starting application..."
exec "$@"
