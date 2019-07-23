import unittest
import datetime

from expenses_report import config
from expenses_report.category_finder import CategoryFinder
from expenses_report.transaction import Transaction


class TestCategoryFinder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.categories.clear()
        config.categories[config.INCOME_CATEGORY] = None
        config.categories['Car'] = ['Aral', 'Fuel']
        config.categories[config.MISC_CATEGORY] = None

    def test_transaction_with_positive_amount_expect_income_category(self):
        ta = Transaction('123456', datetime.datetime.now(), 100, 'salary', '', '')
        finder = CategoryFinder()
        finder.assign_category([ta])
        self.assertEqual(config.INCOME_CATEGORY, ta.category)

    def test_transaction_with_payment_reason_expect_car_category(self):
        ta = Transaction('123456', datetime.datetime.now(), -30, 'Fuel', '', '')
        finder = CategoryFinder()
        finder.assign_category([ta])
        self.assertEqual('Car', ta.category)

    def test_transaction_with_recipient_expect_car_category(self):
        ta = Transaction('123456', datetime.datetime.now(), -30, '', 'Aral', '')
        finder = CategoryFinder()
        finder.assign_category([ta])
        self.assertEqual('Car', ta.category)

    def test_transaction_without_matching_keyword_expect_misc_category(self):
        ta = Transaction('123456', datetime.datetime.now(), -40, 'Shoes', 'Amazon', '')
        finder = CategoryFinder()
        finder.assign_category([ta])
        self.assertEqual(config.MISC_CATEGORY, ta.category)


if __name__ == '__main__':
    unittest.main()
