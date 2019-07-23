import unittest
from expenses_report import util


class TestCsvImport(unittest.TestCase):

    def test_parse_date_ddmmyy(self):
        datetime = util.parse_date('08.10.16')
        self.assertEqual(8, datetime.day)
        self.assertEqual(10, datetime.month)
        self.assertEqual(2016, datetime.year)

    def test_parse_date_ddmmyyyy(self):
        datetime = util.parse_date('12.07.2019')
        self.assertEqual(12, datetime.day)
        self.assertEqual(7, datetime.month)
        self.assertEqual(2019, datetime.year)

    def test_parse_date_yymmdd(self):
        datetime = util.parse_date('17-03-22')
        self.assertEqual(22, datetime.day)
        self.assertEqual(3, datetime.month)
        self.assertEqual(2017, datetime.year)

    def test_parse_date_yyyymmdd(self):
        datetime = util.parse_date('2015-11-23')
        self.assertEqual(23, datetime.day)
        self.assertEqual(11, datetime.month)
        self.assertEqual(2015, datetime.year)

    def test_parse_date_invalid(self):
        self.assertIsNone(util.parse_date('123.88.20001'))
        self.assertIsNone(util.parse_date('a'))
        self.assertIsNone(util.parse_date('1.1.20'))


if __name__ == '__main__':
    unittest.main()
