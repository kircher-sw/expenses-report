import pandas as pd
from plotly import graph_objects as go

from expenses_report.chart_builder import ChartBuilder
from expenses_report.config import config
from expenses_report.preprocessing.data_provider import DataProvider
from expenses_report.visualizations.i_visualization import IVisualization


class TransactionTableVisualization(IVisualization):
    _df_all_ta: pd.DataFrame

    def prepare_data(self, data: DataProvider):
        column_order = [config.PAYMENT_REASON_COL,
                        config.RECIPIENT_COL,
                        config.CATEGORY_MAIN_COL,
                        config.CATEGORY_SUB_COL,
                        config.AMOUNT_COL]

        self._df_all_ta = data.get_all_transactions(). \
                        sort_values(by=[config.DATE_COL, config.CATEGORY_MAIN_COL, config.CATEGORY_SUB_COL]). \
                        loc[:, column_order].reset_index()

    def build_visualization(self) -> go.Figure:
        header_row = ['Date', 'Payment reason', 'Recipient', 'Main-category', 'Sub-category', 'Amount']
        return ChartBuilder.create_table(self._df_all_ta, header_row)
