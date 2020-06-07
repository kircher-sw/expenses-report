from plotly import graph_objects as go

from expenses_report.chart_builder import ChartBuilder
from expenses_report.config import config
from expenses_report.preprocessing.data_provider import DataProvider
from expenses_report.visualizations.i_visualization import IVisualization


class AccumulatedTrendVisualization(IVisualization):
    _x_axis: list
    _cumulative_categories = dict()

    def prepare_data(self, data: DataProvider):
        """
        Accumulates all transactions by category
        """
        df_all = data.get_all_transactions()
        self._x_axis = list(map(lambda date: date, df_all.resample('D').sum().index))

        for category_name in reversed(list(config.categories.keys())):
            df_category = df_all[df_all[config.CATEGORY_MAIN_COL] == category_name]
            df_category = df_category.resample('D').sum().reindex(df_all.index).resample('D').max().fillna(0)

            values = list(df_category[config.ABSAMOUNT_COL].cumsum())
            self._cumulative_categories[category_name] = values


    def build_visualization(self) -> go.Figure:
        return ChartBuilder.create_stacked_area_plot(self._x_axis, self._cumulative_categories)
