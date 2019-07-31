"""
Config for expenses-report
"""


# Path to the csv files from your bank account. All csv files from this path will be read and processed.
CSV_FILES_PATH = 'sample'

OUT_FILE = 'expenses-report.html'


# Csv column identifiers (do not modify)
ACCOUNT_NO_COL = 'accountno'
DATE_COL = 'date'
AMOUNT_COL = 'amount'
PAYMENT_REASON_COL = 'paymentreason'
RECIPIENT_COL = 'recipient'

import_mapping = {
    ACCOUNT_NO_COL: ['Account No', 'Auftragskonto', 'Kontonummer'],
    DATE_COL: ['Date', 'Valutadatum', 'Buchungstag', 'Valuta'],
    AMOUNT_COL: ['Amount', 'Betrag', 'Betrag (EUR)'],
    PAYMENT_REASON_COL: ['Payment Reason', 'Verwendungszweck'],
    RECIPIENT_COL: ['Recipient', 'Beguenstigter/Zahlungspflichtiger', 'Auftraggeber / Begünstigter', 'Name']
}


INCOME_CATEGORY = 'Income'
MISC_CATEGORY = 'Misc'

categories = {
    INCOME_CATEGORY: None,
    'Dwelling': ['Rent', 'Miete', 'Rundfunk'],
    'Car': ['Fuel', 'Garage', 'Kfz-Steuer', 'KFZ-VERSICHERUNG', 'Tankstelle', 'JET', 'Aral', 'Esso', 'Shell', 'Total'],
    'Insurance': ['Insurance', 'HUK', 'HUK24'],
    'Grocery': ['Grocery', 'REWE', 'Kaufland', 'Aldi', 'Edeka', 'Lidl'],
    MISC_CATEGORY: None,
}


# UI related settings
CURRENCY_LABEL = 'EUR'
INCOME_LINE_STYLE = dict(color=('rgb(22, 167, 96)'), width=4)
