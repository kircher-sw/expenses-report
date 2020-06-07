import unittest
from datetime import datetime

from expenses_report.config import config
from expenses_report.preprocessing.transaction import Transaction
from expenses_report.transaction_preprocessor import TransactionPreprocessor


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
        processor = TransactionPreprocessor()
        transactions = [
            Transaction('123456', datetime(year=2019, month=3, day=5), 20.0, 'reason', 'recipient', config.INCOME_CATEGORY),
            Transaction('123456', datetime(year=2019, month=3, day=18), 50.0, 'reason', 'recipient', config.INCOME_CATEGORY),
            Transaction('123456', datetime(year=2019, month=5, day=8), 100.0, 'reason', 'recipient', config.INCOME_CATEGORY),
        ]
        processor.set_transactions(transactions)

        x_axis, values_all_categories = processor.aggregate_transactions_by_category('M')

        self.assertEqual(3, len(x_axis))
        self.assertEqual(2, len(values_all_categories.keys()))
        self.assertListEqual([70.0, 0.0, 100.0], list(values_all_categories[config.INCOME_CATEGORY]))


    def test_aggregate_different_expenses_by_month(self):
        processor = TransactionPreprocessor()
        transactions = [
            Transaction('123456', datetime(year=2019, month=3, day=5), -20.0, 'reason', 'recipient', self.category1),
            Transaction('123456', datetime(year=2019, month=3, day=18), -50.0, 'reason', 'recipient', self.category2),
            Transaction('123456', datetime(year=2019, month=4, day=15), -30.0, 'reason', 'recipient', self.category1),
            Transaction('123456', datetime(year=2019, month=6, day=5), -100.0, 'reason', 'recipient', self.category2),
            Transaction('123456', datetime(year=2019, month=6, day=21), -150.0, 'reason', 'recipient', self.category2),
        ]
        processor.set_transactions(transactions)

        x_axis, values_all_categories = processor.aggregate_transactions_by_category('M')

        self.assertEqual(4, len(x_axis))
        self.assertEqual(4, len(values_all_categories.keys()))
        self.assertListEqual([20.0, 30.0, 0.0, 0.0], list(values_all_categories[self.category1]))
        self.assertListEqual([50.0, 0.0, 0.0, 250.0], list(values_all_categories[self.category2]))


    def test_aggregate_transactions_by_year(self):
        processor = TransactionPreprocessor()
        transactions = [
            Transaction('123456', datetime(year=2018, month=3, day=5), 120.0, 'reason', 'recipient', config.INCOME_CATEGORY),
            Transaction('123456', datetime(year=2018, month=5, day=18), -50.0, 'reason', 'recipient', self.category1),
            Transaction('123456', datetime(year=2018, month=8, day=15), -30.0, 'reason', 'recipient', self.category1),
            Transaction('123456', datetime(year=2018, month=9, day=3), -100.0, 'reason', 'recipient', self.category2),
            Transaction('123456', datetime(year=2019, month=6, day=21), -150.0, 'reason', 'recipient', self.category2),
        ]
        processor.set_transactions(transactions)

        x_axis, values_all_categories = processor.aggregate_transactions_by_category('Y')

        self.assertEqual(2, len(x_axis))
        self.assertEqual(4, len(values_all_categories.keys())) # includes income category
        self.assertListEqual([120.0, 0.0], list(values_all_categories[config.INCOME_CATEGORY]))
        self.assertListEqual([80.0, 0.0], list(values_all_categories[self.category1]))
        self.assertListEqual([100.0, 150.0], list(values_all_categories[self.category2]))


    def test_aggregate_expenses_by_year_with_total(self):
        processor = TransactionPreprocessor()
        transactions = [
            Transaction('123456', datetime(year=2018, month=3, day=5), 120.0, 'reason', 'recipient', config.INCOME_CATEGORY),
            Transaction('123456', datetime(year=2018, month=5, day=18), -50.0, 'reason', 'recipient', self.category1),
            Transaction('123456', datetime(year=2018, month=8, day=15), -30.0, 'reason', 'recipient', self.category1),
            Transaction('123456', datetime(year=2018, month=9, day=3), -100.0, 'reason', 'recipient', self.category2),
            Transaction('123456', datetime(year=2019, month=6, day=21), -150.0, 'reason', 'recipient', self.category2),
        ]
        processor.set_transactions(transactions)

        result = processor.aggregate_expenses_by_year()

        self.assertEqual(2, len(result.keys()))

        self.assertEqual(180.0, result[2018][0])
        self.assertListEqual([self.category1, self.category2], result[2018][1])
        self.assertListEqual([80.0, 100], result[2018][2])

        self.assertEqual(150.0, result[2019][0])
        self.assertListEqual([self.category2], result[2019][1])
        self.assertListEqual([150], result[2019][2])


    def test_accumulate_transactions_by_category(self):
        processor = TransactionPreprocessor()
        transactions = [
            Transaction('123456', datetime(year=2019, month=3, day=5), 120.0, 'reason', 'recipient', config.INCOME_CATEGORY),
            Transaction('123456', datetime(year=2019, month=3, day=5), -50.0, 'reason', 'recipient', self.category1),
            Transaction('123456', datetime(year=2019, month=3, day=6), -30.0, 'reason', 'recipient', self.category1),
            Transaction('123456', datetime(year=2019, month=3, day=7), -100.0, 'reason', 'recipient', self.category2),
            Transaction('123456', datetime(year=2019, month=3, day=8), 200.0, 'reason', 'recipient', config.INCOME_CATEGORY),
            Transaction('123456', datetime(year=2019, month=3, day=9), -100.0, 'reason', 'recipient', self.category2),
        ]
        processor.set_transactions(transactions)

        x_axis, cumulative_categories = processor.accumulate_categories()

        self.assertEqual(5, len(x_axis))
        self.assertEqual(3, len(cumulative_categories.keys()))
        self.assertListEqual([120.0, 120.0, 120.0, 320.0, 320.0], list(cumulative_categories[config.INCOME_CATEGORY]))
        self.assertListEqual([50.0, 80.0, 80.0, 80.0, 80.0], list(cumulative_categories[self.category1]))
        self.assertListEqual([0.0, 0.0, 100.0, 100.0, 200.0], list(cumulative_categories[self.category2]))

    def test_preprocess_expenses_by_category(self):
        processor = TransactionPreprocessor()
        transactions = [
            Transaction('123456', datetime(year=2019, month=3, day=5), 120.0, 'reason', 'recipient', config.INCOME_CATEGORY),
            Transaction('123456', datetime(year=2019, month=3, day=5), -50.0, 'reason', 'recipient', self.category1),
            Transaction('123456', datetime(year=2019, month=3, day=6), -30.0, 'reason', 'recipient', self.category1),
            Transaction('123456', datetime(year=2019, month=3, day=7), -100.0, 'reason', 'recipient', self.category2),
            Transaction('123456', datetime(year=2019, month=3, day=8), 200.0, 'reason', 'recipient', config.INCOME_CATEGORY),
            Transaction('123456', datetime(year=2019, month=3, day=9), -100.0, 'reason', 'recipient', self.category2),
        ]
        processor.set_transactions(transactions)

        result = processor.preprocess_by_category()
        self.assertEqual(3, len(result.keys()))

        xaxis_in, values_in, ratios_in, labels_in = result[config.INCOME_CATEGORY]
        self.assertEqual(2, len(xaxis_in))
        self.assertListEqual([120.0, 200.0], list(values_in))
        self.assertListEqual([120.0 / 320.0, 200.0 / 320.0], list(ratios_in))

        xaxis1, values1, ratios1, labels1 = result[self.category1]
        self.assertEqual(2, len(xaxis1))
        self.assertListEqual([50.0, 30.0], list(values1))
        self.assertListEqual([50.0 / 80.0, 30.0 / 80.0], list(ratios1))

        xaxis2, values2, ratios2, labels2 = result[self.category2]
        self.assertEqual(2, len(xaxis2))
        self.assertListEqual([100.0, 100.0], list(values2))
        self.assertListEqual([100.0 / 200.0, 100.0 / 200.0], list(ratios2))


if __name__ == '__main__':
    unittest.main()
