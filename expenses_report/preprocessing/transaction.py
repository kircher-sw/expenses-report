import math


class Transaction(object):
    account_no = ''
    date = None
    amount = 0.0
    payment_reason = ''
    recipient = ''
    main_category = ''
    sub_category = ''
    other_account_no = ''

    def __init__(self, account_no='', date=None, amount=0.0, payment_reason='', recipient='', main_category='',
                 sub_category = '', other_account_no=''):
        self.date = date
        self.amount = amount
        self.payment_reason = payment_reason
        self.recipient = recipient
        self.main_category = main_category
        self.sub_category = sub_category
        self.set_account_no(account_no)
        self.other_account_no = other_account_no

    def is_valid(self):
        return self.date is not None and self.amount is not None

    def is_expense(self):
        return self.amount < 0

    def set_account_no(self, account_raw):
        self.account_no = account_raw.rjust(22, '0')  # fill up with 0s to length of IBAN

    def set_other_account_no(self, other_account_raw):
        self.other_account_no = other_account_raw.rjust(22, '0')  # fill up with 0s to length of IBAN

    def as_tuple(self):
        return (self.account_no, self.date, self.amount, self.payment_reason, self.recipient,
                self.other_account_no, self.main_category, self.sub_category)

    def __repr__(self):
        return f'{self.account_no} | {self.date} | {self.amount} | {self.payment_reason} | {self.recipient} | ' \
               f'<{self.main_category}/{self.sub_category}>'

    def __eq__(self, other):
        if isinstance(other, Transaction):
            return self.account_no == other.account_no and \
                   self.date == other.date and \
                   math.isclose(self.amount, other.amount, rel_tol=1e-09, abs_tol=0.0) and \
                   self.amount == other.amount and \
                   self.payment_reason == other.payment_reason and \
                   self.recipient == other.recipient and \
                   self.main_category == other.main_category and \
                   self.sub_category == other.sub_category and \
                   self.other_account_no == other.other_account_no
        return False

    def __hash__(self):
        return hash(self.as_tuple())
