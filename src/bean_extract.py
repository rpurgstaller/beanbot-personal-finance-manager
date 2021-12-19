import os, sys

from typing import List

# beancount doesn't run from this directory
sys.path.append(os.path.dirname(__file__))

from util import get_data_files
from database import reset_and_create

#import database as db
import cfg


if len(sys.argv) != 3:
    print('usage: bean-extract src/manage.py DIRECTORY')

# reset db # TODO introduce dev/test/production mode - only reset in dev mode
reset_and_create()

for importer in cfg.get_db_cfg():
    for file in get_data_files(sys.argv[2]):
        if importer.identify(file):
            importer.execute(file)

# beancount config
CONFIG = cfg.get_bean_cfg()
