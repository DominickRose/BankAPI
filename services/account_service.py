from abc import ABC

from entities.account import Account

class AccountService(ABC):
    def add_account_to_client(self, client_id: int, account: Account) -> Account:
        pass

    def retrieve_all_client_accounts(self, client_id: int) -> []:
        pass

    def retrieve_all_client_accounts_in_range(self, client_id: int, lower_bound: int, upper_bound: int) -> []:
        pass

    def retrieve_specific_account_for_client(self, client_id: int, account_id: int) -> Account:
        pass

    def update_account_for_client(self, client_id: int, account: Account) -> Account:
        pass

    def delete_specific_account_for_client(self, client_id: int, account_id: int) -> bool:
        pass

    def change_money_in_account(self, client_id: int, account_id: int, amount: int) -> bool:
        pass

    def transfer_funds(self, client_id: int, start_account_id: int, end_account_id: int, amount: int) -> bool:
        pass
