from entities.account import Account

from daos.account_dao import AccountDao

from exceptions.exceptions import AccountOwnershipException
from exceptions.exceptions import InsufficientFundsException

from services.account_service import AccountService


class AccountServiceImpl(AccountService):
    def __init__(self, account_dao: AccountDao):
        self.account_dao = account_dao


    def add_account_to_client(self, client_id: int, account: Account) -> Account:
        account.owner_id = client_id
        return self.account_dao.add_account(account)


    def retrieve_all_client_accounts(self, client_id: int) -> []:
        all_accounts = self.account_dao.get_all_accounts()
        return [account for account in all_accounts if account.owner_id == client_id]


    def retrieve_all_client_accounts_in_range(self, client_id: int, lower_bound: int, upper_bound: int) -> []:
        client_accounts = self.retrieve_all_client_accounts(client_id)
        return [account for account in client_accounts if lower_bound <= account.balance <= upper_bound]


    def retrieve_specific_account_for_client(self, client_id: int, account_id: int) -> Account:
        account = self.account_dao.get_single_account_by_id(account_id)
        if account.owner_id == client_id:
            return account
        else:
            raise AccountOwnershipException(f"Client with id {client_id} does not own account with id {account_id}")


    def update_account_for_client(self, client_id: int, account: Account) -> Account:
        if account.owner_id == client_id:
            return self.account_dao.update_account(account)
        else:
            raise AccountOwnershipException(
                f"Client with id {client_id} does not own account with id {account.account_id}")


    def delete_specific_account_for_client(self, client_id: int, account_id: int) -> bool:
        account = self.retrieve_specific_account_for_client(client_id, account_id) #Ensures ownership
        return self.account_dao.delete_account_by_id(account.account_id)


    def change_money_in_account(self, client_id: int, account_id: int, amount: int) -> bool:
        account = self.retrieve_specific_account_for_client(client_id, account_id)
        if account.balance + amount < 0:
            raise InsufficientFundsException(f'Account with id {account_id} lacks funds for withdraw')
        account.balance += amount
        self.account_dao.update_account(account)
        return True


    def transfer_funds(self, client_id: int, start_account_id: int, end_account_id: int, amount: int) -> bool:
        self.retrieve_specific_account_for_client(client_id, start_account_id) #This ensures ownership
        self.retrieve_specific_account_for_client(client_id, end_account_id) #This ensures ownership

        self.change_money_in_account(client_id, start_account_id, -1 * amount) #Withdraw the amount
        self.change_money_in_account(client_id, end_account_id, amount) #Deposit the amount
        return True
