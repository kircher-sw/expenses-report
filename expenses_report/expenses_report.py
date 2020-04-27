
from expenses_report.config import config
from expenses_report.argument_parser import ArgumentParser
from expenses_report.preprocessing.csv_importer import CsvImporter
from expenses_report.preprocessing.category_finder import CategoryFinder
from expenses_report.preprocessing.data_formatter import DataFormatter
from expenses_report.transaction_preprocessor import TransactionPreprocessor
from expenses_report.chart_creator import ChartBuilder
from expenses_report.html_report import HtmlReport

import pandas as pd


class ExpensesReport(object):
    _transactions = list()
    _ta_preprocessor = TransactionPreprocessor()
    _charts = list()

    def transactions_updated(self):
        self._ta_preprocessor.set_transactions(self._transactions)

    def create_stacked_area_chart_with_month_frequency(self):
        x_axis, values_all_categories = self._ta_preprocessor.aggregate_transactions_by_category(aggregation_period='MS')
        #self._charts.append(ChartBuilder.create_stacked_area_plot(x_axis, values_all_categories, show_range_selectors=True))

        df_all = self._ta_preprocessor._formatter.get_all_transactions()
        df_agg_months = df_all.groupby([df_all.index.to_period('M'), config.CATEGORY_MAIN_COL])[
            config.ABSAMOUNT_COL].sum().reset_index()
        df_mean = df_agg_months.groupby([config.CATEGORY_MAIN_COL])[config.ABSAMOUNT_COL].mean().reset_index()

        # sort by category order as defined in config
        configOrder = list(config.categories.keys())
        df_mean['index'] = df_mean.apply(lambda row: configOrder.index(row[config.CATEGORY_MAIN_COL]) if row[config.CATEGORY_MAIN_COL] in configOrder else 1000, axis=1)

        total_out = df_mean[config.ABSAMOUNT_COL].sum() - df_mean.loc[
            df_mean[config.CATEGORY_MAIN_COL] == config.INCOME_CATEGORY, config.ABSAMOUNT_COL]
        df_mean = df_mean.append(pd.Series({config.CATEGORY_MAIN_COL: 'Ausgaben', config.ABSAMOUNT_COL: total_out, 'index': -2}), ignore_index=True)
        df_mean = df_mean.append(pd.Series({config.CATEGORY_MAIN_COL: '', config.ABSAMOUNT_COL: None, 'index': -1}), ignore_index=True)
        df_mean.loc[df_mean[config.CATEGORY_MAIN_COL] == config.INCOME_CATEGORY, 'index'] = -3
        df_mean = df_mean.sort_values(by=['index'])

        trendAndTableChart = ChartBuilder.create_trend_chart_with_table(x_axis, values_all_categories, df_mean, show_range_selectors=True)
        self._charts.append(trendAndTableChart)

    def create_stacked_area_chare_with_month_frequency_for_each_category(self):
        df_all = self._ta_preprocessor._formatter.get_all_transactions()
        df_agg_months = df_all.groupby([df_all.index.to_period('M'), config.CATEGORY_MAIN_COL,
                                        config.CATEGORY_SUB_COL])[config.ABSAMOUNT_COL].sum().reset_index()
        df_agg_months.loc[df_agg_months.sub_category == '', config.CATEGORY_SUB_COL] = config.MISC_CATEGORY

        df_all_dates = self._ta_preprocessor._formatter.get_full_date_range('MS')

        values_main_categories = dict()
        x_axis = list()
        for category in config.categories.keys():
            df_cat = df_agg_months.loc[df_agg_months[config.CATEGORY_MAIN_COL] == category, [config.DATE_COL, config.CATEGORY_SUB_COL, config.ABSAMOUNT_COL]]

            x_axis, values_sub_categories = DataFormatter.create_traces_for_groups(df_cat, config.CATEGORY_SUB_COL, df_all_dates, config.ABSAMOUNT_COL)
            values_main_categories[category] = values_sub_categories

        cat_stacked_chart = ChartBuilder.create_multi_stacked_area_plot(x_axis, values_main_categories)
        self._charts.append(cat_stacked_chart)

    def create_table_stats(self):
        df_all = self._ta_preprocessor._formatter.get_all_transactions()
        df_agg_months = df_all.groupby([df_all.index.to_period('M'), config.CATEGORY_MAIN_COL])[config.ABSAMOUNT_COL].sum().reset_index()
        df_mean = df_agg_months.groupby([config.CATEGORY_MAIN_COL])[config.ABSAMOUNT_COL].mean().reset_index()
        table = ChartBuilder.create_table(df_mean)
        self._charts.append(table)
        pass

    def create_stacked_area_chart_with_year_frequency(self):
        x_axis, values_all_categories = self._ta_preprocessor.aggregate_transactions_by_category(aggregation_period='YS')
        self._charts.append(ChartBuilder.create_stacked_area_plot(x_axis, values_all_categories))

    def create_pie_chart_with_categories_by_year(self):
        #results = self._ta_preprocessor.aggregate_expenses_by_year()
        #self._charts.append(ChartCreator.create_pie_plot(results))

        df_out = self._ta_preprocessor._formatter.get_out_transactions()
        df_out_agg_years = df_out.groupby([df_out.index.year, config.CATEGORY_MAIN_COL,
                                           config.CATEGORY_SUB_COL])[config.ABSAMOUNT_COL].sum().reset_index()
        df_out_agg_years.loc[df_out_agg_years.sub_category == '', config.CATEGORY_SUB_COL] = None  # do not plot missing values

        sunburst_chart = ChartBuilder.create_sunburst_plot(df_out_agg_years)
        self._charts.append(sunburst_chart)


    def create_stacked_area_with_cumulative_categories(self):
        x_axis, cumulative_categories = self._ta_preprocessor.accumulate_categories()
        self._charts.append(ChartBuilder.create_stacked_area_plot(x_axis, cumulative_categories))

    def create_transaction_bubble_chart(self):
        result = self._ta_preprocessor.preprocess_by_category()
        self._charts.append(ChartBuilder.create_bubble_chart(result))


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
    df_all = _expenses_report._ta_preprocessor._formatter.get_all_transactions()

    #print(df_all.sort_values(by=[config.CATEGORY_MAIN_COL, config.CATEGORY_SUB_COL]))

    print(df_all.sort_values(by=[config.DATE_COL, config.CATEGORY_MAIN_COL, config.CATEGORY_SUB_COL]).loc[:,
          [config.CATEGORY_MAIN_COL, config.CATEGORY_SUB_COL, config.AMOUNT_COL, config.PAYMENT_REASON_COL,
           config.RECIPIENT_COL]])


def calculate_charts():
    _expenses_report.create_stacked_area_chart_with_month_frequency()
    _expenses_report.create_table_stats()
    _expenses_report.create_stacked_area_chare_with_month_frequency_for_each_category()
    _expenses_report.create_stacked_area_chart_with_year_frequency()
    _expenses_report.create_pie_chart_with_categories_by_year()
    _expenses_report.create_transaction_bubble_chart()
    _expenses_report.create_stacked_area_with_cumulative_categories()


def write_report():
    HtmlReport.create(_expenses_report._charts)
