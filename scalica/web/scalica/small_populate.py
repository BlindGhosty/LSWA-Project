# before running, make sure you're in the virtual environment
# to populate scalica, run: ./manage.py shell < scalica_populate.py

import sys
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils import timezone
from micro.models import Following
import random


User = get_user_model()

user_a = User.objects.create_user(username="user_a")
user_a.set_password("a")
user_a.save()

assert authenticate(username=username,password=password)

user_b = User.objects.create_user(username="user_b")
user_b.set_password("b")
user_b.save()

assert authenticate(username=username,password=password)

user_array = User.objects.all()

single_follower = Following(follower=user_array[0], followee=user_array[1], follow_date=timezone.now())
single_follower.save()
