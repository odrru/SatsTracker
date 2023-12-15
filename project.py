import csv
import sys
import requests
import os
from datetime import datetime
import re

"""
SATStracker is a bitcoin value tracker. The user creates an account
in which the amount and value of their bitcoin is stored. The user
is able to log withdrawals and deposits, each time the program keeps track
of their account balance. This particular program makes it easier for
users who track Bitcoin's value in "Satoshis" or "Sats" (1 sat = 1/100000000 BTC)
to keep on top of their asset's value. The program also supports converting
the value of bitcoin to local currencies.
"""
# Constants used in mulitiple functions for better readability
dashes = 69
rates_database = "rates.csv"
accounts_database = "accounts.csv"
quit_message = "Thank you for using SATStracker. Enjoy your day ☀️"


# Class representing a user account
class Account:
    """
    A class representing a user account with methods for deposit, withdrawal,
    and updating account information.
    """

    def __init__(self, name, balance):
        """
        Initialize an Account instance with a name and balance.
        """
        self.name = name
        self.balance = balance

    @property
    def balance(self):
        """
        Get the balance property.
        """
        return self._balance

    @balance.setter
    def balance(self, balance):
        """
        Set the balance property.
        """
        self._balance = balance

    @property
    def name(self):
        """
        Get the name property.
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Set the name property.
        """
        self._name = name

    def deposit(self, n):
        """
        Deposit money into the account and update the balance.
        """
        if matches := re.search(r"^\d+$", n) and int(n) > 0:
            result, new_balance = self.update_amount(self.name, n)
            self.balance = new_balance
            return result
        else:
            raise ValueError

    def withdraw(self, n):
        """
        Withdraw money from the account and update the balance.
        """
        try:
            if matches := re.search(r"^\d+$", n) and int(self.balance) - int(n) >= 0:
                result, new_balance = self.update_amount(self.name, -int(n))
                self.balance = new_balance
                return result
            else:
                raise ValueError
        except ValueError:
            return f"{format(dashes)}\nNot enough balance in your account.\n"

    @classmethod
    def get(cls):
        """
        Class method to get an existing account or create a new one.
        """
        while True:
            if os.path.exists(accounts_database):
                i = 3
                while i > 0:
                    existing = input(
                        "\nEnter existing account name or type [N] to create new: "
                    ).upper()
                    if existing.upper() == "N":
                        return cls.append_new()
                    else:
                        with open(accounts_database, "r") as file:
                            reader = csv.reader(file)
                            for row in reader:
                                name, balance = row
                                total_accounts = []
                                total_accounts.append(name)
                                if name == existing:
                                    return cls(name, balance)
                                else:
                                    existing_accounts = []
                                    existing_accounts.append(name)

                            if len(existing_accounts) == len(total_accounts):
                                if i != 1:
                                    reply = [
                                        f"SATSTracker failed to find an existing account named '{existing}'.",
                                        f"\nType [N] to create a new one.\n{format(dashes)}\n",
                                    ]
                                    for line in reply:
                                        print(line)
                                i -= 1
                    if i == 0:
                        terminate()
            else:
                return cls.append_new()

    @classmethod
    def append_new(cls):
        """
        Class method to create a new account.
        """
        name = input("\nCreate new account name (e.g John Harvard): ").upper()
        while True:
            try:
                balance = input("Enter initial account balance: SATS ")
                if matches := re.search(r"^\d+$", balance):
                    account = [name, balance]

                    with open(accounts_database, "a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(account)

                    return cls(name, balance)
                else:
                    raise ValueError
            except ValueError:
                print(
                    f"{format(dashes)}\nInvalid Input. Please enter numbers only (e.g 1500)\n"
                )

    def update_amount(self, target_name, amount):
        """
        Update the amount in the account and write changes to the database.
        """
        target_name = self.name
        n = amount
        database = []

        with open(accounts_database, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == target_name:
                    row[1] = int(row[1]) + int(n)
                    new_balance = row[1]
                database.append(row)

        with open(accounts_database, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(database)

        return (
            f"\nSuccessfully updated your balance.\nNew account balance: SATS {new_balance:,}\n{format(dashes)}\n",
            new_balance,
        )


# Main function to run the program
def main():
    """
    Main function that runs the SATStracker program.
    """
    account = Account.get()
    while True:
        balance = float(account.balance)
        service = get_requested_service()
        if service == "X":
            sys.exit(f"{format(dashes)}\n{quit_message}\n")
        elif service == "0":
            print(f"\nBitcoin balance: SATS {balance:,.0f}\n{format(dashes)}\n")
            terminate()
        elif service == "1":
            try:
                result = account.deposit(input("\nDeposit amount: SATS "))
                print(f"{result}")
            except ValueError:
                print(
                    f"{format(dashes)}\nInvalid Input. Please enter positive numbers only (e.g 1500)\n"
                )
            terminate()
        elif service == "2":
            result = account.withdraw(input("\nWithdraw amount: SATS "))
            print(f"{result}")
            terminate()
        else:
            try:
                ticker, conversion = convert(balance)
                print(
                    f"\nYour SATS {balance:,.0f} balance is worth: {ticker} {conversion:,.0f}\n{format(dashes)}\n"
                )
            except requests.exceptions.RequestException:
                print(
                    f"\nProblem fetching exchange data. Check your internet connection.\n{format(dashes)}\n"
                )
            except KeyError:
                print(f"\nProblem with the ticker information entered. Please try again.\n{format(dashes)}\n")
            terminate()


# Function to convert Bitcoin balance to a local currency
def convert(balance):
    """
    Convert Bitcoin balance to a local currency.
    """
    ticker = input(f"\nEnter local currency ticker(e.g USD): ").upper()
    while True:
        if os.path.exists(rates_database):
            with open(rates_database, "r") as file:
                reader = csv.reader(file)
                header = next(reader, None)
                if header[1] != ticker or old(rates_database):
                    file.close()
                    os.remove(rates_database)
                else:
                    row = next(reader, None)
                    bitcoin_sats_price, local_currency_price = row
                    break

        else:
            try:
                SATS_TO_USD = 1 / 100000000
                btc_api = "insert api here"
                currency_api = "insert api here"
                bitcoin_exchange_data = (requests.get(btc_api)).json()
                local_currency_exchange_data = (requests.get(currency_api)).json()
                bitcoin_sats_price = (
                    bitcoin_exchange_data["bitcoin"]["usd"] * SATS_TO_USD
                )
                local_currency_price = local_currency_exchange_data["rates"][ticker]

                rates = [bitcoin_sats_price, local_currency_price]
                with open(rates_database, "w", newline="") as file:
                    writer = csv.writer(file)
                    header = ["sats", ticker]
                    writer.writerow(header)
                    writer.writerow(rates)
                break
            except requests.exceptions.RequestException:
                raise
            except KeyError:
                raise

    return ticker, balance * float(bitcoin_sats_price) * float(local_currency_price)


# Function to check if an existing file is old
def old(item):
    """
    Check if a file is older than 30 minutes.
    """
    item_birthday = datetime.fromtimestamp(os.path.getmtime(item))
    item_modified_age = datetime.now() - item_birthday
    item_modified_age_in_mins = round((item_modified_age.total_seconds()) / 60)

    return True if (item_modified_age_in_mins > 30) else False


# Function to get the user's requested service
def get_requested_service():
    """
    Get the user's requested service.
    """
    menu = [
        "\nSATStracker: TRACK YOUR BITCOIN BALANCE. BE ON TOP OF YOUR SATS",
        format(dashes),
        "Please choose a service:\n ",
        "[0] View account balance",
        "[1] Log a deposit to your account",
        "[2] Log a withdrawal from your account",
        "[3] Convert your bitcoin satoshis balance to a local currency",
        "[X] Quit\n",
    ]
    for line in menu:
        print(line)
    service = input().upper()

    return service


# Function to ask the user if they want to perform another transaction
def terminate():
    """
    Ask the user if they want to perform another transaction.
    """
    menu = [
        "\nWould you like to perform another transaction?",
        "[*] Yes (Press any key to continue)",
        "[X] No (Press X to quit)\n",
    ]
    for line in menu:
        print(line)

    if (input().upper()) == "X":
        sys.exit(f"{format(dashes)}\n{quit_message}\n")


# Function to format a line of dashes
def format(dashes):
    """
    Format a line of dashes
    for the program aesthetics.
    """
    return "-" * dashes


# Function to call main
if __name__ == "__main__":
    main()
