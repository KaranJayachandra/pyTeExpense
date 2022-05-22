
from unittest import TestCase, main
from tinydb import TinyDB, Query
from datetime import datetime, timedelta
from calendar import monthrange
from utils import budgets

from pandas import read_csv, to_datetime
from os import remove

class ExpenseDatabase:
    def __init__(self, dbLocation):
        self.expenses = TinyDB(dbLocation)
        self.user = Query()
        self.budgets = budgets
        self.tBudget = sum([value for key, value in self.budgets.items()])
    def addExpenses(self, data):
        for item in data:
            self.expenses.insert({'vendor': item['vendor'], 'category': item['category'], 
                                  'date': item['date'], 'amount': item['amount']})
    def getExpenses(self, period):
        categories = [row['category'] for row in self.expenses]
        categoryExpenses = dict.fromkeys(list(set(categories)), 0)
        referenceDate = datetime.strptime(period, '%Y-%m')
        totalDays = monthrange(referenceDate.year, referenceDate.month)[1]
        dailyExpenses = dict.fromkeys([i for i in range(1, totalDays + 1)], 0)
        for row in self.expenses:
            iDate = datetime.strptime(row['date'], '%Y-%m-%d')
            if iDate.year == referenceDate.year and iDate.month == referenceDate.month:
                categoryExpenses[row['category']] += row['amount']
                dailyExpenses[int(iDate.strftime('%d'))] += row['amount']
        dailyExpenses = {key : round(dailyExpenses[key], 3) for key in dailyExpenses}
        categoryExpenses = {key : round(categoryExpenses[key], 3) for key in categoryExpenses}
        return dailyExpenses, categoryExpenses
    def __del__(self):
        self.expenses.close()

def testHelper():
    referenceFileName = 'testData.csv'
    dbFileName = 'databaseUnitTest.json'
    reference = read_csv(referenceFileName, delimiter=';')
    try:
        remove(dbFileName)
    except OSError:
        pass
    database = ExpenseDatabase('databaseUnitTest.json')
    return reference, database

class TestExpenseDatabase(TestCase):
    def test_addExpense(self):
        reference, database = testHelper()
        expenses = []
        for i, row in reference.iterrows():
            iDate = datetime.strptime(row['Date'], '%d-%m-%Y')
            row['Date'] = iDate.strftime('%Y-%m-%d')
            expenses.append({'vendor': row['Vendor'], 'category': row['Category'], 
                             'date': row['Date'], 'amount': row['Amount']})
        database.addExpenses(expenses)
        aData = reference.Amount.sum()
        tData = sum([row['amount'] for row in database.expenses])
        self.assertAlmostEqual(tData, aData, 2, "Expense Addition Fails")
        database.expenses.drop_tables()
    def test_getExpenses(self):
        reference, database = testHelper()
        dateToCheck = datetime.now() - timedelta(30)
        reference['Date'] = to_datetime(reference['Date'], format='%d-%m-%Y')
        expenses = []
        for i, row in reference.iterrows():
            row['Date'] = row['Date'].strftime('%Y-%m-%d')
            expenses.append({'vendor': row['Vendor'], 'category': row['Category'], 
                             'date': row['Date'], 'amount': row['Amount']})
        database.addExpenses(expenses)
        reference = reference[(reference['Date'].dt.year == int(dateToCheck.strftime('%Y')))]
        reference = reference[(reference['Date'].dt.month == int(dateToCheck.strftime('%m')))]
        reference['Day'] = reference['Date'].dt.day
        aData1 = reference.groupby('Day').sum().to_dict()['Amount']
        aData1 = {key : round(aData1[key], 3) for key in aData1}
        aData2 = reference.groupby('Category').sum().to_dict()['Amount']
        tData1, tData2 = database.getExpenses(dateToCheck.strftime('%Y-%m'))
        tData1 = dict((k, v) for k, v in tData1.items() if v != 0)
        self.assertDictEqual(tData1, aData1, "Getting Daily Expenses Failed")
        self.assertDictEqual(tData2, aData2, "Getting Category Expenses Failed")
        database.expenses.drop_tables()

if __name__ == "__main__":
    main()