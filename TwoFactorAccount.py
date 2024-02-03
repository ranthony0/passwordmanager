from Account import Account

class TwoFactorAccount(Account):
    def account_ok(self, account_list, exception_term):
        if account_list <3:
            return True
        elif exception_term and account_list == 3:
            return True
        else:
            return False