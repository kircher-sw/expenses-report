
from expenses_report.config import config
from expenses_report.preprocessing.transaction import Transaction


class CategoryFinder(object):
    _empty_category = ''

    def assign_category(self, transactions):
        """
        Assigns a category to each transaction.
        :param transactions:
        :return:
        """
        for ta in transactions:
            ta.main_category, ta.sub_category = self.find_category(ta)


    def find_category(self, transaction: Transaction):
        """
        Finds a matching category for the given transaction.
        If the amount of the transaction is positive, the INCOME category is returned, otherwise the first category with
        a matching keyword is used. If no matching keyword could be found the MISC category is used.
        :param transaction:
        :return: (main_category, sub_category)
        """
        category = None

        # income
        if not transaction.is_expense():
            category = self.find_sub_category(transaction, config.INCOME_CATEGORY)
            if category is None:
                category = config.INCOME_CATEGORY, self._empty_category

        else: # expense
            for main_cat in config.categories.keys():
                if main_cat is not config.INCOME_CATEGORY:
                    category = self.find_sub_category(transaction, main_cat)

                if category:
                    break

        if category is None:
            category = config.MISC_CATEGORY, self._empty_category

        return category


    def find_sub_category(self, transaction, main_category):
        category = None
        sub_categories = config.categories[main_category]

        if type(sub_categories) is dict:
            for sub_cat in sub_categories.keys():
                if self.has_matching_keyword(transaction, sub_categories[sub_cat]):
                    category = main_category, sub_cat
                    break

        elif type(sub_categories) is list:
            if self.has_matching_keyword(transaction, sub_categories):
                category = main_category, self._empty_category

        return category


    def has_matching_keyword(self, transaction, keywords):
        if keywords:
            for keyword in keywords:
                if self.is_keyword_in_transaction(transaction, keyword):
                    return True
        return False


    def is_keyword_in_transaction(self, transaction, keyword):
        k = keyword.lower()
        return k in transaction.payment_reason.lower() or k in transaction.recipient.lower()
