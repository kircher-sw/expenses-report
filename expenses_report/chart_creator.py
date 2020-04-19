import plotly
import plotly.graph_objs as go
import plotly.graph_objects as gos
import pandas as pd

from expenses_report.config import config
from expenses_report.preprocessing.data_formatter import DataFormatter


class ChartCreator(object):

    @staticmethod
    def create_stacked_area_plot(x_axis, values_all_categories, show_range_selectors=False):
        figure = go.Figure()
        for category_name in values_all_categories.keys():
            trace = go.Scatter(x=x_axis,
                               y=values_all_categories[category_name],
                               name=config.INCOME_CATEGORY,
                               line=config.INCOME_LINE_STYLE) \
                    if category_name == config.INCOME_CATEGORY else \
                    go.Scatter(x=x_axis,
                               y=values_all_categories[category_name],
                               name=category_name,
                               mode='lines',
                               stackgroup='out')
            figure.add_trace(trace)

        # layout options
        ChartCreator._sort_legend(figure, config.categories.keys())
        ChartCreator._set_x_axis_layout(figure, x_axis)
        ChartCreator._set_y_axis_layout(figure)

        if show_range_selectors:
            ChartCreator._add_time_span_selectors(figure)

        return ChartCreator._create_plot(figure)


    @staticmethod
    def create_multi_stacked_area_plot(x_axis, values_main_categories, show_range_selectors=True):
        figure = go.Figure()
        main_category_counts = list()
        for main_category in values_main_categories.keys():
            values_sub_category = values_main_categories[main_category]
            main_category_counts.append(len(values_sub_category))
            for sub_category in values_sub_category.keys():
                figure.add_trace(go.Scatter(x=x_axis,
                                            y=values_sub_category[sub_category],
                                            name=sub_category,
                                            mode='lines',
                                            visible=False,
                                            stackgroup=main_category))

        # layout options
        ChartCreator._set_x_axis_layout(figure, x_axis)
        ChartCreator._set_y_axis_layout(figure)
        ChartCreator._add_main_category_buttons(figure, values_main_categories.keys(), main_category_counts)

        if show_range_selectors:
            ChartCreator._add_time_span_selectors(figure)

        return ChartCreator._create_plot(figure)


    @staticmethod
    def create_bubble_chart(result):
        figure = go.Figure()
        for category_name in result.keys():
            x_values, y_values, ratios, labels = result[category_name]
            size = [max(15, ratio * 10000) for ratio in ratios]
            figure.add_trace(go.Scatter(x=x_values,
                                        y=y_values,
                                        name=category_name,
                                        hovertext=labels,
                                        mode='markers',
                                        marker=dict(size=size,
                                                    sizemode='area',
                                                    line=dict(width=2))))

        ChartCreator._set_y_axis_layout(figure)
        ChartCreator._add_time_span_selectors(figure)
        figure.layout.update(yaxis=dict(type='log'))

        return ChartCreator._create_plot(figure)


    @staticmethod
    def create_pie_plot(results):
        # create pie charts for each year
        figure = go.Figure()
        for year in results.keys():
            total, labels, values = results[year]
            figure.add_trace(go.Pie(name=str(year),
                                    labels=labels,
                                    values=values,
                                    hole=0.3,
                                    title=f'{year}<br>{total:.2f} {config.CURRENCY_LABEL}',
                                    textinfo='label+value+percent',
                                    textposition='inside'))

        ChartCreator._add_range_slider(figure)

        return ChartCreator._create_plot(figure)


    @staticmethod
    def create_sunburst_plot(dataframe):
        out_categories = list(filter(lambda cat: cat is not config.INCOME_CATEGORY, config.categories.keys()))
        color_map = dict((cat, out_categories.index(cat) / (len(out_categories)-1)) for cat in out_categories)

        figure = go.Figure()
        for year in list(dataframe[config.DATE_COL].unique()):
            df_year = dataframe.loc[dataframe[config.DATE_COL] == year, :]
            df_all_trees = DataFormatter.build_hierarchical_dataframe(df_year,
                                                                      str(year),
                                                                      [config.CATEGORY_SUB_COL, config.CATEGORY_MAIN_COL],
                                                                      config.ABSAMOUNT_COL,
                                                                      color_map)

            figure.add_trace(gos.Sunburst(labels=df_all_trees['id'],
                                          parents=df_all_trees['parent'],
                                          values=df_all_trees['value'],
                                          #marker=dict(colors=df_all_trees['color'], colorscale='RdBu', cmid=0.5),
                                          visible=False,
                                          hoverinfo='label+value+percent entry',
                                          branchvalues='total',
                                          name=str(year)))

        ChartCreator._add_range_slider(figure)
        return ChartCreator._create_plot(figure)



    @staticmethod
    def _sort_legend(figure, category_order):
        traces_unsorted = figure.data
        figure.data = []
        for category_name in reversed(list(category_order)):
            trace = next((t for t in traces_unsorted if t.name == category_name), None)
            if trace:
                figure.add_trace(trace)

    @staticmethod
    def _set_x_axis_layout(figure, x_axis):
        x_axis_layout = None
        if len(x_axis) >= 2:
            if (x_axis[1] - x_axis[0]).days >= 365:  # year resolution
                x_axis_layout = dict(tickformat='%Y', nticks=len(x_axis))
            elif (x_axis[1] - x_axis[0]).days >= 28:  # month resolution
                x_axis_layout = dict(tickformat='%b %Y')

        if x_axis_layout:
            figure.layout.update(xaxis=x_axis_layout)

    @staticmethod
    def _set_y_axis_layout(figure):
        figure.layout.update(yaxis=dict(title=config.CURRENCY_LABEL))

    @staticmethod
    def _add_main_category_buttons(figure, categories, category_counts):
        buttons = list()
        for i, category in enumerate(categories):
            button = dict(label=category,
                          method='restyle',
                          args=['visible', [False] * len(figure.data)])

            trace_offset = sum(category_counts[:i])
            trace_count = category_counts[i]
            for j in range(trace_count):
                button['args'][1][trace_offset + j] = True  # Toggle i'th trace to "visible"
                figure.data[trace_offset + j].visible = (i == 0)

            buttons.append(button)

        button_menu = dict(buttons=buttons,
                           type='buttons',
                           direction='right',
                           pad={"r": 0, "b": 40},
                           showactive=True,
                           x=0,
                           xanchor="left",
                           y=1,
                           yanchor="bottom")

        figure.layout.update(updatemenus=[button_menu])

    @staticmethod
    def _add_time_span_selectors(figure):
        x_axis = dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=6, step='month', label='6m', stepmode='backward'),
                    dict(count=1, step='year', label='1y', stepmode='backward'),
                    dict(count=3, step='year', label='3y', stepmode='backward'),
                    dict(step='all')])),
            type='date')
        figure.layout.update(xaxis=x_axis)

    @staticmethod
    def _add_range_slider(figure):
        traces = figure.data
        steps = list()
        for i, trace in enumerate(traces):
            trace.visible = (i == len(traces) - 1)
            step = dict(label=trace.name,
                        method='restyle',
                        args=['visible', [False] * len(traces)])
            step['args'][1][i] = True  # Toggle i'th trace to "visible"
            steps.append(step)

        slider = dict(active=len(traces) - 1,
                      currentvalue={'prefix': 'Year: '},
                      pad={'t': 0},  # vertical distance to chart
                      steps=steps)

        figure.layout.update(sliders=[slider])

    @staticmethod
    def _create_plot(figure):
        return plotly.offline.plot(figure, output_type='div', include_plotlyjs=False)