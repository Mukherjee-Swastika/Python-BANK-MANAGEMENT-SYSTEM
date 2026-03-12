import json
import random
import string
from pathlib import Path


class Bank:
    database = 'data.json'

    @classmethod
    def load_data(cls):
        if Path(cls.database).exists():
            with open(cls.database, 'r') as fs:
                return json.load(fs)
        return []

    @classmethod
    def save_data(cls, data):
        with open(cls.database, 'w') as fs:
            json.dump(data, fs, indent=4)

    @classmethod
    def generate_account_number(cls):
        data = cls.load_data()

        while True:
            chars = random.choices(string.ascii_letters, k=3) + \
                    random.choices(string.digits, k=3) + \
                    random.choices("!@#$%^&*", k=1)

            random.shuffle(chars)
            acc_no = ''.join(chars)

            # check duplicate account numbers
            if not any(user["accountNo."] == acc_no for user in data):
                return acc_no

    @classmethod
    def create_account(cls, name, age, email, pin):
        data = cls.load_data()

        if age < 18 or len(str(pin)) != 4:
            return None, "Age must be 18+ and PIN should be 4 digits"

        acc_no = cls.generate_account_number()

        user = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNo.": acc_no,
            "balance": 0
        }

        data.append(user)
        cls.save_data(data)

        return user, "Account created successfully"

    @classmethod
    def find_user(cls, acc_no, pin):
        data = cls.load_data()

        for user in data:
            if user['accountNo.'] == acc_no and user['pin'] == pin:
                return user

        return None

    @classmethod
    def deposit(cls, acc_no, pin, amount):
        data = cls.load_data()

        for user in data:
            if user['accountNo.'] == acc_no and user['pin'] == pin:

                if 0 < amount <= 10000:
                    user['balance'] += amount
                    cls.save_data(data)
                    return True, "Deposit successful"

                return False, "Amount must be between 1 and 10000"

        return False, "Invalid account or PIN"

    @classmethod
    def withdraw(cls, acc_no, pin, amount):
        data = cls.load_data()

        for user in data:
            if user['accountNo.'] == acc_no and user['pin'] == pin:

                if user['balance'] >= amount:
                    user['balance'] -= amount
                    cls.save_data(data)
                    return True, "Withdrawal successful"

                return False, "Insufficient balance"

        return False, "Invalid account or PIN"

    @classmethod
    def update_user(cls, acc_no, pin, name=None, email=None, new_pin=None):
        data = cls.load_data()

        for user in data:
            if user['accountNo.'] == acc_no and user['pin'] == pin:

                user['name'] = name or user['name']
                user['email'] = email or user['email']

                if new_pin:
                    user['pin'] = int(new_pin)

                cls.save_data(data)

                return True, "User details updated"

        return False, "User not found"

    @classmethod
    def delete_user(cls, acc_no, pin):
        data = cls.load_data()

        for i, user in enumerate(data):
            if user['accountNo.'] == acc_no and user['pin'] == pin:

                data.pop(i)
                cls.save_data(data)

                return True, "Account deleted"

        return False, "Account not found"


# -------- Console Menu --------

if __name__ == "__main__":

    print("🏦 Bank Management System")

    while True:

        print("\n1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Show Account Details")
        print("5. Update User Info")
        print("6. Delete Account")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":

            name = input("Enter name: ")
            age = int(input("Enter age: "))
            email = input("Enter email: ")
            pin = int(input("Enter 4 digit PIN: "))

            user, msg = Bank.create_account(name, age, email, pin)
            print(msg)

            if user:
                print("Your Account Number:", user["accountNo."])

        elif choice == "2":

            acc = input("Account Number: ")
            pin = int(input("PIN: "))
            amt = int(input("Amount: "))

            success, msg = Bank.deposit(acc, pin, amt)
            print(msg)

        elif choice == "3":

            acc = input("Account Number: ")
            pin = int(input("PIN: "))
            amt = int(input("Amount: "))

            success, msg = Bank.withdraw(acc, pin, amt)
            print(msg)

        elif choice == "4":

            acc = input("Account Number: ")
            pin = int(input("PIN: "))

            user = Bank.find_user(acc, pin)

            if user:
                print("\nAccount Details")
                print("Name:", user["name"])
                print("Email:", user["email"])
                print("Balance:", user["balance"])
            else:
                print("User not found")

        elif choice == "5":

            acc = input("Account Number: ")
            pin = int(input("PIN: "))

            name = input("New Name (leave blank to skip): ")
            email = input("New Email (leave blank to skip): ")
            new_pin = input("New PIN (leave blank to skip): ")

            success, msg = Bank.update_user(acc, pin, name or None, email or None, new_pin or None)
            print(msg)

        elif choice == "6":

            acc = input("Account Number: ")
            pin = int(input("PIN: "))

            success, msg = Bank.delete_user(acc, pin)
            print(msg)

        elif choice == "7":

            print("Thank you for using the bank system.")
            break

        else:
            print("Invalid choice")