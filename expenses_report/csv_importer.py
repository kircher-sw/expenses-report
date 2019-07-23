import csv
import os
import re

from expenses_report import config
from expenses_report import util
from expenses_report.transaction import Transaction


class CsvImporter(object):

    def __init__(self):
        self.unique_transactions = set()
        self.transactions = list()

    def import_csv_files(self):
        file_names = [fn for fn in os.listdir(config.CSV_FILES_PATH) if fn.lower().endswith('.csv')]
        for file in file_names:
            self.import_from_csv_file(os.path.join(config.CSV_FILES_PATH, file))

    def import_from_csv_file(self, filename):
        with open(filename, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';')
            column_indices = None
            for row in csv_reader:
                if not column_indices: # first row with column names
                    if len(row) >= len(config.import_mapping.keys()):
                        column_indices = self.build_column_mapping(row)
                else:
                    ta = self.build_transaction(column_indices, row)
                    if ta.is_valid():
                        self.unique_transactions.add(ta)

        self.transactions = list(self.unique_transactions)
        self.transactions.sort(key=lambda ta: ta.date)

    @staticmethod
    def build_column_mapping(header_row):
        column_map = dict()
        import_mapping = config.import_mapping
        for col in import_mapping.keys():
            for header in import_mapping[col]:
                if header in header_row:
                    column_map[col] = header_row.index(header)
                    break
        return column_map

    @staticmethod
    def build_transaction(column_indices, row):
        ta = Transaction()
        account_raw = row[column_indices[config.ACCOUNT_NO_COL]].strip()
        ta.account_no = account_raw.rjust(10, '0') # fill up with 0s to length of IBAN
        ta.date = util.parse_date(row[column_indices[config.DATE_COL]])
        ta.amount = float(row[column_indices[config.AMOUNT_COL]].replace('.', '').replace(',', '.'))
        ta.payment_reason = re.sub(r'  +', ' ', row[column_indices[config.PAYMENT_REASON_COL]].strip())
        ta.recipient = re.sub(r'  +', ' ', row[column_indices[config.RECIPIENT_COL]].strip())
        return ta

