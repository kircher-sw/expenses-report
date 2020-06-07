import unittest

from expenses_report.argument_parser import ArgumentParser
from expenses_report.config import config

class TestArgumentParster(unittest.TestCase):

    def test_update_input_dir(self):
        parser = ArgumentParser()
        parser.configure_script(self._build_args('--input /home/test/csv'))
        self.assertEqual('/home/test/csv', config.CSV_FILES_PATH)

    def test_update_date_column(self):
        parser = ArgumentParser()
        parser.configure_script(['--csv_date_col', 'csv date'])
        self.assertListEqual(['csv date'], config.import_mapping[config.DATE_COL])

    def test_update_misc_category_label(self):
        parser = ArgumentParser()
        parser.configure_script(self._build_args('--misc_category other'))
        self.assertEqual('other', config.MISC_CATEGORY)
        self.assertTrue('other' in config.categories)

    def test_define_single_category(self):
        parser = ArgumentParser()
        parser.configure_script(['--category', 'Name: key1, key2, key3'])
        self.assertEqual(4, len(config.categories.keys()))
        self.assertTrue('Name' in config.categories)
        self.assertListEqual(['key1', 'key2', 'key3'], config.categories['Name'])

    def test_define_multiple_categories(self):
        parser = ArgumentParser()
        parser.configure_script(self._build_args('--category Name:key1,key2,key3 --category Test:k1'))
        self.assertEqual(5, len(config.categories.keys()))
        self.assertTrue('Name' in config.categories)
        self.assertTrue('Test' in config.categories)
        self.assertListEqual(['key1', 'key2', 'key3'], config.categories['Name'])
        self.assertListEqual(['k1'], config.categories['Test'])

    def _build_args(self, args_string):
        return args_string.split()
