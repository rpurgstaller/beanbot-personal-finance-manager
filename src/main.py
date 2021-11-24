from __future__ import print_function, unicode_literals

import os
from cli.actions import ActionMain

from database import create as create_db, get_session
from model.account import DbAccount

create_db()

ActionMain().execute()