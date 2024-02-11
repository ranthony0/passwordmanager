from Account import Account
from TwoFactorAccount import TwoFactorAccount

class AccountList:
    __name = ""
    __accounts = []
    __map = {}
    ALL_ACCOUNTS_NAME = "All accounts"

    def __init__(self, name, accounts):
        self.__name = name
        self.__accounts = accounts
        self.__class__.__map[name.lower()] = self

    def __iter__(self):
        return iter(self.__accounts)

    def print_accounts(self):
        print(self.__accounts)

    def __str__(self):
        return F"{self.__name}: {self.__accounts}"

    def __contains__(self, item):
        return item in self.__accounts

    def add(self, account):
        self.__accounts.append(account)

    def __add__(self, other):
        name = self.get_name() + "/" + other.get_name()
        try:
            account_list = self.__class__.lookup(name)
            print(F"Account list {account_list.get_name()} already exists.")
            return None
        except KeyError:
            pass
        new_list = AccountList(name, [])
        for account in self:
            if account not in new_list:
                new_list.add(account)
        for account in other:
            if account not in new_list:
                new_list.add(account)
        return new_list

    def remove(self, account):
        self.__accounts.remove(account)

    def search(self, website_name, login_url):
        for account in self.__accounts:
            if account.get_website_name() == website_name and account.get_login_url() == login_url:
                return account
        return None

    def get_name(self):
        return self.__name

    @classmethod
    def get_account_lists(cls):
        hbo = Account("HBO", "hbomax.com", "ant", "xxx", "x")
        netflix = TwoFactorAccount("Netflix", "Netflix.com", "ant", "xxx", "x", "pin", "1234")
        pcc = TwoFactorAccount("pcc", "mypcc.edu", "ant.ros", "xxx", "x", "phone", "ms authenticator")

        all_accounts = AccountList(cls.ALL_ACCOUNTS_NAME, [hbo, netflix, pcc])

        return all_accounts, [
            AccountList("Entertainment", [hbo, netflix]),
            AccountList("Work", []),
            AccountList("School", [pcc]),
            AccountList("finance", []),
            AccountList("games", []),
            all_accounts
        ]

    @classmethod
    def lookup(cls, name):
        return cls.__map[name.lower()]

