import pandas as pd
import plotly.graph_objects as go

from expenses_report.chart_builder import ChartBuilder
from expenses_report.config import config
from expenses_report.preprocessing.data_provider import DataProvider
from expenses_report.visualizations.i_visualization import IVisualization


class MonthlyTrendVisualization(IVisualization):
    _x_axis: list
    _category_values: dict
    _df_summaries = list()

    def prepare_data(self, data: DataProvider):
        df_all = data.get_all_transactions()
        df_agg_months = data.aggregate_by_category(df_all, 'MS',
                                                   config.CATEGORY_MAIN_COL)

        self._prepare_data_monthly_chart(data, df_agg_months)
        self._prepare_data_average_table(df_agg_months.reset_index())


    def build_visualization(self) -> go.Figure:
        return ChartBuilder.create_trend_chart_with_table(self._x_axis,
                                                          self._category_values,
                                                          self._df_summaries,
                                                          show_range_selectors=True)


    def _prepare_data_monthly_chart(self, data: DataProvider, df_agg_months: pd.DataFrame):
        self._x_axis, self._category_values = data.expand_by_categories(df_agg_months,
                                                                        config.CATEGORY_MAIN_COL)


    def _prepare_data_average_table(self, df_agg_months: pd.DataFrame):
        months = [3, 6, 12, 36, 100 * 12]
        for m in months:
            end_month = df_agg_months[config.DATE_COL].max()
            start_month = (end_month.to_timestamp() - pd.Timedelta(m - 1, unit='M')).to_period('M')

            df_mean = df_agg_months[df_agg_months[config.DATE_COL].between(start_month, end_month)]. \
                groupby(config.CATEGORY_MAIN_COL).mean().reset_index()

            # sort by category order as defined in config
            configOrder = list(config.categories.keys())
            df_mean['index'] = df_mean.apply(lambda row: configOrder.index(row[config.CATEGORY_MAIN_COL]) if row[
                                                                                                                 config.CATEGORY_MAIN_COL] in configOrder else 1000,
                                             axis=1)

            total_out = df_mean[config.ABSAMOUNT_COL].sum() - df_mean.loc[
                df_mean[config.CATEGORY_MAIN_COL] == config.INCOME_CATEGORY, config.ABSAMOUNT_COL]
            df_mean = df_mean.append(
                pd.Series(
                    {config.CATEGORY_MAIN_COL: config.EXPENSES_LABEL, config.ABSAMOUNT_COL: total_out, 'index': -2}),
                ignore_index=True)
            df_mean = df_mean.append(
                pd.Series({config.CATEGORY_MAIN_COL: '-----', config.ABSAMOUNT_COL: None, 'index': -1}),
                ignore_index=True)
            df_mean.loc[df_mean[config.CATEGORY_MAIN_COL] == config.INCOME_CATEGORY, 'index'] = -3
            df_mean = df_mean.sort_values(by=['index'])
            self._df_summaries.append(df_mean)

