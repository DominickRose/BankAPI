from entities.account import Account
from abc import ABC

# DAO class for managing account entities
class AccountDao(ABC):
    def add_account(self, account: Account) -> Account:
        pass

    def get_all_accounts_for_client(self, client_id: int, lower_bound: float = 0, upper_bound: float = float('inf')) -> []:
        pass

    def get_single_account_by_id(self, account_id: int) -> Account:
        pass

    def update_account(self, account: Account) -> Account:
        pass

    def delete_account_by_id(self, account_id: int) -> bool:
        pass