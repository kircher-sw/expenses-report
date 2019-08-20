import pandas as pd

from expenses_report import config

pd.options.mode.chained_assignment = None  # default='warn'

class TransactionPreprocessor(object):
    CATEGORY_COL = 'category'
    ABSAMOUNT_COL = 'absamount'
    LABEL = 'label'
    _transactions = list()
    _columns = None
    _df_all = None
    _df_in = None
    _df_out = None

    def __init__(self):
        self._columns = list(config.import_mapping.keys()) + [self.CATEGORY_COL]

    def set_transactions(self, transactions):
        self._transactions = transactions
        self._df_all = self._df_in = self._df_out = None


    def aggregate_transactions_by_category(self, aggregation_period='M'):
        """
        Aggregates the transactions by category and the given aggregation period
        :param aggregation_period: 'M' group by month
                                   'Y' group by year
        :return: [date range], { category1-name: [category1 values], ... }
        """

        # create full range of date values with the given period
        df_all = self._get_dataframe_of_all_transactions()
        end_date = df_all.index.max().to_period(aggregation_period).end_time.date()
        range_of_all_dates = pd.date_range(start=df_all.index.min(), end=end_date, freq=aggregation_period)
        df_all_dates = range_of_all_dates.to_period().to_frame(name=config.DATE_COL)
        x_axis = list(map(lambda p: p.to_timestamp(), df_all_dates.index.values))

        values_all_categories = dict()

        # income
        df_in = self._get_dataframe_of_in_transactions()
        df_in = df_in.resample(aggregation_period).sum().reindex(range_of_all_dates).fillna(0)
        values_all_categories[config.INCOME_CATEGORY] = df_in[self.ABSAMOUNT_COL].values

        # gain
        df_gain = df_all.resample(aggregation_period).sum().reindex(range_of_all_dates).fillna(0)
        values_all_categories[config.GAIN_CATEGORY] = df_gain[config.AMOUNT_COL].values

        # expenses
        df_out = self._get_dataframe_of_out_transactions()
        df_out_agg = df_out.groupby([pd.DatetimeIndex(df_out.index).to_period(aggregation_period),
                                     self.CATEGORY_COL])[self.ABSAMOUNT_COL].sum()

        for category_name, df_category in df_out_agg.groupby(self.CATEGORY_COL):
            result = pd.merge(df_all_dates, df_category, on=config.DATE_COL, how='left')
            values_out_category = result.fillna(0)[self.ABSAMOUNT_COL].values
            values_all_categories[category_name] = values_out_category

        return (x_axis, values_all_categories)


    def aggregate_expenses_by_year(self):
        """
        Aggregates all expenses by category and year and calculates a total for each year.
        :return: { year: (total, [category names], [category values]), ... }
        """
        result = dict()
        df_out = self._get_dataframe_of_out_transactions()
        df_out_agg_years = df_out.groupby([df_out.index.year, self.CATEGORY_COL])[self.ABSAMOUNT_COL].sum()

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
        df_all = self._get_dataframe_of_all_transactions()
        x_axis = list(map(lambda date: date, df_all.resample('D').sum().index))
        cumulative_categories = dict()
        for category_name in reversed(list(config.categories.keys())):
            df_category = df_all if category_name == config.GAIN_CATEGORY else df_all[df_all.category == category_name]
            df_category = df_category.resample('D').sum().reindex(df_all.index).resample('D').max().fillna(0)

            agg_column = self.ABSAMOUNT_COL
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
        df_out = self._get_dataframe_of_out_transactions()
        for category_name in config.categories.keys():
            df_category = df_out[df_out.category == category_name]
            category_total = df_category[self.ABSAMOUNT_COL].sum()
            df_category.loc[:, RATIO] = df_category[self.ABSAMOUNT_COL] / category_total
            x_axis = list(map(lambda datetime: pd.Timestamp(datetime), pd.DatetimeIndex(df_category.index).values))
            if x_axis:
                result[category_name] = (x_axis,
                                         df_category[self.ABSAMOUNT_COL].values,
                                         df_category[RATIO].values,
                                         df_category[self.LABEL].values)
        return result

    def _rebuild_dataframes(self):
        # create DataFrame from imported transactions
        ta_tuples = list(map(lambda ta: ta.as_tuple(), self._transactions))
        self._df_all = pd.DataFrame.from_records(data=ta_tuples, columns=self._columns, index=config.DATE_COL)
        self._df_all[self.ABSAMOUNT_COL] = self._df_all.amount.apply(abs)
        self._df_all[self.LABEL] = self._df_all[config.PAYMENT_REASON_COL] + '<br>' + self._df_all[config.RECIPIENT_COL]

        self._df_in = self._df_all[self._df_all.category == config.INCOME_CATEGORY]

        self._df_out = self._df_all[self._df_all.category != config.INCOME_CATEGORY]

    def _get_dataframe_of_all_transactions(self):
        if self._df_all is None:
            self._rebuild_dataframes()
        return self._df_all

    def _get_dataframe_of_in_transactions(self):
        if self._df_in is None:
            self._rebuild_dataframes()
        return self._df_in

    def _get_dataframe_of_out_transactions(self):
        if self._df_out is None:
            self._rebuild_dataframes()
        return self._df_out
