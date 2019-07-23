
CSV_FILES_PATH = 'sample'


ACCOUNT_NO_COL = 'accountno'
DATE_COL = 'date'
AMOUNT_COL = 'amount'
PAYMENT_REASON_COL = 'paymentreason'
RECIPIENT_COL = 'recipient'

import_mapping = {
    ACCOUNT_NO_COL: ['Auftragskonto', 'Kontonummer'],
    DATE_COL: ['Valutadatum', 'Buchungstag', 'Valuta'],
    AMOUNT_COL: ['Betrag', 'Betrag (EUR)'],
    PAYMENT_REASON_COL: ['Verwendungszweck'],
    RECIPIENT_COL: ['Beguenstigter/Zahlungspflichtiger', 'Auftraggeber / Begünstigter', 'Name']
}


INCOME_CATEGORY = 'Einkommen'
MISC_CATEGORY = 'Sonstiges'

categories = {
    INCOME_CATEGORY: None,
    'Wohnung': ['Miete', 'Rundfunk'],
    'Auto': ['Kfz-Steuer', 'KFZ-VERSICHERUNG', 'Tankstelle', 'JET', 'Aral', 'Esso', 'Shell', 'Total'],
    'Versicherung': ['HUK', 'HUK24'],
    'Lebensmittel': ['BONUS', 'REWE', 'Kaufland', 'Aldi', 'Edeka', 'Lidl'],
    'Urlaub': ['TUI', 'Hotel'],
    'Bahn': ['DB VERTRIEB', 'DEUTSCHE BAHN', 'LogPay'],
    'Anschaffung': ['Amazon', 'ALTERNATE', 'MEDIA MARKT'],
    'Bargeld': ['BW-Bank', 'Landesbank BW', 'Bargeld'],
    'Spende': ['Spende'],
    'Sparen': ['Sparen'],
    MISC_CATEGORY: None,
}


CURRENCY = 'EUR'

income_line_style = dict(color=('rgb(22, 167, 96)'), width=4)
