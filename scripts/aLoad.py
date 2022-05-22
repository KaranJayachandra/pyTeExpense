from sys import path
from pandas import read_csv
from datetime import datetime
path.insert(0, "./src")
from tracker import ExpenseTracker
from utils import app_name, api_id, api_hash

def main():
    testDataFile = './data/testData.csv'
    dbFileName = 'main.json'
    app = ExpenseTracker(dbFileName, app_name, api_id, api_hash)
    reference = read_csv(testDataFile, delimiter=';')
    expenses = []
    for i, row in reference.iterrows():
        iDate = datetime.strptime(row['Date'], '%d-%m-%Y')
        row['Date'] = iDate.strftime('%Y-%m-%d')
        expenses.append({'vendor': row['Vendor'], 'category': row['Category'], 
                            'date': row['Date'], 'amount': row['Amount']})
    app.db.addExpenses(expenses)
    app.sendStats(datetime.now().strftime('%Y-%m'))

if __name__ == "__main__":
    main()