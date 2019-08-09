# expenses-report
Keeps track of your personal expenses.
* visualizes your expenses by self defined categories
* reads transactions from csv files exported from your bank account
* automatically assigns categories to your expenses
* outputs an interactive html report

---

## Table of Contents
1. [Requirements](#requirements)
1. [Example](#example)
1. [Usage](#usage)

---

## Requirements
* Python >= 3.6
* Pandas >= 0.25.0
* Plotly >= 4.1.0

## Example
For an interactive report demonstration see [sample/sample-report.html](https://kircher-sw.github.io/expenses-report/sample/sample-report.html)

### Categories grouped by month
![Categories by month](sample/category-month.png "expenses-report Categories by month")

### Categories grouped by year
![Categories by year](sample/category-year.png "expenses-report Categories by year")

### Categories as a pie-chart
![Pie chart](sample/pie-year.png "expenses-report Categories as a pie chart")

### All transactions cumulated by categories
![Categories cumulated](sample/category-cumulated.png "expenses-report cumulated by categories")

## Usage
1. Clone repository
1. Adapt the file [**expenses_report/config.py**](expenses_report/config.py)
    * define the path to the folder which contains your CSV files (either absolute or relative to the project directory)
      ``` python
      CSV_FILES_PATH = 'sample'
      ```
    * specify column names of the CSV files in the `import-mapping` dictionary
      ``` python
      import_mapping = {
        ACCOUNT_NO_COL: ['Account No'],
        ...
      }
      ```
    * define `categories` of interest and add keywords as they occur in your transactions
      ``` python
      categories = {
        ...
        'Car': ['Fuel', 'Garage', ...],
        ...
      }
      ```
1. execute [**run.py**](run.py)
    * the script outputs a list of all uncategorized transactions on the command line for further refinement of the keywords
 