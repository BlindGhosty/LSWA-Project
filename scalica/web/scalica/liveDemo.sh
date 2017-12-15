#!/bin/bash

python manage.py flush --no-input
./manage.py shell < populate_test_$1.py
