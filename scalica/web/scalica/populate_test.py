import sys
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils import timezone
from micro.models import Following
import random

User = get_user_model()

user_nameL = "L"
user_nameR = "R"
password = "pass"

i = 0
while (i < 6):
    if (i % 2 == 0):
        gen_string = user_nameL + str(i)
        temp_user = User.objects.create_user(username=gen_string)
        temp_user.set_password(password)
        temp_user.save()
        assert authenticate(username=gen_string, password=password)
    if (i % 2 != 0):
        gen_string = user_nameR + str(i)
        temp_user = User.objects.create_user(username=gen_string)
        temp_user.set_password(password)
        temp_user.save()
        assert authenticate(username=gen_string, password=password)
    i += 1

k = 3
user_array = User.objects.all()

while (k < 6):
    follower_user = user_array[k]
    followee_user = user_array[k - 2]
    newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
    newFollow.save()
    k += 1
