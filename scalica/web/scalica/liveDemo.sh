#!/bin/bash

echo "...Flushing..."
python manage.py flush --no-input
echo "...Populating..."
./manage.py shell < populate_test_$1.py
echo "...Done..."
