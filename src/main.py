from __future__ import print_function, unicode_literals

import os
from cli.actions.action import ActionMain

import database as db

# create DB 
db.create()

ActionMain().execute()