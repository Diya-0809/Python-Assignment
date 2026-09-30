"""
Q4 - Exception-Safe CSV Transaction Splitter
"""
import csv
import sys
from datetime import datetime
from collections import defaultdict

def validate_row(row, line_number):
    required_fields = ["tid", "acc", "type", "amount", "time"]

    # Check missing fields
    for field in required_fields:
        if field not in row or row[field].strip() == "":
            raise ValueError(f"Missing {field}")

    tid = row["tid"].strip()
    acc = row["acc"].strip()
    trans_type = row["type"].strip().upper()
    amount_text = row["amount"].strip()
    timestamp = row["time"].strip()

    # Validate transaction type
    if trans_type not in ("CREDIT", "DEBIT"):
        raise ValueError("Invalid transaction type")

    # Validate amount
    try:
        amount = float(amount_text)
    except ValueError:
        raise ValueError("Amount is not numeric")

    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    # Validate timestamp
    try:
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise ValueError("Invalid timestamp")

    return {
        "tid": tid,
        "acc": acc,
        "type": trans_type,
        "amount": amount,
        "time": timestamp
    }

def process_file(input_file):
    # Account -> net balance change
    balances = defaultdict(float)

    with open(input_file, "r", newline="", encoding="utf-8") as infile, \
         open("credit.csv", "w", newline="", encoding="utf-8") as credit_file, \
         open("debit.csv", "w", newline="", encoding="utf-8") as debit_file, \
         open("error.csv", "w", newline="", encoding="utf-8") as error_file:

        reader = csv.DictReader(infile)

        # Output writers
        output_fields = ["tid", "acc", "type", "amount", "time"]

        credit_writer = csv.DictWriter(
            credit_file,
            fieldnames=output_fields
        )

        debit_writer = csv.DictWriter(
            debit_file,
            fieldnames=output_fields
        )

        error_fields = output_fields + ["reason"]

        error_writer = csv.DictWriter(
            error_file,
            fieldnames=error_fields
        )

        # Write headers
        credit_writer.writeheader()
        debit_writer.writeheader()
        error_writer.writeheader()

        # Process every row independently
        for line_number, row in enumerate(reader, start=2):

            try:
                transaction = validate_row(row, line_number)

                # Valid CREDIT
                if transaction["type"] == "CREDIT":
                    credit_writer.writerow(transaction)
                    balances[transaction["acc"]] += transaction["amount"]

                # Valid DEBIT
                else:
                    debit_writer.writerow(transaction)
                    balances[transaction["acc"]] -= transaction["amount"]

            except Exception as e:
                # Preserve original row values
                error_row = {
                    "tid": row.get("tid", ""),
                    "acc": row.get("acc", ""),
                    "type": row.get("type", ""),
                    "amount": row.get("amount", ""),
                    "time": row.get("time", ""),
                    "reason": str(e)
                }

                error_writer.writerow(error_row)

    result = sorted(
        balances.items(),
        key=lambda x: (-abs(x[1]), x[0])
    )

    for account, balance in result:

        # Avoid displaying unnecessary .0 for integer values
        if balance.is_integer():
            balance = int(balance)

        print(account, balance)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python transaction_splitter.py <input_csv>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        process_file(input_file)

    except FileNotFoundError:
        print("ERROR: Input file not found")

    except PermissionError:
        print("ERROR: Permission denied")

    except Exception as e:
        print(f"ERROR: {e}")
