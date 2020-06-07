import unittest

from expenses_report.config import config
from expenses_report.preprocessing.csv_importer import CsvImporter


class TestCsvImport(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.import_mapping[config.DATE_COL] = ['Date']
        config.import_mapping[config.ACCOUNT_NO_COL] = ['Account No']
        config.import_mapping[config.RECIPIENT_COL] = ['Recipient']
        config.import_mapping[config.PAYMENT_REASON_COL] = ['Payment Reason']
        config.import_mapping[config.AMOUNT_COL] = ['Amount']

    def test_build_column_mapping(self):
        header_row = ['Account No', 'Date', 'Amount', 'Payment Reason', 'Recipient']
        csv_reader = CsvImporter()
        column_map = csv_reader.build_column_mapping(header_row)
        self.assertEqual(0, column_map[config.ACCOUNT_NO_COL])
        self.assertEqual(1, column_map[config.DATE_COL])
        self.assertEqual(2, column_map[config.AMOUNT_COL])
        self.assertEqual(3, column_map[config.PAYMENT_REASON_COL])
        self.assertEqual(4, column_map[config.RECIPIENT_COL])

    def test_build_transaction(self):
        column_map = { config.DATE_COL: 0, config.ACCOUNT_NO_COL: 1, config.PAYMENT_REASON_COL: 2, config.RECIPIENT_COL: 3, config.AMOUNT_COL: 4 }
        ta_row = ['01.02.2019', '123456', 'Fuel', 'Aral', '-50']
        csv_reader = CsvImporter()
        ta = csv_reader.build_transaction(column_map, ta_row)
        self.assertEqual(1, ta.date.day)
        self.assertEqual(2, ta.date.month)
        self.assertEqual(2019, ta.date.year)
        self.assertEqual('0000000000000000123456', ta.account_no)
        self.assertEqual('Fuel', ta.payment_reason)
        self.assertEqual('Aral', ta.recipient)
        self.assertEqual(-50.0, ta.amount)

    def test_build_transaction_with_missing_optional_column(self):
        column_map = { config.DATE_COL: 0, config.PAYMENT_REASON_COL: 2, config.RECIPIENT_COL: 3, config.AMOUNT_COL: 4 }
        ta_row = ['01.02.2019', '123456', 'Fuel', 'Aral', '-50']
        csv_reader = CsvImporter()
        ta = csv_reader.build_transaction(column_map, ta_row)
        self.assertEqual(1, ta.date.day)
        self.assertEqual(2, ta.date.month)
        self.assertEqual(2019, ta.date.year)
        self.assertEqual('0000000000000000000000', ta.account_no)
        self.assertEqual('Fuel', ta.payment_reason)
        self.assertEqual('Aral', ta.recipient)
        self.assertEqual(-50.0, ta.amount)


if __name__ == '__main__':
    unittest.main()
