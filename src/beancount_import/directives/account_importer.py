import json
import sqlite3
from pathlib import Path
from dateutil.parser import parse as parse_date

from beancount.core import data
from beancount_import.directives.directive_importer import DirectiveImporter
from model.account import Account


class AccountImporter(DirectiveImporter):
    def __init__(self) -> None:
        super().__init__()

    def extract(self):
        directives = []

        accounts = Account.get_all()

        for account in accounts:
            open_directive = data.Open(
                # TODO add filename 
                meta = data.new_metadata('f', account.id), 
                date = account.created_on.date(),
                account = f'{account.account_type}:{account.name}',
                currencies = [account.currency],
                booking = data.Booking.NONE
            )
            directives.append(open_directive)
            
        return directives
