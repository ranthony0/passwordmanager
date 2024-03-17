from pymongo import *
from configparser import ConfigParser
import os


class Database:
    __client = None
    __accounts = None
    __account_lists = None
    __password_manager = None

    @classmethod
    def __connect(cls):
        if cls.__client is None:
            config = ConfigParser()
            config.read(os.environ["APPDATA"] + "/PasswordManager/PasswordManager.ini")
            username = config["Database"]["username"]
            password = config["Database"]["password"]
            hostname = config["Database"]["hostname"]
            cls.__client = MongoClient(F"mongodb+srv://{username}:{password}@{hostname}/?retryWrites=true&w=majority")
            cls.__password_manager = cls.__client.PasswordManager
            cls.__accounts = cls.__password_manager.Accounts
            cls.__account_lists = cls.__password_manager.AccountLists

    @classmethod
    def rebuild_data(cls):
        cls.__connect()
        pcc = {
            "_id": "pcc ant.ros",
            "type": "TwoFactorAccount",
            "2fa_type": "phone",
            "2fa_info": "ms authenticator",
            "website_name": "pcc",
            "login_url": "mypcc.edu",
            "user_name": "ant.ros",
            "password": "xxx",
            "last_password_update": "x"
         }

        hbo = {
            "_id": "hbo anthony.rosales1",
            "type": "Account",
            "website_name": "HBO",
            "login_url": "hbomax.com",
            "user_name": "anthony.rosales1",
            "password": "Ant1",
            "last_password_update": "02-15-2024"
         }

        netflix = {
            "_id": "netflix ant",
            "type": "TwoFactorAccount",
            "2fa_type": "pin",
            "2fa_info": "1234",
            "website_name": "Netflix",
            "login_url": "Netflix.com",
            "user_name": "ant",
            "password": "xxx",
            "last_password_update": "x"
         }

        ubif = {
            "_id": "ubif anthonyrosales",
            "type": "Account",
            "website_name": "ubif",
            "login_url": "ubif.com",
            "user_name": "anthonyrosales",
            "password": "xxx",
            "last_password_update": "x"
        }

        boa = {
            "_id": "boa ant",
            "type": "TwoFactorAccount",
            "2fa_type": "pin",
            "2fa_info": "1234",
            "website_name": "boa",
            "login_url": "boa.com",
            "user_name": "ant",
            "password": "xxx",
            "last_password_update": "x"
        }

        wow = {
            "_id": "wow zet",
            "type": "Account",
            "website_name": "wow",
            "login_url": "wow.com",
            "user_name": "zet",
            "password": "xxx",
            "last_password_update": "x"
        }

        cls.__password_manager.Accounts.drop()
        cls.__password_manager.AccountLists.drop()
        cls.__accounts = cls.__password_manager.Accounts
        cls.__account_lists = cls.__password_manager.AccountLists

        all_accounts = [pcc, hbo, netflix, ubif, boa, wow]
        cls.__accounts.insert_many(all_accounts)

        cls.__account_lists.insert_many([{
            "_id": "all accounts",
            "name": "All Accounts",
            "accounts": [account["_id"] for account in all_accounts]
        }, {
            "_id": "entertainment",
            "name": "Entertainment",
            "accounts": [account["_id"] for account in [hbo, netflix]]
        }, {
            "_id": "work",
            "name": "work",
            "accounts": [account["_id"] for account in [ubif]]
        }, {
            "_id": "school",
            "name": "school",
            "accounts": [account["_id"] for account in [pcc]]
        }, {
            "_id": "finance",
            "name": "finance",
            "accounts": [account["_id"] for account in [boa]]
        }, {
            "_id": "games",
            "name": "games",
            "accounts": [account["_id"] for account in [wow]]
        }])

    @classmethod
    def dump_data(cls):
        cls.__connect()
        accounts = cls.__accounts.find()
        for account in accounts:
            print(account)
        account_lists = cls.__account_lists.find()
        for account_list in account_lists:
            print(account_list)

    @classmethod
    def read_data(cls):
        from TwoFactorAccount import TwoFactorAccount
        from Account import Account
        from AccountList import AccountList

        cls.__connect()
        accounts = cls.__accounts.find()
        account_objects = []
        for account_dict in accounts:
            if account_dict["type"] == "Account":
                account_objects.append(Account(
                    account_dict["website_name"],
                    account_dict["login_url"],
                    account_dict["user_name"],
                    account_dict["password"],
                    account_dict["last_password_update"]
                ))
            elif account_dict["type"] == "TwoFactorAccount":
                account_objects.append(TwoFactorAccount(
                    account_dict["website_name"],
                    account_dict["login_url"],
                    account_dict["user_name"],
                    account_dict["password"],
                    account_dict["last_password_update"],
                    account_dict["2fa_type"],
                    account_dict["2fa_info"],
                ))
            else:
                print("Invalid account", account_dict)
        print("Accounts:")
        account_map = {}

        account_lists = cls.__account_lists.find()
        all_lists = []
        all_accounts = None
        for account_list_dict in account_lists:
            account_list = AccountList(account_list_dict["name"], [Account.lookup(key) for key in account_list_dict["accounts"]])
            all_lists.append(account_list)
            if account_list.get_name() == "All Accounts":
                all_accounts = account_list
        return all_accounts, all_lists

    @classmethod
    def add_account_list_to_database(cls, account_list):
        cls.__account_lists.update_one({ "_id": account_list.get_key()}, { "$set": account_list.to_dict() }, upsert=True)

    @classmethod
    def add_account_to_database(cls, account):
        cls.__connect()
        cls.__accounts.update_one({ "_id": account.get_key() }, { "$set": account.to_dict() }, upsert=True)

    @classmethod
    def delete_account_list(cls, account_list):
        cls.__account_lists.delete_one({"_id": account_list.get_key()})
