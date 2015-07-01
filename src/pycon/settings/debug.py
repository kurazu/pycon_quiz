# -*- coding: utf-8 -*-
from pycon.settings.base import *

DEBUG = True
HOST = '0.0.0.0'
PORT = 5000
SQLALCHEMY_DATABASE_URI = 'sqlite:////home/kurazu/workspace/pycon2013/var/riddles.db'
LOGGING_CONFIG_FILE = '/home/kurazu/workspace/pycon2013/src/pycon/settings/logging_debug.cfg'

del SQLALCHEMY_POOL_SIZE
del SQLALCHEMY_POOL_TIMEOUT
del SQLALCHEMY_MAX_OVERFLOW

