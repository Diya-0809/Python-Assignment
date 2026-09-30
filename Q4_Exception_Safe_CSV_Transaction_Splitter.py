"""
Q4 - Exception-Safe CSV Transaction Splitter
Python 3.10+
"""
import csv
import re
from collections import defaultdict
from datetime import datetime

TIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

def validate(row):
    required = ["tid", "acc", "type", "amount", "time"]
    if any(key not in row for key in required):
        raise ValueError("missing column")

    if not row["tid"].strip():
        raise ValueError("empty transaction_id")
    if not row["acc"].strip():
        raise ValueError("empty account_id")

    kind = row["type"].strip().upper()
    if kind not in {"CREDIT", "DEBIT"}:
        raise ValueError("invalid type")

    try:
        amount = float(row["amount"])
    except (ValueError, TypeError):
        raise ValueError("amount is not numeric")

    if amount <= 0:
        raise ValueError("amount must be greater than zero")

    timestamp = row["time"].strip()
    if not TIME_RE.fullmatch(timestamp):
        raise ValueError("invalid timestamp format")
    try:
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise ValueError("invalid timestamp")

    return kind, amount

def main():
    path = input().strip()
    balances = defaultdict(float)

    with open(path, "r", newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header")

        headers = reader.fieldnames
        output_headers = list(headers)

        with open("credit.csv", "w", newline="", encoding="utf-8") as cf, \
             open("debit.csv", "w", newline="", encoding="utf-8") as df, \
             open("error.csv", "w", newline="", encoding="utf-8") as ef:

            credit_writer = csv.DictWriter(cf, fieldnames=output_headers)
            debit_writer = csv.DictWriter(df, fieldnames=output_headers)
            error_writer = csv.DictWriter(
                ef, fieldnames=output_headers + ["reason"]
            )
            credit_writer.writeheader()
            debit_writer.writeheader()
            error_writer.writeheader()

            for row in reader:
                try:
                    kind, amount = validate(row)
                    if kind == "CREDIT":
                        credit_writer.writerow(row)
                        balances[row["acc"]] += amount
                    else:
                        debit_writer.writerow(row)
                        balances[row["acc"]] -= amount
                except (ValueError, KeyError, TypeError) as exc:
                    error_row = dict(row)
                    error_row["reason"] = str(exc)
                    error_writer.writerow(error_row)

    for account, balance in sorted(
        balances.items(), key=lambda x: (-abs(x[1]), x[0])
    ):
        if balance.is_integer():
            print(account, int(balance))
        else:
            print(account, balance)

    print("Files created: credit.csv, debit.csv, error.csv")

if __name__ == "__main__":
    main()
