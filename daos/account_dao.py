from entities.account import Account
from abc import ABC, abstractmethod

# DAO class for managing account entities
class AccountDao(ABC):
    @abstractmethod
    def add_account(self, account: Account) -> Account:
        pass

    @abstractmethod
    def get_all_accounts(self) -> []:
        pass

    @abstractmethod
    def get_single_account_by_id(self, account_id: int) -> Account:
        pass

    @abstractmethod
    def update_account(self, account: Account) -> Account:
        pass

    @abstractmethod
    def delete_account_by_id(self, account_id: int) -> bool:
        pass