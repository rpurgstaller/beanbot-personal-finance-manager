import os
from data_import.csv_importer import CsvImporter
from database import DbBaseModel, get_session

from model.account import DbAccount
from model.partner import DbPartner
from model.transaction import DbTransaction


class GiroImporter():

    ACCOUNT_KEY = os.environ['BEANBOT_GIRO_ACCOUNT']

    CFG_MAPPING_PARTNER = {
        "Partnername" : "partner_name",
        "Partner IBAN" : "partner_iban",
        "BIC/SWIFT" : "partner_bic",
        "Partner Kontonummer" : "partner_account",
        "Bankleitzahl" : "partner_bank_code",
        # required for partner assignment
        "Bucungs-Info": "reference"
    }

    CFG_MAPPING_TRANSACTION = {
        "Buchungsdatum": "date",
        "Betrag" : "amount",
        "Währung" : "currency",
        "Bucungs-Info": "reference"
    }

    def __init__(self) -> None:
        super().__init__()

    def execute(self, filename : str):
        session = get_session()

        accounts = DbAccount.get_full_account_dict(session)
        
        giro_account = accounts[GiroImporter.ACCOUNT_KEY]

        partners = CsvImporter().execute(filename, DbPartner.build_and_assign, GiroImporter.CFG_MAPPING_PARTNER)

        transactions = CsvImporter().execute(filename, DbTransaction.build, GiroImporter.CFG_MAPPING_TRANSACTION)

        for partner, transaction in zip(partners, transactions):
            transaction.partner_id = partner.id
            transaction.account_id = giro_account.id

        # find partners without account
        unassigned_partners = session.query(DbPartner).filter(DbPartner.account_id is None)

        session.add_all(partners + transactions)
        session.commit()