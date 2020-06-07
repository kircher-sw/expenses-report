import pandas as pd
from itertools import product

from expenses_report.config import config
from expenses_report.preprocessing.data_provider import DataProvider

pd.options.mode.chained_assignment = None  # default='warn'

class TransactionPreprocessor(object):

    _formatter = None

    def set_transactions(self, transactions):
        self._formatter = DataProvider.load(transactions)


    def aggregate_transactions_by_category(self, aggregation_period='MS'):
        """
        Aggregates the transactions by category and the given aggregation period
        :param aggregation_period: 'M' group by month
                                   'Y' group by year
        :return: [date range], { category1-name: [category1 values], ... }
        """

        df_all = self._formatter.get_all_transactions()
        x_axis, category_values = self._formatter.aggregate_by_category_as_tuple(df_all, aggregation_period,
                                                                                 config.CATEGORY_MAIN_COL,
                                                                                 config.ABSAMOUNT_COL)

        return x_axis, category_values


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


    def calculate_month_summaries(self, months):

        df_all = self._formatter.get_all_transactions()
        df_agg_months = df_all.groupby([df_all.index.to_period('M'), config.CATEGORY_MAIN_COL])[
            config.ABSAMOUNT_COL].sum().reset_index()

        df_summaries = list()
        for m in months:
            end_month = df_agg_months[config.DATE_COL].max()
            start_month = (end_month.to_timestamp() - pd.Timedelta(m - 1, unit='M')).to_period('M')

            df_range = df_agg_months[df_agg_months[config.DATE_COL].between(start_month, end_month)]

            df_prod = pd.DataFrame(list(product(df_range[config.DATE_COL].unique(), config.categories.keys())),
                                   columns=[config.DATE_COL, config.CATEGORY_MAIN_COL])
            df_range_full = df_prod.merge(df_range, how='left').fillna(0)

            df_mean = df_range_full.groupby([config.CATEGORY_MAIN_COL])[config.ABSAMOUNT_COL].mean().reset_index()

            # sort by category order as defined in config
            configOrder = list(config.categories.keys())
            df_mean['index'] = df_mean.apply(lambda row: configOrder.index(row[config.CATEGORY_MAIN_COL]) if row[config.CATEGORY_MAIN_COL] in configOrder else 1000,
                                             axis=1)

            total_out = df_mean[config.ABSAMOUNT_COL].sum() - df_mean.loc[
                df_mean[config.CATEGORY_MAIN_COL] == config.INCOME_CATEGORY, config.ABSAMOUNT_COL]
            df_mean = df_mean.append(
                pd.Series({config.CATEGORY_MAIN_COL: config.EXPENSES_LABEL, config.ABSAMOUNT_COL: total_out, 'index': -2}),
                ignore_index=True)
            df_mean = df_mean.append(
                pd.Series({config.CATEGORY_MAIN_COL: '-----', config.ABSAMOUNT_COL: None, 'index': -1}),
                ignore_index=True)
            df_mean.loc[df_mean[config.CATEGORY_MAIN_COL] == config.INCOME_CATEGORY, 'index'] = -3
            df_mean = df_mean.sort_values(by=['index'])
            df_summaries.append(df_mean)

        return df_summaries


    def accumulate_categories(self):
        """
        Accumulates all transactions by category
        :return: [date range], { category1-name: [category1 values], ... }
        """
        df_all = self._formatter.get_all_transactions()
        x_axis = list(map(lambda date: date, df_all.resample('D').sum().index))
        cumulative_categories = dict()
        for category_name in reversed(list(config.categories.keys())):
            df_category = df_all[df_all.main_category == category_name]
            df_category = df_category.resample('D').sum().reindex(df_all.index).resample('D').max().fillna(0)

            values = list(df_category[config.ABSAMOUNT_COL].cumsum())
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


