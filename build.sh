#!/usr/bin/env bash

# Exit on error
set -e errexit

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput