
from expenses_report import config
from expenses_report.transaction import Transaction


class CategoryFinder(object):

    def assign_category(self, transactions):
        for ta in transactions:
            ta.category = self.find_category(ta)


    def find_category(self, transaction: Transaction):
        category = None

        if not transaction.is_expense():
            return config.INCOME_CATEGORY

        categories = config.categories
        for cat in categories.keys():
            if categories[cat]:
                for keyword in categories[cat]:
                    k = keyword.lower()
                    if k in transaction.payment_reason.lower() or k in transaction.recipient.lower():
                        category = cat
                        break
                if category is not None:
                    break

        if category is None:
            category = config.MISC_CATEGORY

        return category
