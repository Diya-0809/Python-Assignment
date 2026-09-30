"""
Q5 - Object-Oriented Bank Settlement System
Python 3.10+
"""
from dataclasses import dataclass
from copy import deepcopy

class BankError(Exception):
    pass

class AccountNotFoundError(BankError):
    pass

class InvalidAmountError(BankError):
    pass

class InsufficientFundsError(BankError):
    pass

@dataclass(frozen=True)
class Transaction:
    kind: str
    source: str
    target: str | None
    amount: int | float

class Account:
    def __init__(self, account_id, balance=0):
        self._account_id = account_id
        self._balance = balance

    @property
    def account_id(self):
        return self._account_id

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive.")
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive.")
        if amount > self._balance:
            raise InsufficientFundsError("Insufficient funds.")
        self._balance -= amount

    # Internal rollback support.
    def _restore(self, balance):
        self._balance = balance

class Bank:
    def __init__(self):
        self.accounts = {}
        self.history = []
        self._batch = None
        self.failed_batches = []

    def add_account(self, account_id, balance):
        if account_id in self.accounts:
            raise BankError("Duplicate account.")
        if balance < 0:
            raise InvalidAmountError("Initial balance cannot be negative.")
        self.accounts[account_id] = Account(account_id, balance)

    def _account(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFoundError(f"Unknown account: {account_id}")
        return self.accounts[account_id]

    def _touch(self, account_id):
        if self._batch is not None and account_id not in self._batch["snapshot"]:
            self._batch["snapshot"][account_id] = self._account(account_id).balance

    def deposit(self, account_id, amount):
        self._touch(account_id)
        self._account(account_id).deposit(amount)
        self.history.append(Transaction("DEPOSIT", account_id, None, amount))

    def withdraw(self, account_id, amount):
        self._touch(account_id)
        self._account(account_id).withdraw(amount)
        self.history.append(Transaction("WITHDRAW", account_id, None, amount))

    def transfer(self, source, target, amount):
        self._touch(source)
        self._touch(target)
        src = self._account(source)
        dst = self._account(target)
        src.withdraw(amount)
        try:
            dst.deposit(amount)
        except Exception:
            src.deposit(amount)  # local atomic rollback
            raise
        self.history.append(Transaction("TRANSFER", source, target, amount))

    def begin_batch(self):
        if self._batch is not None:
            raise BankError("Nested batches are not supported.")
        self._batch = {"snapshot": {}, "history_len": len(self.history)}

    def end_batch(self, batch_number):
        if self._batch is None:
            raise BankError("BATCH_END without BATCH_BEGIN.")
        self._batch = None

    def rollback_batch(self, batch_number):
        if self._batch is None:
            return
        snapshot = self._batch["snapshot"]
        for account_id, old_balance in snapshot.items():
            self.accounts[account_id]._restore(old_balance)
        del self.history[self._batch["history_len"]:]
        self._batch = None
        self.failed_batches.append(batch_number)

def main():
    bank = Bank()

    n = int(input().strip())
    if n < 1:
        raise ValueError("At least one account is required.")

    for _ in range(n):
        acc, balance = input().split()
        bank.add_account(acc, int(balance))

    q = int(input().strip())
    batch_no = 0
    active_batch_no = None
    skipping_failed_batch = False

    for _ in range(q):
        parts = input().split()
        if not parts:
            continue

        try:
            op = parts[0]

            # Once a batch fails, ignore its remaining operations until BATCH_END.
            if skipping_failed_batch:
                if op == "BATCH_END" and len(parts) == 1:
                    skipping_failed_batch = False
                    active_batch_no = None
                continue

            if op == "DEPOSIT" and len(parts) == 3:
                bank.deposit(parts[1], int(parts[2]))
            elif op == "WITHDRAW" and len(parts) == 3:
                bank.withdraw(parts[1], int(parts[2]))
            elif op == "TRANSFER" and len(parts) == 4:
                bank.transfer(parts[1], parts[2], int(parts[3]))
            elif op == "BATCH_BEGIN" and len(parts) == 1:
                batch_no += 1
                active_batch_no = batch_no
                bank.begin_batch()
            elif op == "BATCH_END" and len(parts) == 1:
                bank.end_batch(active_batch_no)
                active_batch_no = None
            else:
                raise BankError("Invalid operation.")

        except (BankError, ValueError):
            # A failed transaction inside a batch rolls back the whole batch.
            if active_batch_no is not None:
                bank.rollback_batch(active_batch_no)
                skipping_failed_batch = True

    if active_batch_no is not None:
        bank.rollback_batch(active_batch_no)

    for number in bank.failed_batches:
        print("FAILED", number)

    for account_id in sorted(bank.accounts):
        print(account_id, bank.accounts[account_id].balance)

if __name__ == "__main__":
    main()
