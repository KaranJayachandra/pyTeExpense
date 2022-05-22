# pyTeExpense

This application is used to note expenses using text messages stored in the popular messaging app [Telegram](https://telegram.org/). The dependencies for the application are shown in requirements and can be installed using:

To use this application you will need a telegram application id and hash. This can be procured [here](https://my.telegram.org/auth?to=apps), from the developers section of the Telegram website.

```
git clone https://github.com/KaranJayachandra/pyTeExpense.git
pip install -r requirements.txt
```

Edit `helper.py` in src with the details you received from the Telegram application API. You can now start the application by creating an empty json file and configure the application with the same name in `aUpdate.py`.

Create crontab on a linux server for periodic update of the database. Edit your crontab and place:

```
15 * * * * python path\to\aLoad.py
```

Now run aLoad.py locally once to start a Telegram session. Subsequent sessions will use the same login credentials.