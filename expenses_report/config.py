"""
Config for expenses-report

Only modify text within '...'
"""


# Path to the CSV files from your bank account. All CSV files from this path will be read and processed.
CSV_FILES_PATH = 'sample'

CSV_DELIMITER = ';'

OUT_FILE = 'expenses-report.html'


# CSV column identifiers (do not modify)
ACCOUNT_NO_COL = 'accountno'
DATE_COL = 'date'
AMOUNT_COL = 'amount'
PAYMENT_REASON_COL = 'paymentreason'
RECIPIENT_COL = 'recipient'

# CSV column identification
# Add the names of the CSV columns as a new element to each list. If you have CSV files from different bank accounts
# with different column header names you could add multiple entries per row.
# Usually the column names can be found in the first row of the CSV file.
import_mapping = {
    ACCOUNT_NO_COL: ['Account No', 'Auftragskonto', 'Kontonummer'],
    DATE_COL: ['Date', 'Valutadatum', 'Buchungstag', 'Valuta'],
    AMOUNT_COL: ['Amount', 'Betrag', 'Betrag (EUR)'],
    PAYMENT_REASON_COL: ['Payment Reason', 'Verwendungszweck'],
    RECIPIENT_COL: ['Recipient', 'Beguenstigter/Zahlungspflichtiger', 'Auftraggeber / Begünstigter', 'Name']
}


# Category name for income
INCOME_CATEGORY = 'Income'

# Label for all uncategorized transactions. This category is assigned if no matching keyword was found.
MISC_CATEGORY = 'Misc'

# Mapping of categories and their keywords.
# Add or remove categories and define keywords for them as they occur in the PAYMENT_REASON or RECIPIENT field of
# the transactions. (Don't add keywords for INCOME and MISC category)
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
