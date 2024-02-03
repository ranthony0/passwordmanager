class Account:
    __website_name = ""
    __login_url = ""
    __user_name = ""
    __password = ""
    __last_password_update = ""

    def __init__(self, website_name, login_url, user_name, password, last_password_update):
        self.__website_name = website_name
        self.__login_url = login_url
        self.__user_name = user_name
        self.__password = password
        self.__last_password_update = last_password_update

    def __str__(self):
        return F"Account: {self.__website_name}, {self.__user_name}"

    def account_ok(self, account_list):
        raise Exception("account_ok is abstract!")