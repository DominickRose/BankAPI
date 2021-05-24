from entities.account import Account

from daos.account_dao import AccountDao

from exceptions.exceptions import AccountNotFoundException

class AccountDaoLocal(AccountDao):
    account_ids = 1
    local_accounts = {}

    def add_account(self, account: Account) -> Account:
        account.account_id = AccountDaoLocal.account_ids
        AccountDaoLocal.account_ids += 1
        AccountDaoLocal.local_accounts[account.account_id] = account
        return account

    def get_all_accounts_for_client(self, client_id: int, lower_bound: float = 0, upper_bound: float = float('inf')) -> []:
        all_client_accounts = [account for account in AccountDaoLocal.local_accounts.values() if account.owner_id == client_id]
        all_client_accounts = [account for account in all_client_accounts if lower_bound <= account.balance <= upper_bound]
        return all_client_accounts

    def get_single_account_by_id(self, account_id: int) -> Account:
        try:
            result = AccountDaoLocal.local_accounts[account_id]
            return result
        except KeyError as e:
            raise AccountNotFoundException(f'Account with given id {account_id} was not found')

    def update_account(self, account: Account) -> Account:
        if account.account_id not in AccountDaoLocal.local_accounts:
            raise AccountNotFoundException(f'Account with given id {account.account_id} was not found')

        AccountDaoLocal.local_accounts[account.account_id] = account
        return account

    def delete_account_by_id(self, account_id: int) -> bool:
        try:
            del AccountDaoLocal.local_accounts[account_id]
            return True
        except KeyError as e:
            raise AccountNotFoundException(f'Account with given id {account_id} was not found')