from flask import Flask, render_template, request, redirect, url_for
from AccountList import AccountList
from datetime import datetime
from Account import Account




class PasswordManagerWeb:
    __app = Flask(__name__)
    __all_account_lists = None
    __all_accounts = None

    def __init__(self):
        PasswordManagerWeb.__app.secret_key = "some string value"

    @staticmethod
    def find_account_list(account_list_name):
        for account_list in PasswordManagerWeb.__all_account_lists:
            if account_list.get_key() == account_list_name.lower():
                return account_list
        return None

    @staticmethod
    def find_account(account_name, account_list):
        for account in account_list:
            if account_name.lower() == account.get_key().lower():
                return account
            return None

    @staticmethod
    def read_account_lists():
        return AccountList.get_account_lists()

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
    @__app.route("/select_account_list_for_delete")
    def select_account_list_for_delete():
        return render_template(
            "select_account_list_for_delete.html",
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
        return render_template("error.html", error_message=F"Error! Couldn't find an account list named {account_list_name}!")

    @staticmethod
    @__app.route("/delete_account_list")
    def delete_account_list():
        if "account_list" in request.args:
            account_list_name = request.args["account_list"]
        else:
            account_list_name = AccountList.ALL_ACCOUNTS_NAME
        for account_list in PasswordManagerWeb.__all_account_lists:
            if account_list.get_key() == account_list_name.lower():
                PasswordManagerWeb.__all_account_lists.remove(account_list)
                account_list.delete()
                return render_template("delete_succeeded.html", account_list_name=account_list_name)
        return render_template("error.html", error_message=F"Error! Couldn't find an account list named {account_list_name}!")

    @staticmethod
    @__app.route("/get_account_name_and_password_for_update")
    def get_account_name_and_password_for_update():
        return render_template(
            "get_account_name_and_password_for_update.html",
            all_accounts=PasswordManagerWeb.__all_accounts
        )

    @staticmethod
    @__app.route("/update_account", methods=["POST"])
    def update_account():
        password = request.form["password"]
        account_name = request.form["account_name"]
        for account in PasswordManagerWeb.__all_accounts:
            if account_name.lower() == account.get_key().lower():
                account.set_password(password)
                account.set_last_password_update(str(datetime.now()))
                account.add_to_database()
                return render_template("update_succeeded.html", account_name=account_name, password=password)
        return F"Error! Couldn't find account named {account_name}!"

    @staticmethod
    @__app.route("/select_account_for_remove")
    def select_account_for_remove():
        account_list_name = request.args["account_list"]
        account_list = PasswordManagerWeb.find_account_list(account_list_name)
        if account_list is None:
            return render_template(
                "error.html",
                error_message=F"Error! Couldn't find Account List {account_list_name}!")
        return render_template("select_account_for_remove.html", account_list=account_list)

    @staticmethod
    @__app.route("/select_account_list_for_remove_account")
    def select_account_list_for_remove_account():
        return render_template(
            "select_account_list_for_remove_account.html",
            account_lists=PasswordManagerWeb.__all_account_lists
        )

    @staticmethod
    @__app.route("/remove_account_from_list")
    def remove_account_from_list():
        account_name = request.args["account_name"]
        account_list_name = request.args["account_list_name"]
        account_list = PasswordManagerWeb.find_account_list(account_list_name)
        if account_list is None:
            return render_template(
                "error.html",
                error_message=F"Error! Couldn't find Account List {account_list_name}!")
        account = Account.lookup(account_name)
        if account is None:
            return render_template(
                "error.html",
                error_message= F"Error! Couldn't find Account named {account_name} in List {account_list_name}")
        account_list.remove(account)
        account_list.add_to_database()
        return render_template(
            "remove_account_from_list_succeeded.html",
            account_name=account_name,
            account_list_name=account_list_name
        )
    @staticmethod
    @__app.route("/type_account_list_for_add")
    def type_account_list_for_add():
        return render_template(
            "type_account_list_for_add.html"
        )

    @staticmethod
    @__app.route("/add_account_list")
    def add_account_list():
        if "account_list_name" in request.args:
            name = request.args["account_list_name"]
        else:
            return render_template("error.html", error_message="Account list name not specified")
        try:
            account_list = AccountList.lookup(name)
            if account_list is not None:
                return render_template("error.html", error_message="Account list already exists")
        except KeyError:
            pass
        account_list = AccountList(name, [])
        AccountList.add_to_database(account_list)
        PasswordManagerWeb.__all_account_lists.append(account_list)
        return render_template("add_account_list_succeeded.html", account_list_name=name)

    @staticmethod
    @__app.route("/select_account_lists_for_join")
    def select_account_lists_for_join():
        return render_template(
            "select_account_lists_for_join.html",
            account_lists=PasswordManagerWeb.__all_account_lists
        )

    @staticmethod
    @__app.route("/join_account_lists")
    def join_account_lists():
        account_list_name_1 = request.args["account_list_name_1"]
        account_list_name_2 = request.args["account_list_name_2"]
        account_list_1 = PasswordManagerWeb.find_account_list(account_list_name_1)
        account_list_2 = PasswordManagerWeb.find_account_list(account_list_name_2)
        if account_list_1 is None:
            return render_template(
                "error.html",
                error_message=F"Error! Couldn't find Account List {account_list_name_1}!"
            )
        if account_list_2 is None:
            return render_template(
                "error.html",
                error_message=F"Error! Couldn't find Account List {account_list_name_2}!"
            )
        new_list = account_list_1 + account_list_2
        if new_list is None:
            return render_template(
                "error.html",
                error_message=F"Error! Account List already exists {account_list_name_1}/{account_list_name_2}!"
            )
        PasswordManagerWeb.__all_account_lists.append(new_list)
        new_list.add_to_database()
        return render_template(
            "join_succeeded.html",
            account_list_name_1=account_list_name_1,
            account_list_name_2=account_list_name_2
        )
    @staticmethod
    @__app.route("/")
    def redirect_to_main():
        return redirect(url_for("main_menu"))


    @staticmethod
    @__app.route("/main_menu")
    def main_menu():
        return render_template("main_menu.html")

    def run(self):
        PasswordManagerWeb.__all_accounts, PasswordManagerWeb.__all_account_lists = AccountList.read_data()
        PasswordManagerWeb.__app.run(port=8443, ssl_context=('cert.pem', 'key.pem'))


if __name__ == "__main__":
    app = PasswordManagerWeb()
    app.run()
