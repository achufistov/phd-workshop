#!/bin/bash
set -e

echo "Applying migrations..."
python manage.py makemigrations vulnapp
python manage.py migrate

echo "Creating test users..."
python manage.py create_test_users

echo "Creating initial posts..."
python manage.py create_initial_posts

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000 