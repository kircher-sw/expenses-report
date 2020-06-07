import pandas as pd

from expenses_report.argument_parser import ArgumentParser
from expenses_report.chart_builder import ChartBuilder
from expenses_report.config import config
from expenses_report.html_report import HtmlReport
from expenses_report.preprocessing.category_finder import CategoryFinder
from expenses_report.preprocessing.csv_importer import CsvImporter
from expenses_report.preprocessing.data_provider import DataProvider
from expenses_report.visualizations.accumulated_trend_visualization import AccumulatedTrendVisualization
from expenses_report.visualizations.annual_sunburst_visualization import AnnualSunburstVisualization
from expenses_report.visualizations.annual_trend_visualization import AnnualTrendVisualization
from expenses_report.visualizations.monthly_subcategories_visualization import MonthlySubcategoriesVisualization
from expenses_report.visualizations.monthly_trend_visualization import MonthlyTrendVisualization
from expenses_report.visualizations.transaction_bubbles_visualization import TransactionBubblesVisualization
from expenses_report.visualizations.transaction_table_visualization import TransactionTableVisualization

pd.options.mode.chained_assignment = None  # default='warn'

class ExpensesReport(object):
    _transactions = list()
    _data_provider: DataProvider
    _charts = list()

    def transactions_updated(self):
        self._data_provider = DataProvider.load(self._transactions)


_expenses_report = ExpensesReport()

def configure_script():
    parser = ArgumentParser()
    parser.configure_script()

def import_csv_files():
    importer = CsvImporter()
    transactions = importer.import_from_csv_files()
    transactions = remove_internal_transactions(transactions)
    _expenses_report._transactions = transactions


def remove_internal_transactions(transactions):
    own_account_numbers = set(map(lambda ta: ta.account_no, transactions)) | config.OWN_ACCOUNTS
    clean_transactions = list(filter(lambda ta: ta.other_account_no not in own_account_numbers, transactions))
    #internal_transactions = set(transactions) - set(clean_transactions)
    return clean_transactions

def assign_category_to_transactions():
    transactions = _expenses_report._transactions
    category_finder = CategoryFinder()
    category_finder.assign_category(transactions)
    _expenses_report.transactions_updated()
    print_transactions_statistics(transactions)


def print_transactions_statistics(transactions):
    print('-----------------')
    print(f'Total transactions {len(transactions)}')
    print('-----------------')
    uncategorized_transactions = list(filter(lambda ta: ta.main_category == config.MISC_CATEGORY, transactions))
    print(f'Uncategorized transactions {len(uncategorized_transactions)}')
    for ta in uncategorized_transactions:
        print(ta)
    print('-----------------')

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 2000)
    df_all = _expenses_report._data_provider.get_all_transactions()

    #print(df_all.sort_values(by=[config.CATEGORY_MAIN_COL, config.CATEGORY_SUB_COL]))

    print(df_all.sort_values(by=[config.DATE_COL, config.CATEGORY_MAIN_COL, config.CATEGORY_SUB_COL]).loc[:,
          [config.CATEGORY_MAIN_COL, config.CATEGORY_SUB_COL, config.AMOUNT_COL, config.PAYMENT_REASON_COL,
           config.RECIPIENT_COL]])


def calculate_charts():

    visualizations = [MonthlyTrendVisualization(),
                      MonthlySubcategoriesVisualization(),
                      AnnualTrendVisualization(),
                      AnnualSunburstVisualization(),
                      TransactionBubblesVisualization(),
                      AccumulatedTrendVisualization(),
                      TransactionTableVisualization()]

    data = _expenses_report._data_provider
    charts = list(map(lambda vis: vis.build(data), visualizations))
    html_plots = list(map(lambda chart: ChartBuilder._create_plot(chart), charts))

    _expenses_report._charts = html_plots


def write_report():
    HtmlReport.create(_expenses_report._charts)
