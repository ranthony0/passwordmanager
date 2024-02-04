class AccountList:
    __name = ""
    __accounts = []

    def __init__(self, name, accounts):
        self.__name = name
        self.__accounts = accounts

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