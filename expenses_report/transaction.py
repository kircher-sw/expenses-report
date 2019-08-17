import math


class Transaction(object):
    account_no = ''
    date = None
    amount = 0.0
    payment_reason = ''
    recipient = ''
    category = ''

    def __init__(self, account_no='', date=None, amount=0.0, payment_reason='', recipient='', category=''):
        self.date = date
        self.amount = amount
        self.payment_reason = payment_reason
        self.recipient = recipient
        self.category = category
        self.set_account_no(account_no)

    def is_valid(self):
        return self.date is not None and self.amount is not None

    def is_expense(self):
        return self.amount < 0

    def set_account_no(self, account_raw):
        self.account_no = account_raw.rjust(22, '0')  # fill up with 0s to length of IBAN

    def get_short_account_no(self):
        return self.account_no[-10:]

    def as_tuple(self):
        return (self.get_short_account_no(), self.date, self.amount, self.payment_reason, self.recipient, self.category)

    def __repr__(self):
        return f'{self.account_no} | {self.date} | {self.amount} | {self.payment_reason} | {self.recipient} | <{self.category}>'

    def __eq__(self, other):
        if isinstance(other, Transaction):
            return self.get_short_account_no() == other.get_short_account_no() and \
                   self.date == other.date and \
                   math.isclose(self.amount, other.amount, rel_tol=1e-09, abs_tol=0.0) and \
                   self.amount == other.amount and \
                   self.payment_reason == other.payment_reason and \
                   self.recipient == other.recipient and \
                   self.category == other.category
        return False

    def __hash__(self):
        return hash(self.as_tuple())
