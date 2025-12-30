#!/bin/bash

# Exit on error
set -e

echo "Starting entrypoint script..."

# Ensure persistent directories exist
mkdir -p /app/db

# Run database migrations (only if pending)
echo "Checking for pending migrations..."
if python manage.py showmigrations --plan | grep -qE '^\s*\[ \]\s'; then
  echo "Pending migrations found. Applying..."
  python manage.py migrate --noinput
else
  echo "No pending migrations."
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Entrypoint script completed successfully!"

# Execute the main command
exec "$@"
