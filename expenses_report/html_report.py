import os

from expenses_report import config

class HtmlReport(object):

    placeholder = '$CHART'

    @staticmethod
    def _load_html_template(file):
        html = ''
        with open(file, 'r') as html_template:
            html = html_template.read()
        return html

    @staticmethod
    def _build_html_report(html, charts):
        html_report = html
        for chart_div in charts:
            html_report = html_report.replace(HtmlReport.placeholder, chart_div, 1)
        return html_report

    @staticmethod
    def create(charts):
        html_template = HtmlReport._load_html_template(os.path.join('resources', 'expenses-report-layout.html'))
        html_report = HtmlReport._build_html_report(html_template, charts)

        f = open(config.OUT_FILE, 'w')
        f.write(html_report)
        f.close()