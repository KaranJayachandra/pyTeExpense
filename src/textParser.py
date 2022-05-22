from unittest import TestCase
from unittest import TestCase, main
from numpy import asarray, cumsum, round
from math import ceil

class GraphGenerator:
    def getOverall(self, data, totalBudget):
        outputWidth = 20
        dailyExpense = asarray(list(data.values()))
        totalExpense = round(cumsum(dailyExpense), 2)
        plotText = '`ET: Daily Expenses\n'
        plotText += '------------------\n'
        for iDay in range(len(totalExpense)):
            plotText += str(iDay).zfill(2)
            dataPercent = int(round(totalExpense[iDay] * 100 / totalBudget))
            plotText += ' [' + str(int(dailyExpense[iDay])).rjust(3) + '€ ('
            plotText += str(dataPercent).rjust(3) + ' %)] |'
            bar = (totalExpense[iDay] * outputWidth) / totalBudget
            for iData in range(outputWidth):
                if iData < ceil(bar):
                    plotText += 'o'
                else:
                    plotText += '.'
            plotText += '|\n'
        return plotText + '`'
    def getCategory(self, data, budgets):
        outputWidth = 11
        textWidth = len(max(list(data.keys()), key=len))
        valueWidth = len(max([str(value) for key, value in data.items()], key=len))
        plotText = '`ET: Category Expenses\n'
        plotText += '---------------------\n'
        for iCategory, iValue in data.items():
            plotText += iCategory.rjust(textWidth)
            dataPercent = int(round(iValue * 100 / budgets[iCategory.upper()]))
            plotText += ' [ ' + str(int(iValue)).rjust(3) + '€ (' + str(dataPercent).rjust(3) + ' %)] |'
            bar = (iValue * outputWidth) / budgets[iCategory.upper()]
            for iData in range(outputWidth):
                if iData < ceil(bar):
                    plotText += 'o'
                else:
                    plotText += '.'
            plotText += '|\n'
        return plotText + '`'

class TestGraphGenerator(TestCase):
    def test_getOverall(self):
        graphing = GraphGenerator()
        data = {i : i for i in range(1, 11)}
        plotText = graphing.getOverall(data, 300)
        print(plotText)

    def test_getCategory(self):
        graphing = GraphGenerator()
        data = {"Housing": 800, "Loan": 700, "Groceries": 150, "Luxury": 100}
        budgets = {"HOUSING": 900, "LOAN": 800, "GROCERIES": 100, "LUXURY": 150}
        plotText = graphing.getCategory(data, budgets)
        print(plotText)

if __name__ == "__main__":
    main()