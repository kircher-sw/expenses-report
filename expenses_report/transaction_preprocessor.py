import pandas as pd

from expenses_report.config import config
from expenses_report.preprocessing.data_formatter import DataFormatter

pd.options.mode.chained_assignment = None  # default='warn'

class TransactionPreprocessor(object):

    _formatter = None

    def set_transactions(self, transactions):
        self._formatter = DataFormatter.load(transactions)


    def aggregate_transactions_by_category(self, aggregation_period='MS'):
        """
        Aggregates the transactions by category and the given aggregation period
        :param aggregation_period: 'M' group by month
                                   'Y' group by year
        :return: [date range], { category1-name: [category1 values], ... }
        """

        # income
        df_in = self._formatter.get_in_transactions()
        df_in = self._formatter.aggregate_data(df_in, aggregation_period)

        # expenses
        df_out = self._formatter.get_out_transactions()
        period = aggregation_period.rstrip('S') if len(aggregation_period) > 1 else aggregation_period
        df_out_agg = df_out.groupby([df_out.index.to_period(period), config.CATEGORY_MAIN_COL])[config.ABSAMOUNT_COL].sum()

        df_all_dates = self._formatter.get_full_date_range(aggregation_period)
        x_axis, out_traces = DataFormatter.create_traces_for_groups(df_out_agg, config.CATEGORY_MAIN_COL, df_all_dates, config.ABSAMOUNT_COL)

        values_all_categories = dict()
        values_all_categories[config.INCOME_CATEGORY] = df_in[config.ABSAMOUNT_COL].values
        values_all_categories = {**values_all_categories, **out_traces}

        return (x_axis, values_all_categories)


    def aggregate_expenses_by_year(self):
        """
        Aggregates all expenses by category and year and calculates a total for each year.
        :return: { year: (total, [category names], [category values]), ... }
        """
        result = dict()
        df_out = self._formatter.get_out_transactions()
        df_out_agg_years = df_out.groupby([df_out.index.year, config.CATEGORY_MAIN_COL])[config.ABSAMOUNT_COL].sum()

        years = list(df_out_agg_years.index.levels[0].values)
        for year in years:
            df_out_agg_year = df_out_agg_years[df_out_agg_years.index.get_level_values(0) == year]

            labels = list(map(lambda tuple: tuple[1], df_out_agg_year.index.values))
            values = list(df_out_agg_year.values)
            total = df_out_agg_year.values.sum()

            result[year] = (total, labels, values)

        return result


    def accumulate_categories(self):
        """
        Accumulates all transactions by category
        :return: [date range], { category1-name: [category1 values], ... }
        """
        df_all = self._formatter.get_all_transactions()
        x_axis = list(map(lambda date: date, df_all.resample('D').sum().index))
        cumulative_categories = dict()
        for category_name in reversed(list(config.categories.keys())):
            df_category = df_all if category_name == config.GAIN_CATEGORY else df_all[df_all.main_category == category_name]
            df_category = df_category.resample('D').sum().reindex(df_all.index).resample('D').max().fillna(0)

            agg_column = config.ABSAMOUNT_COL
            if category_name == config.GAIN_CATEGORY:
                df_category.loc[df_category.index.min(), config.AMOUNT_COL] += config.INITIAL_ACCOUNT_BALANCE
                agg_column = config.AMOUNT_COL

            values = list(df_category[agg_column].cumsum())
            cumulative_categories[category_name] = values

        return (x_axis, cumulative_categories)

    def preprocess_by_category(self):
        """
        Preprocesses each transaction and calculates the relative amount within its category
        :return:
        """
        RATIO = 'ratio'
        result = dict()
        df = self._formatter.get_all_transactions()
        for category_name in config.categories.keys():
            df_category = df[df.main_category == category_name]
            category_total = df_category[config.ABSAMOUNT_COL].sum()
            df_category.loc[:, RATIO] = df_category[config.ABSAMOUNT_COL] / category_total
            x_axis = list(map(lambda datetime: pd.Timestamp(datetime), pd.DatetimeIndex(df_category.index).values))
            if x_axis:
                result[category_name] = (x_axis,
                                         df_category[config.ABSAMOUNT_COL].values,
                                         df_category[RATIO].values,
                                         df_category[config.LABEL].values)
        return result


