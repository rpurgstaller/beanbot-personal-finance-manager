import os
from data_import.csv_importer import CsvImporter
from database import DbBaseModel, get_session

from model.account import DbAccount
from model.partner import DbPartner
from model.transaction import DbTransaction


class GiroImporter():

    #TODO config file
    CFG_MAPPING_TRANSACTION = {
        "Partnername" : "partner_name",
        "Partner IBAN" : "partner_iban",
        "BIC/SWIFT" : "partner_bic",
        "Partner Kontonummer" : "partner_account_number",
        "Bankleitzahl" : "partner_bank_code",
        "Buchungsdatum": "date",
        "Betrag" : "amount",
        "Währung" : "currency_code",
        "Buchungs-Info": "reference"
    }

    def __init__(self, account_key) -> None:
        super().__init__()
        self.account_key = account_key

    def execute(self, filename : str):
        session = get_session()

        accounts = DbAccount.get_full_account_dict(session)
        
        giro_account = accounts[self.account_key]

        transactions = CsvImporter().execute(filename, DbTransaction.build, GiroImporter.CFG_MAPPING_TRANSACTION)

        for transaction in transactions:
            transaction.account_id = giro_account.id
            # TODO execute rules

        # find partners without account
        unassigned_transactions = [t for t in transactions if t.partner_account_id is None]

        session.add_all(transactions)
        session.commit()