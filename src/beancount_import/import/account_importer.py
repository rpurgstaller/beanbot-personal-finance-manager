import json
import sqlite3
from pathlib import Path
from dateutil.parser import parse as parse_date

from beancount.ingest import importer
from beancount.core import data
from model.account import Account

import database as db


class AccountImport():
    def __init__(self) -> None:
        super().__init__()

    def extract(self, file):
        directives = []

        accounts = Account.get_all()

        for account in accounts:
            open_directive = data.Open(
                meta = data.new_metadata(file.name, account.id), 
                date = account.created_on.date(),
                account = f'{account.account_type}:{account.name}',
                currencies = [account.currency],
                booking = data.Booking.NONE
            )
            directives.append(open_directive)
            
        return directives
