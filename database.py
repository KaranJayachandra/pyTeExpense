from pandas import read_csv
from tinydb import TinyDB, Query
import unittest

class ExpenseDatabase:
    def __init__(self, dbLocation):
        self.db = TinyDB(dbLocation)
        self.user = Query()
        self.expenseTable = self.db.table('Expenses')
        self.vendorTable = self.db.table('Vendor')
    def addVendor(self, name, category):
        data = self.vendorTable.search(self.user.vendor == name)
        if not data:
            self.vendorTable.insert({'vendor': name, 'category': category})
    def addExpense(self, name, category, date, amount):
        self.addVendor(name, category)
        self.expenseTable.insert({'vendor': name, 'date': date, 'amount': amount})
    def __del__(self):
        self.db.close()

def testHelper():
    reference = read_csv('testData.csv', delimiter=';')
    database = ExpenseDatabase('databaseUnitTest.json')
    return reference, database

class TestExpenseDatabase(unittest.TestCase):
    def test_addVendor(self):
        reference, database = testHelper()
        for i, row in reference.iterrows():
            database.addVendor(row['Vendor'], row['Category'])
        aData = reference.Vendor.unique()
        tData = [row['vendor'] for row in database.vendorTable]
        self.assertCountEqual(tData, aData, "Vendor Addition Fails")
        database.db.drop_tables()
    def test_addExpense(self):
        reference, database = testHelper()
        for i, row in reference.iterrows():
            database.addExpense(row['Vendor'], row['Category'], row['Date'], row['Amount'])
        aData = reference.Amount.sum()
        tData = sum([row['amount'] for row in database.expenseTable])
        self.assertAlmostEqual(tData, aData, 2, "Expense Addition Fails")
        database.db.drop_tables()

if __name__ == "__main__":
    unittest.main()