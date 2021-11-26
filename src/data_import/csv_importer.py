import re
import csv
import database as db
from model.account import DbAccount

class CsvImporter(object):
    def __init__(self) -> None:
        super().__init__()

    @db.sessioncommit
    def execute(self, file : str, classToCreate):
        with open(file) as csvDataFile:

            reader = csv.reader(csvDataFile)

            objects = []

            columns = next(reader)

            for row in reader:
                objects.append(classToCreate.build(**{col : row[idx] for idx, col in enumerate(columns)}))

            return objects