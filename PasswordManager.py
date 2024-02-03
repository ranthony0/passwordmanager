from Validation import *
from Account import Account
from TwoFactorAccount import TwoFactorAccount

class PasswordManagerUI:
    all_passwords = None

    def __init__(self):
        pass


    @staticmethod
    def print_menu():
        print()
        print("Choose an action:")
        print("   i: Print the list of accounts")
        print("   a: Add a new account")
        print("   d: Delete an account")
        print("   x: Exit the program")

    @staticmethod
    def print_lists():
        print("Account Lists:")
        for Account in PasswordManagerUI.__account_lists:
            print("    ", Account.get_name())

    @staticmethod
    def add_account_list():
        name = input_string(prompt="What is the name of the account list: ")
        PasswordManagerUI__account_lists.append(Account(name))

    @staticmethod
    def delete_account_list():
        name = select_item(items=[al.get_name() for al in PasswordManagerUI.__account_lists])
        for al in PasswordManagerUI.__account_lists:
            if al.get_name() == name:
                PasswordManagerUI.__account_lists.remove(al)
    def run(self):
        PasswordManagerUI.__account_lists = PasswordManagerUI.read_account_lists()
        while True:
            self.print_menu()
            choice = select_item("Select", items=["i", "x", "a", "d"])
            if choice == "x":
                print("Goodbye!")
                break
            elif choice == "i":
                self.print_lists()
            elif choice == "a":
                self.add_account_list()
            elif choice == "d":
                self.delete_account_list()


if __name__ == "__main__":
    app = PasswordManagerUI()
    app.run()


