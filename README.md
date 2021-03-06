![](https://github.com/kircher-sw/expenses-report/workflows/Python%20Unittests/badge.svg)

# expenses-report
Keeps track of your personal expenses.
* visualizes your expenses by self defined categories
* automatically categorizes transactions imported form CSV files
* outputs an interactive html report

---

## Table of Contents
1. [Requirements](#requirements)
1. [Example](#example)
1. [Usage](#usage)

---

## Requirements
* <a href="https://www.python.org/downloads" target="_blank">Python 3</a> (3.6 or later)
* install dependent packages with
  ```
  pip install -r requirements.txt
  ```

## Example
Interactive demo report: [sample/sample-report.html](https://kircher-sw.github.io/expenses-report/sample/sample-report.html)

### Monthly expenses
![Categories by month](sample/category-month.png "expenses-report Categories by month")

### Annual expenses
![Categories by year](sample/category-year.png "expenses-report Categories by year")
![Pie chart](sample/pie-year.png "expenses-report Categories as a pie chart")

### Accumulated expenses
![Categories cumulated](sample/category-cumulated.png "expenses-report cumulated by categories")

### All expenses
![All expenses](sample/all-expenses.png "expenses-report")

## Usage
1. Clone repository
1. Adapt the file [**expenses_report/config.py**](expenses_report/config/config.py)
    * define the path to the folder which contains your CSV files (either absolute or relative to the project directory)
      ```python
      CSV_FILES_PATH = 'sample'
      ```
    * specify column names of the CSV files in the `import-mapping` dictionary
      ```python
      import_mapping = {
        DATE_COL: ['Date', 'Valuta'],
        ...
      }
      ```
    * define `categories` of interest and add keywords as they occur in your transactions
      ```python
      categories = {
        ...
        'Fixed costs': {
          'Dwelling': ['Rent'],
          'Insurances': ['Insurance', 'Allianz', 'HUK']
        },
        ...
      }
      ```
1. execute [**run.py**](run.py)
    * the script outputs a list of all uncategorized transactions on the command line for further refinement of the keywords
 
