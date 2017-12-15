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

TOTAL_USERS = 20
MAX_FOLLOWERS = 3

i = 0
while (i < TOTAL_USERS):
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


user_array = User.objects.all()

k = 0
while (k < TOTAL_USERS):
    follower_user = user_array[k]

    j = 1
    duplicate_list = []
    duplicate_list.append(k)

    while (j < MAX_FOLLOWERS):
        # This allows users to only follow users of the same EVEN/ODD type
        next_index = random.randint(0,(TOTAL_USERS)


        if (next_index in duplicate_list == False and (next_index % 2) == (k % 2)):
            duplicate_list.append(i)
            followee_user = user_array[next_index]
            newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
            newFollow.save()
        j += 1
    k += 1

# HERE WE ADD THE LONE USER W, if we do things correctly, he should live on his own with no followers.
final_user = "RUSH_SUCKS"
temp_user = User.objects.create_user(username=final_user)
temp_user.set_password(password)
temp_user.save()
assert authenticate(username=final_user, password=password)
