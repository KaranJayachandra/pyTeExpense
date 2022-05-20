# Python - Telethon Expense Tracker

Software Requirements: python, telethon, gnuplotlib
Hardware Requirements: Small Server to run a crontab

## Background

I was using an excel spread sheet to perform calculations of my personal expenses throughout the month. The flow of the calculation was quite simple. It takes four fields as input:
- Date
- Vendor
- Category
- Amount

The expenses were grouped by the category every month and checked against a budget that was also defined per month. In addition to this, it was allowed to exchange budgets from one category to the other every month as long as the total remained the same. Filling these spreadsheets though required a PC and also repetive entries for the Date and Vendor's Category.

## Vision

I would like to create a Telegram application that periodically checks my saved messages and picks up messages tagged as expenses using a prefix eg. 'ET:'. The messages should be of three categories:
- Add Expense
- Edit Expense
- Set Budget
- Edit Budget

After the periodical check, the application should provide the following information to the user:
- Total Budget vs. Expenses (Line Graph)
- Expenses vs. Budget by Category
- Line Items of all Expenses for Specific Month (Add a tagged message as a request)

## Testing

I can use the information I collected last month and the current month and store in the a database to use as test vectors for the program.

## Release Schedule
- Release 0.0: Load the data from the excel sheet into a simple database
- Release 0.1: Check for expenses (in correct format) and list all the expenses
- Release 0.2: Report the expense vs. budget in text form
- Release 0.3: Report the expense vs. budget using gnuplotlib
- Release 0.4: Register Vendors and allow expenses for those only
- Release 0.5: Edit expense via request
- Release 0.5: Set and edit budget via message