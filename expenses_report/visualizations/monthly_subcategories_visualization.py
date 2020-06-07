from plotly import graph_objects as go

from expenses_report.chart_builder import ChartBuilder
from expenses_report.config import config
from expenses_report.preprocessing.data_provider import DataProvider
from expenses_report.visualizations.i_visualization import IVisualization


class MonthlySubcategoriesVisualization(IVisualization):
    _x_axis: list
    _main_category_values = dict()

    def prepare_data(self, data: DataProvider):
        df_all = data.get_all_transactions().copy()
        df_all.loc[df_all[config.CATEGORY_SUB_COL] == '', config.CATEGORY_SUB_COL] = config.MISC_CATEGORY

        for main_category in config.categories.keys():
            df_cat = df_all.loc[
                df_all[config.CATEGORY_MAIN_COL] == main_category, [config.CATEGORY_SUB_COL, config.ABSAMOUNT_COL]]

            self._x_axis, sub_category_values = data.aggregate_by_category_as_tuple(df_cat, 'MS', config.CATEGORY_SUB_COL)
            self._main_category_values[main_category] = sub_category_values

    def build_visualization(self) -> go.Figure:
        return ChartBuilder.create_multi_stacked_area_plot(self._x_axis, self._main_category_values)
