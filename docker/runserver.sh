#!/bin/sh

python manage.py migrate
gunicorn -b 0.0.0.0:80 config.wsgi:application
