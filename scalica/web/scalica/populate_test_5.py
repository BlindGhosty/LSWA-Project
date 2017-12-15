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

user_name = "ZPRIME"
temp_user = User.objects.create_user(username=user_name)
temp_user.set_password(password)
temp_user.save()
assert authenticate(username=user_name, password=password)

user_name = "Bubble0"
temp_user = User.objects.create_user(username=user_name)
temp_user.set_password(password)
temp_user.save()
assert authenticate(username=user_name, password=password)

user_name = "Bubble1"
temp_user = User.objects.create_user(username=user_name)
temp_user.set_password(password)
temp_user.save()
assert authenticate(username=user_name, password=password)

user_name = "Bubble2"
temp_user = User.objects.create_user(username=user_name)
temp_user.set_password(password)
temp_user.save()
assert authenticate(username=user_name, password=password)

user_name = "Bubble3"
temp_user = User.objects.create_user(username=user_name)
temp_user.set_password(password)
temp_user.save()
assert authenticate(username=user_name, password=password)

user_name = "FollowForFollow0"
temp_user = User.objects.create_user(username=user_name)
temp_user.set_password(password)
temp_user.save()
assert authenticate(username=user_name, password=password)

user_name = "FollowForFollow1"
temp_user = User.objects.create_user(username=user_name)
temp_user.set_password(password)
temp_user.save()
assert authenticate(username=user_name, password=password)

user_name = "FollowForFollow2"
temp_user = User.objects.create_user(username=user_name)
temp_user.set_password(password)
temp_user.save()
assert authenticate(username=user_name, password=password)

user_array = User.objects.all()

# A -> B

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

# Z -> C

follower_user = user_array[5]
followee_user = user_array[2]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()

# Z -> D

follower_user = user_array[5]
followee_user = user_array[3]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()

# Bubble0 -> Bubble1

follower_user = user_array[6]
followee_user = user_array[7]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()

# Bubble0 -> Bubble2

follower_user = user_array[6]
followee_user = user_array[8]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()

# Bubble1 -> Bubble2

follower_user = user_array[7]
followee_user = user_array[8]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()

# Bubble2 -> Bubble1

follower_user = user_array[8]
followee_user = user_array[7]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()

# Follower0 -> Yair

follower_user = user_array[9]
followee_user = user_array[0]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()

# Follower1 -> Yair

follower_user = user_array[10]
followee_user = user_array[0]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()

# Follower2 -> Yair

follower_user = user_array[11]
followee_user = user_array[0]

newFollow = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
newFollow.save()
