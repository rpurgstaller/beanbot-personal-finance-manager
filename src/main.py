from __future__ import print_function, unicode_literals

import cli.action as action

import database as db

# create DB 
db.create()

action.run()
