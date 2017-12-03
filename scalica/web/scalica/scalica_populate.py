# before running, make sure you're in the virtual environment
# to populate scalica, run: ./manage.py shell < scalica_populate.py

import sys
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


User = get_user_model()

users = [
	('b1','1'),
	('b2','1'),
	('b3','1'),
	('b4','1'),
	('b5','1'),
	('b6','1'),
	('b7','1'),
	('b8','1'),
	('b9','1'),
	('b10','1'),
	('b11','1'),
	('b12','1'),
	('b13','1'),
	('b14','1'),
	('b15','1'),
	('b16','1'),
	('b17','1'),
	('b18','1'),
	('b19','1'),
	('b20','1'),
	('b21','1'),
	('b22','1'),
	('b23','1'),
	('b24','1'),
	('b25','1'),
]

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


