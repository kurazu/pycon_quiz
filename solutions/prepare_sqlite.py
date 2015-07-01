import sys
import hashlib
import base64
import os
import random
import datetime

USERS = [
	('john', 'John', 'Snow', 'bastard@example.com', 'bastard'),
	('arya', 'Arya', 'Stark', 'arry@example.com', 'runaway'),
	('joffrey', 'Joffrey', 'Lannister', 'joff@example.com', 'asshole'),
	('tyrion', 'Tyrion', 'Lannister', 'tyrion@example.com', 'dwarf'),
	('brienne', 'Brienne', 'of Tarth', 'brienne@example.com', 'maid'),
	('gregor', 'Gregor', 'Clegane', 'gregor@example.com', 'force'),
	('admin', 'Mance', 'Ryder', 'kingbeyondthewall@example.com', 'inheritor')
]

DATE_FMT = '%Y-%m-%d %H:%M:%S'

def get_random_date(year):
	month = random.randint(1, 9)
	day = random.randint(1, 28)
	hour = random.randint(0, 23)
	minute = random.randint(0, 59)
	second = random.randint(0, 59)
	date = datetime.datetime(year, month, day, hour, minute, second)
	return date.strftime(DATE_FMT)

def get_password(passwd):
	salt = base64.b64encode(os.urandom(4))[:5]
	sum = hashlib.sha1(salt + passwd).hexdigest()
	return u'sha1${0}${1}'.format(salt, sum)

for username, first_name, last_name, email, password in USERS:
	last_login = get_random_date(2013)
	date_joined = get_random_date(2012)
	password = get_password(password)
	is_admin = 'TRUE' if username == 'admin' else 'FALSE'
	print u'INSERT INTO auth_user VALUES ({0!r}, {1!r}, {2!r}, {3!r}, {4!r}, {5}, TRUE, {5}, {6!r}, {7!r});'.format(
		username, first_name, last_name, email, password, is_admin, last_login, date_joined)
