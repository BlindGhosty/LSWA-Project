# before running, make sure you're in the virtual environment
# to populate scalica, run: ./manage.py shell < scalica_populate.py

import sys
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils import timezone
from micro.models import Following
import random


User = get_user_model()

users = []

for i in range(30):
	newusername = 'seed' + str(i)
	users.append((newusername,'pass'))

for username, password in users:
	try:
		print 'Create user {0}.'.format(username)
		user = User.objects.create_user(username=username)
		user.set_password(password)
		user.save()

		assert authenticate(username=username,password=password)
		print 'User {0} successfully created.'.format(username)
	except:
		print 'There was a problem creating the user: {0}. Error:{1}.'.format(username, sys.exc_info()[1])

print 'Finished populating user list'


follower_arr = []
followee_arr = []
followee_str = ""
follower_str = ""
for i in range(6):
	follower_str = "seed" + str(random.randint(0,29))
	while follower_str in follower_arr:
		follower_str = "seed" + str(random.randint(0,29))
	followee_str = "seed" + str(random.randint(0,29))
	while followee_str in followee_arr or followee_str in follower_arr:
		followee_str = "seed" + str(random.randint(0,29))
	follower_arr.append(follower_str)
	followee_arr.append(followee_str)


follower_str = "seed" + str(random.randint(0,29))
followee_str = "seed" + str(random.randint(0,29))

follower_arr.append(follower_str)
followee_arr.append(followee_str)
follower_arr.append(followee_str)
followee_arr.append(follower_str)

follower_str = "seed" + str(random.randint(0,29))
for i in range(5):
	followee_str = "seed" + str(random.randint(0,29))
	while followee_str in followee_arr:
		followee_str = "seed" + str(random.randint(0,29))
	follower_arr.append(follower_str)
	followee_arr.append(followee_str)
	follower_str = followee_str

followee_str = "seed" + str(random.randint(0,29))
followerer_str = "seed" + str(random.randint(0,29))
for i in range(4):
	while follower_str in follower_arr:
		follower_str = "seed" + str(random.randint(0,29))
	followee_arr.append(followee_str)
	follower_arr.append(follower_str)
	followee_arr.append(follower_str)
	follower_arr.append(followerer_str)


print "This is the follow list"
for i in range(0, len(follower_arr)):
	for usern in User.objects.all():
		if usern.get_username() == follower_arr[i]:
			follower_user = usern
		if usern.get_username() == followee_arr[i]:
			followee_user = usern
	followdouble = Following(follower=follower_user, followee=followee_user, follow_date=timezone.now())
	followdouble.save()

for follow in Following.objects.all():
	print follow.__str__()


