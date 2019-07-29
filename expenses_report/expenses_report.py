
from expenses_report import config
from expenses_report.csv_importer import CsvImporter
from expenses_report.category_finder import CategoryFinder
from expenses_report.transaction_preprocessor import TransactionPreprocessor
from expenses_report.chart_creator import ChartCreator


class ExpensesReport(object):
    _transactions = list()
    _ta_preprocessor = TransactionPreprocessor()
    _stacked_area_month = None
    _stacked_area_year = None
    _pie_year = None
    _cumulative_categories = None

    def __init__(self):
        pass

    def transactions_updated(self):
        self._ta_preprocessor.set_transactions(self._transactions)

    def create_stacked_area_chart_with_month_frequency(self):
        x_axes, values_all_categories = self._ta_preprocessor.preprocess_by_category('M')
        self._stacked_area_month = ChartCreator.create_stacked_area_plot(x_axes, values_all_categories, show_range_selectors=True)

    def create_stacked_area_chart_with_year_frequency(self):
        x_axes, values_all_categories = self._ta_preprocessor.preprocess_by_category('Y')
        self._stacked_area_year = ChartCreator.create_stacked_area_plot(x_axes, values_all_categories)

    def create_pie_chart_with_categories_by_year(self):
        results = self._ta_preprocessor.preprocess_by_year()
        self._pie_year = ChartCreator.create_pie_plot(results)

    def create_stacked_area_with_cumulative_categories(self):
        x_axes, cumulative_categories = self._ta_preprocessor.preprocess_cumulative_categories()
        self._cumulative_categories = ChartCreator.create_stacked_area_plot(x_axes, cumulative_categories)


_expenses_report = ExpensesReport()


def import_csv_files():
    importer = CsvImporter()
    importer.import_csv_files()
    _expenses_report._transactions = importer.transactions


def assign_category_to_transactions():
    transactions = _expenses_report._transactions
    category_finder = CategoryFinder()
    category_finder.assign_category(transactions)
    _expenses_report.transactions_updated()

    print('-----------------')
    print(f'Total transactions {len(transactions)}')
    print('-----------------')
    uncategorized_transactions = list(filter(lambda ta: ta.category == config.MISC_CATEGORY, transactions))
    print(f'Uncategorized transactions {len(uncategorized_transactions)}')
    for ta in uncategorized_transactions:
        print(ta)
    print('-----------------')


def calculate_charts():
    _expenses_report.create_stacked_area_chart_with_month_frequency()
    _expenses_report.create_stacked_area_chart_with_year_frequency()
    _expenses_report.create_pie_chart_with_categories_by_year()
    _expenses_report.create_stacked_area_with_cumulative_categories()


def write_report():
    f = open('expenses.html', 'w')
    f.write('<html>'
            '<head><meta charset="utf-8" />'
            '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            '<style>'
            '* { box-sizing: border-box; }'
            '.column { float: left; width: 50%; padding: 10px; }'
            '.row:after { content: ""; display: table; clear: both; }'
            '</style>'
            '</head>'
            '<body>')
    f.write(_expenses_report._stacked_area_month)
    f.write('<div class="row">'
            '<div class="column">')
    f.write(_expenses_report._stacked_area_year)
    f.write('</div>'
            '<div class="column">')
    f.write(_expenses_report._pie_year)
    f.write('</div>'
            '</div>')
    f.write(_expenses_report._cumulative_categories)
    #f.write(df_all.to_html().replace('<table border="1" class="dataframe">', '<table class="table table-striped">'))
    f.write('</body>'
            '</html>')
    f.close()


