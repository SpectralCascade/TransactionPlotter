import datetime as dt
import csv
import matplotlib.pyplot as graph
import os
import sys

def ImportTransactionData(paths):
    dates = []
    balances = []
    transactions = []
    for path in paths:
        with open(path) as file:
            line = 0
            rdr = csv.reader(file)
            lastDate = ""
            for row in rdr:
                line += 1
                if line < 2 or len(row) < 1:
                    continue
                if lastDate == row[0]:
                    transactions[-1] += float(row[3])
                    balances[-1] = float(row[4])
                else:
                    dates.append(dt.datetime.strptime(row[0], "%d %b %Y"))
                    transactions.append(float(row[3]))
                    balances.append(float(row[4]))
                lastDate = row[0]
    return dates, transactions, balances

def get_csv_files_from_directory(directory):
    csv_files = []
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            csv_files.append(os.path.join(directory, file))
    return csv_files

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("No path provided, must provide a directory or file path to CSV with bank statement data.")

        input_path = sys.argv[1]
        if os.path.isfile(input_path):
            data = ImportTransactionData([input_path])
        elif os.path.isdir(input_path):
            csv_files = get_csv_files_from_directory(input_path)
            if not csv_files:
                raise ValueError("No CSV data found in the provided directory.")
            data = ImportTransactionData(csv_files)
        else:
            raise ValueError("Invalid file or directory path.")

        # Plot transactions over time
        graph.plot(data[0], data[1], "-")
        # Plot balance over time
        graph.plot(data[0], data[2], "-")

        graph.xlabel("Time [days]")
        graph.ylabel("Money [£]")
        graph.legend(["Net Transactions", "Balance"], loc='upper left')
        graph.show()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)