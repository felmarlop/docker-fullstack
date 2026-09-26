#!/bin/sh

set -e

# Validate runtime environment
if [ -z "$ENVIRONMENT" ]; then
    echo "ENVIRONMENT is not defined."
    exit 1
fi

if [ "$SKIP_INITIALIZATION" != "true" ]; then
    if [ "$ENVIRONMENT" = "dev" ] || [ "$ENVIRONMENT" = "prod" ]; then
        echo "Running database migrations..."
        python manage.py migrate --noinput

        echo "Setting up periodic tasks..."
        python manage.py setup_periodic_tasks

        echo "Collecting static files..."
        python manage.py collectstatic --noinput
    fi
fi

echo "Starting server..."
exec "$@"
