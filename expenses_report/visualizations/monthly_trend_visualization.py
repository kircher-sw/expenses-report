import pandas as pd
import plotly.graph_objects as go

from expenses_report.chart_builder import ChartBuilder
from expenses_report.config import config
from expenses_report.preprocessing.data_provider import DataProvider
from expenses_report.visualizations.i_visualization import IVisualization


class MonthlyTrendVisualization(IVisualization):
    INDEX_COL = 'index'
    _x_axis: list
    _category_values: dict
    _df_summaries = list()

    def prepare_data(self, data: DataProvider):
        df_all = data.get_all_transactions()
        df_agg_months = data.aggregate_by_category(df_all, 'MS', config.CATEGORY_MAIN_COL)

        self._prepare_data_monthly_chart(data, df_agg_months)
        self._prepare_data_average_table(df_agg_months.reset_index())


    def build_visualization(self) -> go.Figure:
        return ChartBuilder.create_trend_chart_with_table(self._x_axis,
                                                          self._category_values,
                                                          self._df_summaries,
                                                          show_range_selectors=True)


    def _prepare_data_monthly_chart(self, data: DataProvider, df_agg_months: pd.DataFrame):
        self._x_axis, self._category_values = data.expand_by_categories(df_agg_months, config.CATEGORY_MAIN_COL)


    def _prepare_data_average_table(self, df_agg_months: pd.DataFrame):
        months = [3, 6, 12, 36, 100 * 12]
        for m in months:
            end_month = df_agg_months[config.DATE_COL].max()
            start_month = end_month - (m - 1)

            df_range = df_agg_months[df_agg_months[config.DATE_COL].between(start_month, end_month)]
            df_mean = df_range.groupby(config.CATEGORY_MAIN_COL).mean().reset_index()

            # sort by category order as defined in config
            config_order = list(config.categories.keys())
            df_mean[self.INDEX_COL] = df_mean[config.CATEGORY_MAIN_COL].apply(lambda main_cat: config_order.index(main_cat) if main_cat in config_order else 1000)
            total_out = df_mean.loc[df_mean[config.CATEGORY_MAIN_COL] != config.INCOME_CATEGORY, config.ABSAMOUNT_COL].sum()

            df_mean.loc[df_mean[config.CATEGORY_MAIN_COL] == config.INCOME_CATEGORY, self.INDEX_COL] = -3
            df_mean = df_mean.append(self._new_row(-2, config.EXPENSES_LABEL, total_out), ignore_index=True)
            df_mean = df_mean.append(self._new_row(-1, '-----', None), ignore_index=True)

            df_mean = df_mean.sort_values(by=[self.INDEX_COL])
            self._df_summaries.append(df_mean)


    def _new_row(self, index, category, value):
        return pd.Series({config.CATEGORY_MAIN_COL: category, config.ABSAMOUNT_COL: value, self.INDEX_COL: index})
