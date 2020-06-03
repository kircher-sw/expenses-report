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


    @staticmethod
    def build_hierarchical_dataframe(df, root_label, levels, value_column, color_map):
        """
        Build a hierarchy of levels for Sunburst or Treemap charts.

        Levels are given starting from the bottom to the top of the hierarchy,
        ie the last level corresponds to the root.
        """
        columns = ['id', 'parent', 'value', 'color']
        df_all_trees = pd.DataFrame(columns=columns)
        for i, level in enumerate(levels):
            df_tree = pd.DataFrame(columns=columns)
            dfg = df.groupby(levels[i:]).sum()
            dfg = dfg.reset_index()
            df_tree['id'] = dfg[level].copy()
            if i < len(levels) - 1:
                df_tree['parent'] = dfg[levels[i + 1]].copy()
            else:
                df_tree['parent'] = root_label
            df_tree['value'] = dfg[value_column]
            #df_tree['color'] = df_tree.apply(lambda row: color_map[row['id']] if row['id'] in color_map.keys() else 0.5, axis=1)
            df_all_trees = df_all_trees.append(df_tree, ignore_index=True)
        root_node = pd.Series(dict(id=root_label,
                                   parent='',
                                   value=df[value_column].sum(),
                                   color=0))
        df_all_trees = df_all_trees.append(root_node, ignore_index=True)
        return df_all_trees

    @staticmethod
    def create_traces_for_groups(df, group_label, df_all_dates, value_column):
        traces = dict()
        x_axis = list(df_all_dates.index.to_timestamp())
        for category_name, df_category in df.groupby(group_label):
            df_result = pd.merge(df_all_dates, df_category, on=config.DATE_COL, how='left')
            values_category = df_result.fillna(0)[value_column].values
            traces[category_name] = values_category

        return x_axis, traces
