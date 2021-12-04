from __future__ import print_function, unicode_literals

import cli.action as action

import database as db
import sys, argparse

from config import config_by_name


parser = argparse.ArgumentParser()

parser.add_argument('--mode')


def main(mode):
    cfg = config_by_name[mode]()

    db.initialize_db(cfg.DB_FILENAME)

    action.run()

if __name__ == "__main__":
    if not sys.argv[1:]:
        sys.exit(0)
    parsed_args = parser.parse_args(sys.argv[1:])
    main(parsed_args.mode)