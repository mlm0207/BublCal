#!/bin/bash

python manage.py makemigrations app
python manage.py makemigrations --dry-run
python manage.py migrate app
python manage.py migrate --run-syncdb