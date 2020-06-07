import argparse
import re

from expenses_report.config import config


class ArgumentParser(object):

    def configure_script(self, args_string=None):
        args = self._read_commandline_arguments(args_string)
        self._update_configuration(args)

    def _read_commandline_arguments(self, args_string):
        parser = argparse.ArgumentParser()
        string_type = '<STRING>'
        parser.add_argument('--input', metavar=string_type, help='Input directory containing CSV files')
        parser.add_argument('--output', metavar=string_type, help='Output filename')

        parser.add_argument('--csv_account_col', metavar=string_type, help='CSV column name for account number')
        parser.add_argument('--csv_date_col', metavar=string_type, help='CSV column name for the transaction date')
        parser.add_argument('--csv_amount_col', metavar=string_type, help='CSV column name for transaction amount')
        parser.add_argument('--csv_reason_col', metavar=string_type, help='CSV column name for payment reason of transaction ')
        parser.add_argument('--csv_recipient_col', metavar=string_type, help='CSV column name for transaction recipient')

        parser.add_argument('--income_category', metavar=string_type, help='Category name for income')
        parser.add_argument('--gain_category', metavar=string_type, help='Category name for gain')
        parser.add_argument('--misc_category', metavar=string_type, help='Category name for all uncategorized transactions')
        parser.add_argument('--category', action='append', metavar='<STRING>:<STRING>[,<STRING>]', help='Self defined category followed by a comma separated list of keywords')

        args = parser.parse_args(args_string)
        return args


    def _update_configuration(self, args):
        if args.input:
            config.CSV_FILES_PATH = args.input
            print(f'set input dir to "{config.CSV_FILES_PATH}"')
        if args.output:
            config.OUT_FILE = args.output
            print(f'set output file to "{config.OUT_FILE}"')

        if args.csv_account_col:
            config.import_mapping[config.ACCOUNT_NO_COL] = [args.csv_account_col]
            print(f'set CSV account number column to "{args.csv_account_col}"')
        if args.csv_date_col:
            config.import_mapping[config.DATE_COL] = [args.csv_date_col]
            print(f'set CSV date column to "{args.csv_date_col}"')
        if args.csv_amount_col:
            config.import_mapping[config.AMOUNT_COL] = [args.csv_amount_col]
            print(f'set CSV amount column to "{args.csv_amount_col}"')
        if args.csv_reason_col:
            config.import_mapping[config.PAYMENT_REASON_COL] = [args.csv_reason_col]
            print(f'set CSV payment reason column to "{args.csv_reason_col}"')
        if args.csv_recipient_col:
            config.import_mapping[config.RECIPIENT_COL] = [args.csv_recipient_col]
            print(f'set CSV recipient column to "{args.csv_recipient_col}"')

        new_categories = None
        if args.income_category:
            del config.categories[config.INCOME_CATEGORY]
            config.INCOME_CATEGORY = args.income_category
            new_categories = config.categories.copy()
            print(f'set income category to "{config.INCOME_CATEGORY}"')
        if args.misc_category:
            del config.categories[config.MISC_CATEGORY]
            config.MISC_CATEGORY = args.misc_category
            new_categories = config.categories.copy()
            print(f'set misc category to "{config.MISC_CATEGORY}"')
        if args.category:
            new_categories = self._parse_categories(args.category)
            print(f'set categories to "{config.categories}"')

        if new_categories:
            self._rebuild_categories_config(new_categories)

    def _parse_categories(self, categories):
        new_categories = dict()
        for category in categories:
            category_name, keywords = self._parse_category(category)
            if category_name:
                new_categories[category_name] = keywords
        return new_categories

    def _parse_category(self, category):
        category_name = None
        keywords = []

        category_regex = re.compile(r'(.*?):(.*)')
        category_matches = category_regex.search(category)
        if category_matches:
            category_name = category_matches.group(1).strip()
            keywords_raw = category_matches.group(2).split(',')
            keywords = list(map(lambda k: k.strip(), keywords_raw))

        return category_name, keywords


    def _rebuild_categories_config(self, new_categories):
        config.categories.clear()
        config.categories[config.INCOME_CATEGORY] = None
        config.categories = {**config.categories, **new_categories}
        config.categories[config.MISC_CATEGORY] = None
