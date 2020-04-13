import pandas as pd

from expenses_report.config import config

class DataFormatter(object):

    _transactions = list()
    _columns = None

    def __init__(self, transactions):
        self._transactions = transactions
        self._columns = list(config.import_mapping.keys()) + [config.CATEGORY_MAIN_COL, config.CATEGORY_SUB_COL]

    @staticmethod
    def load(transactions):
        formatter = DataFormatter(transactions)
        formatter._rebuild_dataframes()
        return formatter


    def _rebuild_dataframes(self):
        # creates DataFrames from imported transactions
        ta_tuples = list(map(lambda ta: ta.as_tuple(), self._transactions))
        self._df_all = pd.DataFrame.from_records(data=ta_tuples, columns=self._columns, index=config.DATE_COL)
        self._df_all[config.ABSAMOUNT_COL] = self._df_all.amount.apply(abs)
        self._df_all[config.LABEL] = self._df_all[config.PAYMENT_REASON_COL] + '<br>' + self._df_all[config.RECIPIENT_COL]

        self._df_in = self._df_all[self._df_all.main_category == config.INCOME_CATEGORY]
        self._df_out = self._df_all[self._df_all.main_category != config.INCOME_CATEGORY]

    def get_all_transactions(self):
        if self._df_all is None:
            self._rebuild_dataframes()
        return self._df_all

    def get_in_transactions(self):
        if self._df_in is None:
            self._rebuild_dataframes()
        return self._df_in

    def get_out_transactions(self):
        if self._df_out is None:
            self._rebuild_dataframes()
        return self._df_out

    def get_full_date_range(self, aggregation_period='MS'):
        '''
        Builds a dataframe containing the full date range of the specified period
        :param aggregation_period: {'MS' for month start, 'YS' for year start, ... }, default 'MS'
            see https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects
        :return:
        '''
        df_all = self.get_all_transactions()

        delta_period = aggregation_period.rstrip('S') if len(aggregation_period) > 1 else aggregation_period

        df_all_dates = pd.date_range(df_all.index.min() - pd.Timedelta(1, delta_period),
                                     df_all.index.max(),
                                     freq=aggregation_period,
                                     normalize=True).to_period().to_frame(name=config.DATE_COL)
        return df_all_dates

    def aggregate_data(self, dataframe, aggregation_period='MS'):
        df_all_dates = self.get_full_date_range(aggregation_period)
        return dataframe.resample(aggregation_period).sum().reindex(df_all_dates.index.to_timestamp()).fillna(0)
