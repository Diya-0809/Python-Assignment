"""
Q5 - Object-Oriented Bank Settlement System
"""
class Bank:
    def __init__(self):
        self._accounts = {}
        self._history = []

        # None = no active batch
        self._batch = None

        self._batch_number = 0
        self._failed_batches = []

    def add_account(self, account_id, balance):
        self._accounts[account_id] = Account(account_id, balance)

    def get_account(self, account_id):
        if account_id not in self._accounts:
            raise AccountNotFound(f"Account {account_id} does not exist")

        return self._accounts[account_id]

    def deposit(self, account_id, amount):
        account = self.get_account(account_id)
        account.deposit(amount)
        self._history.append(("DEPOSIT", account_id, amount))

    def withdraw(self, account_id, amount):
        account = self.get_account(account_id)
        account.withdraw(amount)
        self._history.append(("WITHDRAW", account_id, amount))

    def transfer(self, from_id, to_id, amount):
        if amount <= 0:
            raise InvalidAmount("Amount must be positive")

        source = self.get_account(from_id)
        destination = self.get_account(to_id)

        if amount > source.balance:
            raise InsufficientBalance()

        source.withdraw(amount)
        destination.deposit(amount)

        self._history.append(
            ("TRANSFER", from_id, to_id, amount)
        )

    def begin_batch(self):
        if self._batch is not None:
            raise BankException("Nested batches are not supported")

        self._batch = []

    def add_to_batch(self, transaction):
        if self._batch is None:
            raise BankException("No active batch")

        self._batch.append(transaction)

    def execute_batch(self):
        if self._batch is None:
            raise BankException("No active batch")

        self._batch_number += 1
        batch_number = self._batch_number

        # Save balances before the batch.
        snapshots = {}

        try:
            for transaction in self._batch:

                if transaction.operation == "DEPOSIT":
                    acc, _ = transaction.args
                    snapshots.setdefault(
                        acc,
                        self.get_account(acc).balance
                    )

                elif transaction.operation == "WITHDRAW":
                    acc, _ = transaction.args
                    snapshots.setdefault(
                        acc,
                        self.get_account(acc).balance
                    )

                elif transaction.operation == "TRANSFER":
                    source, destination, _ = transaction.args

                    snapshots.setdefault(
                        source,
                        self.get_account(source).balance
                    )

                    snapshots.setdefault(
                        destination,
                        self.get_account(destination).balance
                    )

                transaction.execute(self)

        except BankException:
            # Roll back every account modified by the batch.
            for acc, old_balance in snapshots.items():
                self._accounts[acc]._balance = old_balance

            self._failed_batches.append(batch_number)

        finally:
            self._batch = None
