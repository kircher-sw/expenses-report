import plotly.graph_objects as go

from expenses_report.preprocessing.data_provider import DataProvider

class IVisualization:
    """"""

    def prepare_data(self, data: DataProvider):
        """"""
        pass


    def build_visualization(self) -> go.Figure:
        """"""
        pass

    def build(self, data: DataProvider):
        self.prepare_data(data)
        return self.build_visualization()
