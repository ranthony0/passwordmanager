from Account import Account

class TwoFactorAccount(Account):
    __website_name = ""
    __login_url = ""
    __user_name = ""
    __password = ""
    __last_password_update = ""
    __type = ""
    __info = ""

    def __init__(self, website_name, login_url, user_name, password, last_password_update, type, info):
        super().__init__(website_name, login_url, user_name, password, last_password_update)
        self.__type = type
        self.__info = info

    def to_dict(self):
        dict = super().to_dict()
        dict["type"] = "TwoFactorAccount"
        dict["2fa_type"] = self.__type
        dict["2fa_info"] = self.__info
        return dict

    def get_type(self):
        return self.__type

    def get_info(self):
        return self.__info

    def __str__(self):
        return super().__str__() + f" {self.__type}:{self.__info}"


