from pymongo import *
class Database:
    pass

def test_database():
    print("Welcome to pymongo")
    client = MongoClient("mongodb+srv://anthonyrosales1:Limitededition1@sandbox.nbaerza.mongodb.net/?retryWrites=true&w=majority")
    print(client)
    db = client.PasswordManager
    print(db)
    db.accounts.drop()
    accounts = db.Accounts
    db.AccountLists.drop()
    account_lists = db.AccountsLists
    print(accounts)
    pcc = {
            "_id": "pcc mypcc.edu",
            "type": "phone",
            "info": "ms authenticator",
            "website_name": "pcc",
            "login_url:": "mypcc.edu",
            "user_name": "ant.ros",
            "password": "xxx",
            "last_password_update": "x"
    }
    hbo = {
            "_id": "HBO hbomax.com",
            "website_name": "HBO",
            "login_url:": "hbomax.com",
            "user_name": "anthony.rosales1",
            "password": "Ant1",
            "last_password_update": "02-15-2024"
    }
    netflix = {
            "_id": "Netflix Netflix.com",
            "type": "pin",
            "info": "1234",
            "website_name": "Netflix",
            "login_url:": "Netflix.com",
            "user_name": "ant",
            "password": "xxx",
            "last_password_update": "x"
    }

    all_accounts = [pcc, hbo, netflix]
    result = accounts.insert_many(all_accounts)
    all_accounts = list(accounts.find())
    print(all_accounts)
    print("Accounts:")
    account_map = {}
    for account in all_accounts:
        account_map[F"{account['website_name']} {account['login_url']}"] = account
        print(account)
    account_lists.insert_one({
        "name": "All Accounts",
        "accounts": account["_id"]} for account in all_accounts)
    #"accounts": [F"{account['website_name']} {account['login_url']}" for account in all_accounts
    #})
    all_accounts_list = account_lists.find_one({"name": "All Accounts"})
    print(all_accounts_list)
    for account_key in all_accounts_list["accounts"]:
        print(account_map[account_key])



if __name__ == "__main__":
    test_database()