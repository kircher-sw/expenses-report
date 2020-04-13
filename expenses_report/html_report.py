import os
import re

from expenses_report.config import config

class HtmlReport(object):

    chart_placeholder = '$CHART'
    script_placeholder = '$SCRIPT'

    @staticmethod
    def create(charts):
        html_template = HtmlReport._load_html_template()
        html_report = HtmlReport._build_html_report(html_template, charts)
        HtmlReport._write_file(html_report)


    @staticmethod
    def _load_html_template():
        template_path = os.path.join('resources', 'expenses-report-layout.html')
        with open(template_path, 'r') as html_template:
            html = html_template.read()
        return html

    @staticmethod
    def _build_html_report(html_template, charts):
        html_report = html_template
        divs, scripts = HtmlReport._split_charts_into_div_and_script(charts)

        # insert div elements for each chart
        for chart_div in divs:
            html_report = html_report.replace(HtmlReport.chart_placeholder, chart_div, 1)

        # put chart rendering scripts to the end of the html document to have correct sizes in css layout items
        all_scripts = '\n'.join(scripts)
        html_report = html_report.replace(HtmlReport.script_placeholder, all_scripts)

        return html_report

    @staticmethod
    def _split_charts_into_div_and_script(charts):
        divs = list()
        scripts = list()
        chart_regex = re.compile(r'(<div id=.*?></div>)(.*)</div>', re.DOTALL)
        for chart in charts:
            chart_matches = chart_regex.search(chart)
            if chart_matches:
                divs.append(chart_matches.group(1))
                scripts.append(chart_matches.group(2))
        return divs, scripts

    @staticmethod
    def _write_file(html_report):
        f = open(config.OUT_FILE, 'w')
        f.write(html_report)
        f.close()

