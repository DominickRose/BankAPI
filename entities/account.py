#Represents a specific bank account for a single user
class Account:
    def __init__(self, account_id:int, owner_id:int, balance: int, type: str):
        self.account_id = account_id
        self.owner_id = owner_id
        self.balance = balance
        self.type = type

    def json(self):
        account = {
            'accountId': self.account_id,
            'ownerId': self.owner_id,
            'balance': self.balance,
            'type': self.type
        }
        return account

    @staticmethod
    def from_json(json):
        account = Account(0, 0, 0, '')
        account.account_id = json['accountId']
        account.owner_id = json['ownerId']
        account.balance = json['balance']
        account.type = json['type']
        return account