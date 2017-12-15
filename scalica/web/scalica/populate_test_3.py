import sys
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils import timezone
from micro.models import Following
import random

User = get_user_model()

password = "pass"

# A -> B -> C
# A -> D -> E
user_name = "Yair"
temp_user = User.objects.create_user(username=user_name)
temp_user.set_password("josh_homme_INNOCENT!")
temp_user.save()
assert authenticate(username=user_name, password="josh_homme_INNOCENT!")

user_name = "B"
temp_user = User.objects.create_user(username=user_name)
temp_user.set_password(password)
temp_user.save()
assert authenticate(username=user_name, password=password)

user_name = "C"
temp_user = User.objects.create_user(username=user_name)
temp_user.set_password(password)
temp_user.save()
assert authenticate(username=user_name, password=password)

user_name = "D"
temp_user = User.objects.create_user(username=user_name)
temp_user.set_password(password)
temp_user.save()
assert authenticate(username=user_name, password=password)

user_name = "E"
temp_user = User.objects.create_user(username=user_name)
temp_user.set_password(password)
temp_user.save()
assert authenticate(username=user_name, password=password)

# A -> B

user_array = User.objects.all()

follower_user = user_array[0]
followee_user = user_array[1]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()

# B -> C

follower_user = user_array[1]
followee_user = user_array[2]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()

# A -> D

follower_user = user_array[0]
followee_user = user_array[3]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()

# D -> E

follower_user = user_array[3]
followee_user = user_array[4]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()
