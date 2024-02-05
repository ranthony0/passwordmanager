from Validation import *
from Account import Account
from TwoFactorAccount import TwoFactorAccount
from AccountList import AccountList


class PasswordManagerUI:
    __account_lists = None

    def __init__(self):
        pass

    @classmethod
    def init(cls):
        cls.__account_lists = AccountList.get_account_lists()

    @staticmethod
    def print_menu():
        print()
        print("Choose an action:")
        print("   i: Print the list of accounts")
        print("   a: Add a new account list")
        print("   d: Delete an account list")
        print("   x: Exit the program")

    @classmethod
    def print_lists(cls):
        print("Account Lists:")
        for account_list in cls.__account_lists:
            print("    ", account_list.get_name())

    @classmethod
    def lookup_account_list(cls, name):
        for account_list in cls.__account_lists:
            if name.lower() == account_list.get_name().lower():
                return account_list
        return None

    @classmethod
    def add_account_list(cls):
        name = input_string(prompt="What is the name of the account list: ")
        account_list = cls.lookup_account_list(name)
        if account_list is not None:
            print("Error, already exists")
            return
        account_list = AccountList(name, [])
        cls.__account_lists.append(account_list)

    @classmethod
    def add_account(cls):
        website_name = input_string(prompt="What is the Website Name? ")
        login_url = input_string(prompt="What is the URL? ")
        user_name = input_string(prompt="What is your user name? ")
        password = input_string(prompt="What is the password? ")
        last_password_update = input_string(prompt="When was the last password updated? ")
        account = Account(website_name, login_url, user_name, password, last_password_update)

    @classmethod
    def delete_account_list(cls):
        name = select_item("PLease select an account list: ",
                           choices=[al.get_name() for al in PasswordManagerUI.__account_lists])
        for al in cls.__account_lists:
            if al.get_name() == name:
                cls.__account_lists.remove(al)

    @classmethod
    def run(cls):
        while True:
            cls.print_menu()
            choice = select_item("Select", choices=["i", "x", "d", "a"])
            if choice == "x":
                print("Goodbye!")
                break
            elif choice == "i":
                cls.print_lists()
            elif choice == "a":
                cls.add_account_list()
            elif choice == "d":
                cls.delete_account_list()

    def run(self):
        al1 = AccountList("TwoFactorAuthentication")
        al1.add(TwoFactorAccount)
        print(al1)
        al1.print_accounts()


if __name__ == "__main__":
    PasswordManagerUI.init()
    PasswordManagerUI.run()
