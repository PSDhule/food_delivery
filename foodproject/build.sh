#!/usr/bin/env bash

pip install -r requirements.txt
python manage.py collectstatic --noinput
cp -r media staticfiles/media
python manage.py migrate