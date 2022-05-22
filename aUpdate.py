from sys import path
path.append('src')
from datetime import datetime
from tracker import ExpenseTracker
from helper import app_name, api_id, api_hash

def main():
    dbFileName = 'main.json'
    app = ExpenseTracker(dbFileName, app_name, api_id, api_hash)
    app.updateDatabase()
    app.sendStats(datetime.now().strftime('%Y-%m'))

if __name__ == "__main__":
    main()