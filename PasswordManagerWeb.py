from flask import Flask, render_template, request
from AccountList import AccountList


class PasswordManagerWeb:
    __app = Flask(__name__)
    __all_account_lists = None
    __all_accounts = None

    def __init__(self):
        PasswordManagerWeb.__app.secret_key = "some string value"

    @staticmethod
    def read_account_lists():
        return AccountList.get_account_lists()
    #read - have readaccountlist in passswordmanager but cant import?
    #Failure error not found when running print_account_list in web browswer?

    @staticmethod
    @__app.route("/print_account_lists")
    def print_account_lists():
        return render_template("print_account_lists.html", account_lists=PasswordManagerWeb.__all_account_lists)

    @staticmethod
    @__app.route("/select_account_list_for_print")
    def select_account_list_for_print():
        return render_template(
            "select_account_list_for_print.html",
            account_lists=PasswordManagerWeb.__all_account_lists
        )

    @staticmethod
    @__app.route("/print_account_list")
    def print_account_list():
        if "account_list" in request.args:
            account_list_name = request.args["account_list"]
        else:
            account_list_name = AccountList.ALL_ACCOUNTS_NAME
        for account_list in PasswordManagerWeb.__all_account_lists:
            if account_list.get_key() == account_list_name.lower():
                return render_template("print_account_list.html", account_list=account_list)
        return "<h1>Error! Couldn't find an account list named " + account_list_name + "!</h1>"

    def run(self):
        PasswordManagerWeb.__all_accounts, PasswordManagerWeb.__all_account_lists = AccountList.read_data()
        PasswordManagerWeb.__app.run(port=8000)


if __name__ == "__main__":
    app = PasswordManagerWeb()
    app.run()
