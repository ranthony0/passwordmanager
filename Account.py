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

    def get_website_name(self):
        return self.__website_name

    def get_login_url(self):
        return self.__login_url

    def get_user_name(self):
        return self.__user_name

    def get_password(self):
        return self.__password

    def get_last_password_update(self):
        return self.__last_password_update

    def __str__(self):
        return F"Account: {self.__website_name}, {self.__login_url}, {self.__user_name}, {self.__password}, {self.__last_password_update}"

    def __repr__(self):
        return self.__str__()

    def get_website_name(self):
        return self.__website_name

    def get_login_url(self):
        return self.__login_url

    def set_website_name(self, website_name):
        self.__website_name = website_name

    def set_password(self, password):
        self.__password = password

    def set_last_password_update(self, last_password_update):
        self.__last_password_update = last_password_update
