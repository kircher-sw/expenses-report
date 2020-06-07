from plotly import graph_objects as go

from expenses_report.chart_builder import ChartBuilder
from expenses_report.config import config
from expenses_report.preprocessing.data_provider import DataProvider
from expenses_report.visualizations.i_visualization import IVisualization


class AnnualTrendVisualization(IVisualization):
    _x_axis: list
    _category_values: dict

    def prepare_data(self, data: DataProvider):
        df_all = data.get_all_transactions()
        self._x_axis, self._category_values = data.aggregate_by_category_as_tuple(df_all, 'YS',
                                                                                  config.CATEGORY_MAIN_COL,
                                                                                  config.ABSAMOUNT_COL)

    def build_visualization(self) -> go.Figure:
        return ChartBuilder.create_stacked_area_plot(self._x_axis, self._category_values)
