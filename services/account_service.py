from abc import ABC, abstractmethod

from entities.account import Account

class AccountService(ABC):
    @abstractmethod
    def add_account_to_client(self, client_id: int, account: Account) -> Account:
        pass

    @abstractmethod
    def get_all_client_accounts(self, client_id: int) -> []:
        pass

    @abstractmethod
    def get_all_client_accounts_in_range(self, client_id: int, lower_bound: int, upper_bound: int) -> []:
        pass

    @abstractmethod
    def get_specific_account_for_client(self, client_id: int, account_id: int) -> Account:
        pass

    @abstractmethod
    def update_account_for_client(self, client_id: int, account: Account) -> Account:
        pass

    @abstractmethod
    def delete_specific_account_for_client(self, client_id: int, account_id: int) -> bool:
        pass

    @abstractmethod
    def change_money_in_account(self, client_id: int, account_id: int, amount: int) -> bool:
        pass

    @abstractmethod
    def transfer_funds(self, client_id: int, start_account_id: int, end_account_id: int, amount: int) -> bool:
        pass
