from datetime import datetime

app_name = '<app_name>'
api_id = '<app_id>'
api_hash = '<app_hash>'
budgets =  {'HOUSING': 700.0, 
            'LOAN': 750.0,
            'SAVINGS': 500.0,
            'GROCERIES' : 150.0,
            'INSURANCE' : 150.0,
            'TRANSPORT' : 450.0,
            'TECHNOLOGY' : 50.0,
            'CLOTHING' : 50.0,
            'SOCIAL' : 100.0,
            'LUXURY' : 100.0}

testData = [{'vendor': 'AH2Go', 'category': 'Luxury', 'date': datetime.now().strftime('%Y-%m-%d'), 'amount': 20.0},
            {'vendor': 'Rent', 'category': 'Housing', 'date': datetime.now().strftime('%Y-%m-%d'), 'amount': 100.0},
            {'vendor': 'Albert Heijn', 'category': 'Groceries', 'date': datetime.now().strftime('%Y-%m-%d'), 'amount': 10.0}]