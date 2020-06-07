import pandas as pd
from plotly import graph_objects as go

from expenses_report.chart_builder import ChartBuilder
from expenses_report.config import config
from expenses_report.preprocessing.data_provider import DataProvider
from expenses_report.visualizations.i_visualization import IVisualization


class AnnualSunburstVisualization(IVisualization):
    _df_agg_years: pd.DataFrame

    def prepare_data(self, data: DataProvider):
        df_out = data.get_out_transactions()
        self._df_agg_years = df_out.groupby([df_out.index.year,
                                             config.CATEGORY_MAIN_COL,
                                             config.CATEGORY_SUB_COL])[config.ABSAMOUNT_COL].sum().reset_index()
        self._df_agg_years.loc[self._df_agg_years.sub_category == '', config.CATEGORY_SUB_COL] = None  # do not plot missing values

    def build_visualization(self) -> go.Figure:
        return ChartBuilder.create_sunburst_plot(self._df_agg_years)
