class AccountList:
    __name = ""
    __accounts = []

    def __init__(self, name, accounts):
        self.__name = name
        self.__accounts = []

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
        new_list = AccountList(self.get_name() + "/" + other.get_name())
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
    @staticmethod
    def get_account_lists():
        return [
            AccountList("Entertainment", []),
            AccountList("Work", []),
            AccountList("School", []),
            AccountList("finance", []),
            AccountList("games", []),
            AccountList("All accounts", [])
        ]


