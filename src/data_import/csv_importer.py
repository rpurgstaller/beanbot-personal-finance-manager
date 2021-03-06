import csv

class CsvImporter(object):
    def __init__(self) -> None:
        super().__init__()

    def execute(self, file : str, builder_func, column_transformation = None):
        with open(file, 'r', newline='', encoding='UTF-16') as csvDataFile:

            reader = csv.reader(csvDataFile)

            objects = []

            columns = next(reader)

            if column_transformation:
                columns = [column_transformation[col] for col in columns if col in column_transformation]

            for row in reader:
                objects.append(builder_func(**{col : row[idx] for idx, col in enumerate(columns)}))

            return objects