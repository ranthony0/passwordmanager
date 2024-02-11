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
        print("   i: Print the list of account lists")
        print("   p: Print the contents of an account list")
        print("   a: Add a new account list")
        print("   n: Make a new account and add them to a list")
        print("   d: Delete an account list")
        print("   r: Remove an account from a list")
        print("   u: Update account")
        print("   j: Join two lists together")
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
        name = select_item("PLease select an account list: ", "Must be the name of an account list",
                           choices=[al.get_name() for al in PasswordManagerUI.__account_lists] + ["skip"])
        if name != "skip":
            for al in cls.__account_lists:
                if al.get_name() == name:
                    cls.__account_lists.remove(al)

    @classmethod
    def print_list(cls):
        name = select_item("PLease select an account list: ", "Must be the name of an account list",
                           choices=[al.get_name() for al in PasswordManagerUI.__account_lists] + ["skip"])
        if name != "skip":
            for al in cls.__account_lists:
                if al.get_name() == name:
                    PasswordManagerUI.print_account_list(al)

    @classmethod
    def make_or_find_account(cls):
        website_name = input_string("What is the account website name: ")
        login_url = input_string("What is the login URL: ")
        account = cls.__all_accounts.search(website_name, login_url)
        if account is not None:
            add_it = y_or_n("There is already an account with that Website. Do you want to add to the list (Y/N)? ")
            if add_it:
                return account
            else:
                return None
        else:
            user_name = input_string("What is the account username: ")
            password = input_string("What is the account password: ")
            last_password_update = input_string("When was the password last updated: ")
            if y_or_n("Is the account a Two factor account (Y/N)? "):
                type = input_string("What is the type of authentication: ")
                info = input_string("What is the information required: ")
                account = TwoFactorAccount(website_name, login_url, user_name, password, last_password_update, type, info)
            else:
                account = Account(website_name, login_url, user_name, password, last_password_update)
            cls.__all_accounts.add(account)
            return account

    @classmethod
    def update_account(cls):
        account = cls.find_account(cls.__all_accounts)
        if account is not None:
            website_name = input_string("What is the account website name: ", valid=lambda x: True)
            account.set_website_name(website_name)

    @classmethod
    def select_account_list(cls):
        name = select_item("PLease select an account list: ", "Must be the name of an account list",
                            choices=[al.get_name() for al in cls.__account_lists] + ["skip"])
        if name != "skip":
            for al in cls.__account_lists:
                if al.get_name() == name:
                    return al
            return None
        else:
            return None

    @classmethod
    def join_lists(cls):
        list1 = PasswordManagerUI.select_account_list()
        if list1 is not None:
            list2 = PasswordManagerUI.select_account_list()
            if list2 is not None:
                new_list = list1 + list2
                PasswordManagerUI.__account_lists.append(new_list)
        #list1 = select_item("PLease select an account list: ", "Must be the name of an account list",
        #                   choices=[al.get_name() for al in cls.__account_lists] + ["skip"])
        #if list1 != "skip":
        #    for al in cls.__account_lists:
         #       if al.get_name() == name:
          #          pass

    @staticmethod
    def find_account(al):
        print("Accounts: ")
        for item in al:
            print(F"    {item.get_website_name()} {item.get_login_url()}")


        account_name = select_item("Please select an account: ", "Must be the name of an account: ",
                                   choices=[F"{item.get_website_name()} {item.get_login_url()}" for item in al] + ["skip"])
        if account_name == "skip":
            return None
        else:
            for account in al:
                if account_name == F"{account.get_website_name()} {account.get_login_url()}":
                    return account
            return None

    @classmethod
    def new_account(cls):
        al = PasswordManagerUI.select_account_list()
            #select_item("PLease select an account list: ", "Must be the name of an account list",
             #              choices=[al.get_name() for al in PasswordManagerUI.__account_lists] + ["skip"]))
        if al is not None:
            #for al in cls.__account_lists:
             #   if al.get_name() == name:
            account = PasswordManagerUI.make_or_find_account()
            if account is not None and account not in al:
                al.add(account)

    @classmethod
    def remove_account_from_list(cls):
        al = PasswordManagerUI.select_account_list()
            #select_item("PLease select an account list: ", "Must be the name of an account list",
             #              choices=[al.get_name() for al in PasswordManagerUI.__account_lists] + ["skip"]))
        if al is not None:
 #           for al in cls.__account_lists:
  #              if al.get_name() == name:
            account = PasswordManagerUI.find_account(al)
            if account is not None and account in al:
                al.remove(account)


    @classmethod
    def run(cls):
        cls.__all_accounts, cls.__account_lists = AccountList.get_account_lists()
        while True:
            cls.print_menu()
            choice = select_item("Select: ", choices=["i", "x", "d", "a", "p", "n", "r", "j", "u"])
            if choice == "x":
                print("Goodbye!")
                break
            elif choice == "i":
                cls.print_lists()
            elif choice == "p":
                cls.print_list()
            elif choice == "a":
                cls.add_account_list()
            elif choice == "n":
                cls.new_account()
            elif choice == "d":
                cls.delete_account_list()
            elif choice == "r":
                cls.remove_account_from_list()
            elif choice == "u":
                cls.update_account
            elif choice == "j":
                cls.join_lists()

    @staticmethod
    def print_account_list(account_list):
        print(account_list.get_name(), ":", sep="")
        for account in account_list:
            print("  ", account)

    @classmethod
    def read_account_lists(cls):
        all = AccountList("All Accounts")
        cls.__all_accounts = all
        account = TwoFactorAccount(website_name, login_url, user_name, password, last_password_update, type, info)
        for account in Account:
            account.add(Account)
        lists = [all, Account]



if __name__ == "__main__":
    PasswordManagerUI.init()
    PasswordManagerUI.run()
