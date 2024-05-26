import os
import random

# Account base class
class Account:
    def __init__(self, account_holder, account_number, password, balance, account_type):
        self.account_holder = account_holder
        self.account_number = account_number
        self.password = password
        self.balance = balance
        self.account_type = account_type
        self.transaction_history = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited: Nu.{amount}")
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew: Nu.{amount}")
            return True
        return False

    def check_balance(self):
        return self.balance

    def change_password(self, new_password):
        self.password = new_password

    def view_details(self):
        return (f"Account Holder: {self.account_holder}\n"
                f"Account Number: {self.account_number}\n"
                f"Account Type: {self.account_type}\n"
                f"Balance: Nu.{self.balance}")

    def view_transaction_history(self):
        if not self.transaction_history:
            return "No transactions yet."
        return "\n".join(self.transaction_history)

    def change_account_holder_name(self, new_name):
        self.account_holder = new_name

class BusinessAccount(Account):
    def __init__(self, account_holder, account_number, password, balance):
        super().__init__(account_holder, account_number, password, balance, "Business")

class PersonalAccount(Account):
    def __init__(self, account_holder, account_number, password, balance):
        super().__init__(account_holder, account_number, password, balance, "Personal")

class Bank:
    def __init__(self):
        self.accounts = {}
        self.load_accounts()

    def load_accounts(self):
        if os.path.exists("accounts.txt"):
            with open("accounts.txt", "r") as file:
                while True:
                    account_holder_line = file.readline().strip()
                    if not account_holder_line:
                        break
                    account_number_line = file.readline().strip()
                    password_line = file.readline().strip()
                    account_type_line = file.readline().strip()
                    balance_line = file.readline().strip()
                    file.readline()

                    try:
                        account_holder = account_holder_line.split(": ")[1]
                        account_number = account_number_line.split(": ")[1]
                        password = password_line.split(": ")[1]
                        account_type = account_type_line.split(": ")[1]
                        balance = float(balance_line.split(": ")[1])
                    except IndexError:
                        print("Error reading account information. Skipping entry.")
                        continue

                    if account_type == "Business":
                        self.accounts[account_number] = BusinessAccount(account_holder, account_number, password, balance)
                    else:
                        self.accounts[account_number] = PersonalAccount(account_holder, account_number, password, balance)

    def save_accounts(self):
        with open("accounts.txt", "w") as file:
            for account in self.accounts.values():
                file.write(f"Account Holder: {account.account_holder}\n")
                file.write(f"Account Number: {account.account_number}\n")
                file.write(f"Password: {account.password}\n")
                file.write(f"Account Type: {account.account_type}\n")
                file.write(f"Balance: {account.balance}\n")
                file.write(f"Transactions: {';'.join(account.transaction_history)}\n\n")

    def create_account(self, account_type):
        account_holder = input("Enter your name: ")
        account_number = str(random.randint(100000000, 999999999))
        password = str(random.randint(1000, 9999))
        if account_type.lower() in ["business", "b"]:
            account = BusinessAccount(account_holder, account_number, password, 0.0)
        else:
            account = PersonalAccount(account_holder, account_number, password, 0.0)
        self.accounts[account_number] = account
        self.save_accounts()
        return account_number, password

    def login(self, account_number, password):
        if account_number in self.accounts and self.accounts[account_number].password == password:
            return self.accounts[account_number]
        return None

    def transfer_money(self, from_account, to_account_number, amount):
        if to_account_number in self.accounts:
            confirm_password = input("Enter your password to confirm the transfer: ")
            if confirm_password == from_account.password:
                if from_account.withdraw(amount):
                    self.accounts[to_account_number].deposit(amount)
                    from_account.transaction_history.append(f"Transferred: Nu.{amount} to {to_account_number}")
                    self.accounts[to_account_number].transaction_history.append(f"Received: Nu.{amount} from {from_account.account_number}")
                    self.save_accounts()
                    return True
            else:
                print("Invalid password! Transfer failed.")
        return False

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            self.save_accounts()
            return True
        return False

    def view_all_accounts(self):
        if not self.accounts:
            return "No accounts found."
        details = [account.view_details() for account in self.accounts.values()]
        return "\n\n".join(details)

def main():
    bank = Bank()
    while True:
        print("\nWelcome to the CST Bank")
        print("1. Open Account")
        print("2. Login")
        print("3. Exit")
        main_menu_option = input("Choose an option: ")

        if main_menu_option == '1':
            account_type = input("Enter account type (Business/Personal): ")
            account_number, password = bank.create_account(account_type)
            print(f"Account created successfully!\nAccount Number: {account_number}\nPassword: {password}")

        elif main_menu_option == '2':
            account_number = input("Enter your account number: ")
            password = input("Enter your password: ")
            account = bank.login(account_number, password)
            if account:
                print("Login successful!")
                while True:
                    print(f"\nWelcome to your account, {account.account_holder}")
                    print("1. Check Balance")
                    print("2. Deposit Money")
                    print("3. Withdraw Money")
                    print("4. Transfer Money")
                    print("5. Change Password")
                    print("6. View Account Details")
                    print("7. View Transaction History")
                    print("8. Change Account Holder's Name")
                    print("9. Delete Account")
                    print("10. Logout")
                    account_menu_option = input("Choose an option: ")

                    if account_menu_option == '1':
                        print(f"Your balance is: Nu.{account.check_balance()}")

                    elif account_menu_option == '2':
                        amount = float(input("Enter amount to deposit: "))
                        if account.deposit(amount):
                            bank.save_accounts()
                            print(f"Nu.{amount} deposited successfully.")
                        else:
                            print("Invalid deposit amount.")

                    elif account_menu_option == '3':
                        amount = float(input("Enter amount to withdraw: "))
                        if account.withdraw(amount):
                            bank.save_accounts()
                            print(f"Nu.{amount} withdrawn successfully.")
                        else:
                            print("Insufficient funds.")

                    elif account_menu_option == '4':
                        to_account_number = input("Enter recipient account number: ")
                        amount = float(input("Enter amount to transfer: "))
                        if bank.transfer_money(account, to_account_number, amount):
                            print(f"Nu.{amount} transferred successfully.")
                        else:
                            print("Transfer failed! Check account details or balance.")

                    elif account_menu_option == '5':
                        new_password = input("Enter new password: ")
                        account.change_password(new_password)
                        bank.save_accounts()
                        print("Password changed successfully.")

                    elif account_menu_option == '6':
                        print("\nAccount Details:")
                        print(account.view_details())

                    elif account_menu_option == '7':
                        print("\nTransaction History:")
                        print(account.view_transaction_history())

                    elif account_menu_option == '8':
                        new_name = input("Enter new account holder's name: ")
                        account.change_account_holder_name(new_name)
                        bank.save_accounts()
                        print("Account holder's name changed successfully.")

                    elif account_menu_option == '9':
                        confirm = input("Are you sure you want to delete your account? (yes/no): ")
                        if confirm.lower() == 'yes':
                            if bank.delete_account(account.account_number):
                                print("Account deleted successfully.")
                                break
                            else:
                                print("Account deletion failed.")
                        else:
                            print("Account deletion canceled.")

                    elif account_menu_option == '10':
                        print("Logged out successfully.")
                        break

                    else:
                        print("Invalid option! Please choose again.")
            else:
                print("Invalid account number or password.")

        elif main_menu_option == '3':
            print("Thank you for using the CST Bank.")
            break

        else:
            print("Invalid option! Please choose again.")

if __name__ == "__main__":
    main()
