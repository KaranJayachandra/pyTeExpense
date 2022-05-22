from unittest import TestCase, main
from telethon import TelegramClient
from asyncio import get_event_loop
from helper import budgets, testData, app_name, api_id, api_hash

class Client:
    def __init__(self, app_name, api_id, api_hash):
        self.client = TelegramClient(app_name, api_id, api_hash)
        loop = get_event_loop()
        task = loop.create_task(self.client.connect())
        loop.run_until_complete(task)
        self.client.start()
    def sendMessage(self, messageText):
        loop = get_event_loop()
        task = loop.create_task(self.client.send_message('me', messageText))
        loop.run_until_complete(task)
    def getMessages(self, nMessage):
        validBudgetItems = [key for key, value in budgets.items()]
        releventMessages = []
        parsedData = []
        for message in self.client.iter_messages('me', limit=nMessage):
            if isinstance(message.message, str):
                if 'EA:' in message.message:
                    data = message.message.replace('EA:', '').split(',')
                    data = [item.strip() for item in data]
                    if len(data) == 3:
                        iVendor = data[0]
                        iCategory = data[1]
                        iAmount = data[2]
                        if isinstance(iVendor, str) and len(iVendor) > 0:
                            if iCategory.upper() in validBudgetItems:
                                try:
                                    iAmount = float(iAmount)
                                    releventMessages.append(message.id)
                                    iDate = message.date.strftime('%Y-%m-%d')
                                    parsedData.append({'vendor': iVendor, 'category': iCategory, 'date': iDate, 'amount': iAmount})
                                except:
                                    continue
                                    
                elif 'ET:' in message.message:
                    releventMessages.append(message.id)
        loop = get_event_loop()
        task = loop.create_task(self.client.delete_messages('me', message_ids=releventMessages))
        loop.run_until_complete(task)
        self.sendMessage('`ET: Captured ' + str(len(parsedData)) + '`')
        return parsedData

class TestClient(TestCase):
    def test_getMessages(self):
        client = Client(app_name, api_id, api_hash)
        for item in testData:
            text = 'EA: ' + item['vendor'] + ', ' + item['category'] + ', ' + str(item['amount'])
            client.sendMessage(text)
        parsedData = client.getMessages(100)
        client.client.disconnect()
        self.assertEqual(len(testData), len(parsedData), 'Extracting Expenses Fails')
        self.assertCountEqual(testData, parsedData, 'Parsing Text Fails')

if __name__ == "__main__":
    main()