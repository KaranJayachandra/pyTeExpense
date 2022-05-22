from sys import path
from datetime import datetime
path.insert(0, "./src")
from ..src.tracker import ExpenseTracker
from ..src.utils import app_name, api_id, api_hash

def main():
    dbFileName = 'main.json'
    app = ExpenseTracker(dbFileName, app_name, api_id, api_hash)
    app.updateDatabase()
    app.sendStats(datetime.now().strftime('%Y-%m'))

if __name__ == "__main__":
    main()