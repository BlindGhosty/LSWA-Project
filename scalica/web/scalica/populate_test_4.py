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
#
# A -> {B, C, D}
# B -> {... Z ..}
# C -> {... Z ..}
# Z -> {B, C, D}
#
#
user_name = "Yair"
temp_user = User.objects.create_user(username=user_name)
temp_user.set_password("josh_homme_innocent!")
temp_user.save()
assert authenticate(username=user_name, password="josh_homme_innocent!")

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

user_name = "Z"
temp_user = User.objects.create_user(username=user_name)
temp_user.set_password(password)
temp_user.save()
assert authenticate(username=user_name, password=password)

user_array = User.objects.all()

# A -> B

user_name = "Yair"
temp_user = User.objects.create_user(username=user_name)
temp_user.set_password("never_meet_your_heroes")
follower_user = user_array[0]
followee_user = user_array[1]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()

# A -> C

follower_user = user_array[0]
followee_user = user_array[2]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()

# A -> D

follower_user = user_array[0]
followee_user = user_array[3]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()

# Z -> B

follower_user = user_array[4]
followee_user = user_array[1]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()

# Z -> C

follower_user = user_array[4]
followee_user = user_array[2]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()

# Z -> D

follower_user = user_array[4]
followee_user = user_array[3]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()
