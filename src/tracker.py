from unittest import TestCase, main
from os import remove
from pandas import read_csv
from datetime import datetime
from utils import testData, app_name, api_id, api_hash

from database import ExpenseDatabase
from formatter import GraphGenerator
from client import Client

class ExpenseTracker():
    def __init__(self, dbLocaiton, app_name, api_id, api_hash):
        self.db = ExpenseDatabase(dbLocaiton)
        self.plotter = GraphGenerator()
        self.client = Client(app_name, api_id, api_hash)
    def updateDatabase(self):
        parsedData = self.client.getMessages(100)
        print(parsedData)
        self.db.addExpenses(parsedData)
    def sendStats(self, period):
        dailyData, categoryData = self.db.getExpenses(period)
        dailyText = self.plotter.getOverall(dailyData, self.db.tBudget)
        categoryText = self.plotter.getCategory(categoryData, self.db.budgets)
        print(dailyText, categoryText)
        self.client.sendMessage(dailyText)
        self.client.sendMessage(categoryText)

class TestExpenseTracker(TestCase):
    def test_application(self):
        testDataFile = 'testData.csv'
        dbFileName = 'databaseUnitTest.json'
        try:
            remove(dbFileName)
        except OSError:
            pass
        app = ExpenseTracker(dbFileName, app_name, api_id, api_hash)
        reference = read_csv(testDataFile, delimiter=';')
        expenses = []
        for i, row in reference.iterrows():
            iDate = datetime.strptime(row['Date'], '%d-%m-%Y')
            row['Date'] = iDate.strftime('%Y-%m-%d')
            expenses.append({'vendor': row['Vendor'], 'category': row['Category'], 
                             'date': row['Date'], 'amount': row['Amount']})
        app.db.addExpenses(expenses)

        for item in testData:
            text = 'EA: ' + item['vendor'] + ', ' + item['category'] + ', ' + str(item['amount'])
            app.client.sendMessage(text)

        app.updateDatabase()
        app.sendStats(datetime.now().strftime('%Y-%m'))

if __name__ == "__main__":
    main()