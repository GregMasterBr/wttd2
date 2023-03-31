#!/usr/bin/env bash

set -o errexit  # exit on error
python -m pip install --upgrade pip
python manage.py collectstatic --no-input
python manage.py migrate
