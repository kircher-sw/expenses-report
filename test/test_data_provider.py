import unittest
from datetime import datetime

from expenses_report.config import config
from expenses_report.preprocessing.data_provider import DataProvider
from expenses_report.preprocessing.transaction import Transaction


class TestCsvImport(unittest.TestCase):

    category1 = 'cat1'
    category2 = 'cat2'


    @classmethod
    def setUpClass(cls):
        config.categories.clear()
        config.categories[config.INCOME_CATEGORY] = None
        config.categories[cls.category1] = []
        config.categories[cls.category2] = []


    def test_aggregate_income_by_month(self):
        transactions = [
            Transaction('123456', datetime(year=2019, month=3, day=5), 20.0, 'reason', 'recipient', config.INCOME_CATEGORY),
            Transaction('123456', datetime(year=2019, month=3, day=18), 50.0, 'reason', 'recipient', config.INCOME_CATEGORY),
            Transaction('123456', datetime(year=2019, month=5, day=8), 100.0, 'reason', 'recipient', config.INCOME_CATEGORY),
        ]
        data_provider = DataProvider.load(transactions)
        df_all = data_provider.get_all_transactions()

        x_axis, category_values = data_provider.aggregate_by_category_as_tuple(df_all, 'MS',
                                                                               config.CATEGORY_MAIN_COL)

        self.assertEqual(3, len(x_axis))
        self.assertEqual(3, len(category_values.keys()))
        self.assertListEqual([70.0, 0.0, 100.0], list(category_values[config.INCOME_CATEGORY]))


    def test_aggregate_different_expenses_by_month(self):
        transactions = [
            Transaction('123456', datetime(year=2019, month=3, day=1), -20.0, 'reason', 'recipient', self.category1),
            Transaction('123456', datetime(year=2019, month=3, day=18), -50.0, 'reason', 'recipient', self.category2),
            Transaction('123456', datetime(year=2019, month=4, day=15), -30.0, 'reason', 'recipient', self.category1),
            Transaction('123456', datetime(year=2019, month=6, day=5), -100.0, 'reason', 'recipient', self.category2),
            Transaction('123456', datetime(year=2019, month=6, day=21), -150.0, 'reason', 'recipient', self.category2),
        ]
        data_provider = DataProvider.load(transactions)
        df_all = data_provider.get_all_transactions()

        x_axis, category_values = data_provider.aggregate_by_category_as_tuple(df_all, 'MS', config.CATEGORY_MAIN_COL)

        self.assertEqual(4, len(x_axis))
        self.assertEqual(3, len(category_values.keys()))
        self.assertListEqual([20.0, 30.0, 0.0, 0.0], list(category_values[self.category1]))
        self.assertListEqual([50.0, 0.0, 0.0, 250.0], list(category_values[self.category2]))


    def test_aggregate_transactions_by_year(self):
        transactions = [
            Transaction('123456', datetime(year=2018, month=3, day=5), 120.0, 'reason', 'recipient', config.INCOME_CATEGORY),
            Transaction('123456', datetime(year=2018, month=5, day=18), -50.0, 'reason', 'recipient', self.category1),
            Transaction('123456', datetime(year=2018, month=8, day=15), -30.0, 'reason', 'recipient', self.category1),
            Transaction('123456', datetime(year=2018, month=9, day=3), -100.0, 'reason', 'recipient', self.category2),
            Transaction('123456', datetime(year=2019, month=6, day=21), -150.0, 'reason', 'recipient', self.category2),
        ]
        data_provider = DataProvider.load(transactions)
        df_all = data_provider.get_all_transactions()

        x_axis, category_values = data_provider.aggregate_by_category_as_tuple(df_all, 'YS', config.CATEGORY_MAIN_COL)

        self.assertEqual(2, len(x_axis))
        self.assertEqual(3, len(category_values.keys())) # includes income category
        self.assertListEqual([120.0, 0.0], list(category_values[config.INCOME_CATEGORY]))
        self.assertListEqual([80.0, 0.0], list(category_values[self.category1]))
        self.assertListEqual([100.0, 150.0], list(category_values[self.category2]))


if __name__ == '__main__':
    unittest.main()
