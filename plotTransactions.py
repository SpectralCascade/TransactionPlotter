import datetime as dt
import csv
import matplotlib.pyplot as graph
import matplotlib.dates as graphDates
import sys

def ImportTransactionData(path):
    dates = []
    balances = []
    transactions = []
    with open(path) as file:
        line = 0
        rdr = csv.reader(file)
        lastDate = ""
        for row in rdr:
            line += 1
            if (line < 4 or len(row) < 1):
                continue
            if (lastDate == row[0]):
                transactions[-1] += float(row[3])
                balances[-1] = float(row[4])
            else:
                dates.append(graphDates.date2num(dt.datetime.strptime(row[0], "%d/%m/%Y")))
                transactions.append(float(row[3]))
                balances.append(float(row[4]))
            lastDate = row[0]
    return (dates, transactions, balances)

if __name__ == "__main__":
    data = ImportTransactionData(sys.argv[1])

    # Plot transactions over time
    graph.plot_date(data[0], data[1], fmt="-")
    # Plot balance over time
    graph.plot_date(data[0], data[2], fmt="-")

    graph.xlabel("Time [days]")
    graph.ylabel("Money [£]")
    graph.legend(["Net Transactions", "Balance"], loc='upper left')
    graph.show()



