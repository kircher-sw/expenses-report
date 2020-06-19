"""
Config for expenses-report

Only modify text within '...'
"""

# Path to the CSV files from your bank account. All CSV files from this path will be read and processed.
CSV_FILES_PATH = 'sample'

CSV_DELIMITER = ';'

OUT_FILE = 'sample/sample-report.html'
REPORT_TEMPLATE = 'expenses-report-layout.html'

# CSV column identifiers (do not modify)
ACCOUNT_NO_COL = 'accountno'
DATE_COL = 'date'
AMOUNT_COL = 'amount'
PAYMENT_REASON_COL = 'paymentreason'
RECIPIENT_COL = 'recipient'
OTHER_ACCOUNT_NO_COL = 'otheraccountno'

CATEGORY_MAIN_COL = 'main_category'
CATEGORY_SUB_COL = 'sub_category'
ABSAMOUNT_COL = 'absamount'
LABEL = 'label'

# CSV column identification
# Add the names of the CSV columns as a new element to each list. If you have CSV files from different bank accounts
# with different column header names you could add multiple entries per row.
# Usually the column names can be found in the first row of the CSV file.
import_mapping = {
    ACCOUNT_NO_COL: ['Account No', 'Auftragskonto', 'Kontonummer'],  # optional (list may be empty)
    DATE_COL: ['Date', 'Valutadatum', 'Buchungstag', 'Valuta'],  # mandatory
    AMOUNT_COL: ['Amount', 'Betrag', 'Betrag (EUR)'],  # mandatory
    PAYMENT_REASON_COL: ['Payment Reason', 'Verwendungszweck'],  # optional if RECIPIENT_COL is set
    RECIPIENT_COL: ['Recipient', 'Beguenstigter/Zahlungspflichtiger', 'Auftraggeber / Begünstigter', 'Name'],
    # optional if PAYMENT_REASON_COL is set
    OTHER_ACCOUNT_NO_COL: ['Kontonummer/IBAN'],
}

INITIAL_ACCOUNT_BALANCE = 0.0

OWN_ACCOUNTS = set()

EXPENSES_LABEL = 'Expenses'

# Category name for income
INCOME_CATEGORY = 'Income'

# Label for all uncategorized transactions. This category is assigned if no matching keyword was found.
MISC_CATEGORY = 'Misc'

# Mapping of categories and their keywords.
# Add or remove categories and define keywords for them as they occur in the PAYMENT_REASON or RECIPIENT field of
# the transactions. (Don't add keywords for MISC category)
categories = {
    INCOME_CATEGORY: {
        'Salary': ['Salary'],
        MISC_CATEGORY: None
    },

    'Fixed costs': {
        'Dwelling': ['Rent', 'Miete'],
        'Insurances': ['Insurance', 'Allianz', 'HUK']
    },

    'Variable costs': {
        'Supermarket': ['Grocery', 'REWE', 'Kaufland', 'Aldi', 'Edeka', 'Lidl'],
        'Fuel': ['Fuel', 'JET', 'Aral', 'Esso', 'Shell', 'Total']
    },

    'Donations': ['unicef', 'Brot für die Welt'],

    MISC_CATEGORY: None,
}

# UI related settings
CURRENCY_LABEL = 'EUR'
INCOME_LINE_STYLE = dict(color=('rgb(22, 167, 96)'), width=4)
