from __future__ import print_function, unicode_literals

import cli.action as action

import database as db
import os, sys, argparse, unittest

from config import config_by_name


parser = argparse.ArgumentParser()

parser.add_argument('--mode')


def main(mode):
    cfg = config_by_name[mode]()

    db.create(cfg.DB_FILENAME)

    if cfg.TEST:
        unittest.main()
    else:
        action.run()

if __name__ == "__main__":
    if not sys.argv[1:]:
        sys.exit(0)
    parsed_args = parser.parse_args(sys.argv[1:])
    main(parsed_args.mode)