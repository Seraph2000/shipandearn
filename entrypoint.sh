#!/bin/sh
set -e
flask db upgrade
exec gunicorn -c gunicorn.conf.py app:app
