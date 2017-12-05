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

newusername = 'Alex_Lifeson'
users.append((newusername,'pass'))
for i in range(15):
	newusername = 'phish_fan' + str(i)
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
follower_str = "live_demo"
for i in range(3):
	followee_str = "phish_fan" + str(i)
	follower_arr.append(follower_str)
	followee_arr.append(followee_str)

follower_str = "phish_fan1"
for i in range(4,7):
	followee_str = "phish_fan" + str(i)
	follower_arr.append(follower_str)
	followee_arr.append(followee_str)



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


