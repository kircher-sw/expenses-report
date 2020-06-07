import pandas as pd
from plotly import graph_objects as go

from expenses_report.chart_builder import ChartBuilder
from expenses_report.config import config
from expenses_report.preprocessing.data_provider import DataProvider
from expenses_report.visualizations.i_visualization import IVisualization


class TransactionBubblesVisualization(IVisualization):
    _category_values = dict()

    def prepare_data(self, data: DataProvider):
        """
        Preprocesses each transaction and calculates the relative amount within its category
        """
        RATIO = 'ratio'
        df_all = data.get_all_transactions()
        for category_name in config.categories.keys():
            df_category = df_all[df_all[config.CATEGORY_MAIN_COL] == category_name]
            category_total = df_category[config.ABSAMOUNT_COL].sum()
            df_category.loc[:, RATIO] = df_category[config.ABSAMOUNT_COL] / category_total
            x_axis = list(map(lambda datetime: pd.Timestamp(datetime), pd.DatetimeIndex(df_category.index).values))
            if x_axis:
                self._category_values[category_name] = (x_axis,
                                                        df_category[config.ABSAMOUNT_COL].values,
                                                        df_category[RATIO].values,
                                                        df_category[config.LABEL].values)


    def build_visualization(self) -> go.Figure:
        return ChartBuilder.create_bubble_chart(self._category_values)
