#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect Static Files (CSS)
python manage.py collectstatic --no-input

# Run Migrations (This will create tables in TiDB!)
python manage.py migrate