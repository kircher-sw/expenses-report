import datetime
import re


def parse_date(date_string):
    date = None
    if re.match(r'^\d\d\.\d\d\.\d\d$', date_string):
        date = datetime.datetime.strptime(date_string, '%d.%m.%y')
    elif re.match(r'^\d\d\.\d\d\.\d\d\d\d$', date_string):
        date = datetime.datetime.strptime(date_string, '%d.%m.%Y')
    elif re.match(r'^\d\d-\d\d-\d\d$', date_string):
        date = datetime.datetime.strptime(date_string, '%y-%m-%d')
    elif re.match(r'^\d\d\d\d-\d\d-\d\d$', date_string):
        date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    return date
