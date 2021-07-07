import re

def validate_account(account):
    account_regex = '[a-zA-Z]\w{4,12}'
    return re.search(account_regex, account)

def validate_password(password):
    password_regex = '[a-zA-Z0-9!@##$%^&+=]{8,16}'
    return re.search(password_regex, password)
