
from expenses_report import config
from expenses_report.argument_parser import ArgumentParser
from expenses_report.csv_importer import CsvImporter
from expenses_report.category_finder import CategoryFinder
from expenses_report.transaction_preprocessor import TransactionPreprocessor
from expenses_report.chart_creator import ChartCreator
from expenses_report.html_report import HtmlReport

import pandas as pd
import plotly
import plotly.express as px


class ExpensesReport(object):
    _transactions = list()
    _ta_preprocessor = TransactionPreprocessor()
    _charts = list()

    def transactions_updated(self):
        self._ta_preprocessor.set_transactions(self._transactions)

    def create_stacked_area_chart_with_month_frequency(self):
        x_axis, values_all_categories = self._ta_preprocessor.aggregate_transactions_by_category(aggregation_period='M')
        self._charts.append(ChartCreator.create_stacked_area_plot(x_axis, values_all_categories, show_range_selectors=True))

    def create_stacked_area_chart_with_year_frequency(self):
        x_axis, values_all_categories = self._ta_preprocessor.aggregate_transactions_by_category(aggregation_period='Y')
        self._charts.append(ChartCreator.create_stacked_area_plot(x_axis, values_all_categories))

    def create_pie_chart_with_categories_by_year(self):
        #results = self._ta_preprocessor.aggregate_expenses_by_year()
        #self._charts.append(ChartCreator.create_pie_plot(results))

        df_out = self._ta_preprocessor._get_dataframe_of_out_transactions()
        df_out_agg_years = df_out.groupby([df_out.index.year, self._ta_preprocessor.CATEGORY_MAIN_COL,
                                           self._ta_preprocessor.CATEGORY_SUB_COL])[self._ta_preprocessor.ABSAMOUNT_COL].sum()
        df = df_out_agg_years[df_out_agg_years.index.get_level_values(0) == 2019].reset_index()
        df.loc[df.sub_category == '', self._ta_preprocessor.CATEGORY_SUB_COL] = None
        fig = px.sunburst(df,
                          path=[self._ta_preprocessor.CATEGORY_MAIN_COL, self._ta_preprocessor.CATEGORY_SUB_COL],
                          values=self._ta_preprocessor.ABSAMOUNT_COL)
        sunburst_chart = plotly.offline.plot(fig, output_type='div', include_plotlyjs=False)
        self._charts.append(sunburst_chart)


    def create_stacked_area_with_cumulative_categories(self):
        x_axis, cumulative_categories = self._ta_preprocessor.accumulate_categories()
        self._charts.append(ChartCreator.create_stacked_area_plot(x_axis, cumulative_categories))

    def create_transaction_bubble_chart(self):
        result = self._ta_preprocessor.preprocess_by_category()
        self._charts.append(ChartCreator.create_bubble_chart(result))


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
    own_account_numbers = set(list(map(lambda ta: ta.account_no, transactions)))
    clean_transactions = list(filter(lambda ta: ta.other_account_no not in own_account_numbers, transactions))
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


def calculate_charts():
    _expenses_report.create_stacked_area_chart_with_month_frequency()
    _expenses_report.create_stacked_area_chart_with_year_frequency()
    _expenses_report.create_pie_chart_with_categories_by_year()
    _expenses_report.create_stacked_area_with_cumulative_categories()
    _expenses_report.create_transaction_bubble_chart()


def write_report():
    HtmlReport.create(_expenses_report._charts)
