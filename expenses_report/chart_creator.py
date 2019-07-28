import plotly
import plotly.graph_objs as go

from expenses_report import config


class ChartCreator(object):

    @staticmethod
    def create_stacked_area_plot(x_axes, values_all_categories, show_range_selectors=False):
        traces_unsorted = list()
        for category_name in values_all_categories.keys():
            trace_category = go.Scatter(x=x_axes,
                                        y=values_all_categories[category_name],
                                        name=config.INCOME_CATEGORY,
                                        line=config.income_line_style) \
                             if category_name == config.INCOME_CATEGORY else \
                             go.Scatter(x=x_axes,
                                        y=values_all_categories[category_name],
                                        name=category_name,
                                        mode='lines',
                                        stackgroup='out')
            traces_unsorted.append(trace_category)

        traces = ChartCreator._sort_legend_by_config_order(traces_unsorted)

        layout = dict(yaxis=dict(title=config.CURRENCY))
        x_axes_layout = ChartCreator._get_x_axes_layout(x_axes)
        if x_axes_layout:
            layout['xaxis'] = x_axes_layout

        if show_range_selectors:
            ChartCreator._add_range_selectors(layout)

        return plotly.offline.plot(dict(data=traces, layout=layout), output_type='div', include_plotlyjs=False)

    @staticmethod
    def _get_x_axes_layout(x_axes):
        x_axes_layout = None
        if len(x_axes) >= 2:
            if (x_axes[1] - x_axes[0]).days >= 365: # year resolution
                x_axes_layout = dict(tickformat='%Y', nticks=len(x_axes))
            elif (x_axes[1] - x_axes[0]).days >= 28: # month resolution
                x_axes_layout = dict(tickformat='%b %Y')
        return x_axes_layout

    @staticmethod
    def _sort_legend_by_config_order(traces_unsorted):
        traces = list()
        all_categories = list(config.categories.keys())
        for category_name in reversed(all_categories):
            trace = next((t for t in traces_unsorted if t.name == category_name), None)
            if trace:
                traces.append(trace)
        return traces

    @staticmethod
    def _add_range_selectors(layout):
        current_xaxis = layout['xaxis'] if 'xaxis' in layout else dict()
        new_xaxis = dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=6, step='month', label='6m', stepmode='backward'),
                    dict(count=1, step='year', label='1y', stepmode='backward'),
                    dict(count=3, step='year', label='3y', stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=True,
                thickness=0.08
            ),
            type='date')
        layout['xaxis'] = {**current_xaxis, **new_xaxis}

    @staticmethod
    def create_pie_plot(year, total, labels, values):
        pie_trace = go.Pie(labels=labels,
                           values=values,
                           hole=0.3,
                           title=f'{year}<br>{total:.2f} {config.CURRENCY}',
                           textinfo='label+value+percent',
                           textposition='inside')
        return plotly.offline.plot(dict(data=[pie_trace]), output_type='div', include_plotlyjs=False)
