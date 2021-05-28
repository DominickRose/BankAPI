from entities.account import Account

from daos.account_dao import AccountDao

from exceptions.exceptions import AccountNotFoundException

from utils.connection_util import connection

class AccountDaoPostgres(AccountDao):
    def add_account(self, account: Account) -> Account:
        sql = """insert into account (owner_id, balance, account_type) values (%s, %s, %s) returning account_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (account.owner_id, account.balance, account.type))
        connection.commit()
        account_id = cursor.fetchone()[0]
        account.account_id = account_id
        return account

    def get_all_accounts(self) -> []:
        sql = """select * from account"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        return [Account(*record) for record in records]

    def get_single_account_by_id(self, account_id: int) -> Account:
        sql = """select * from account where account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [account_id])
        record = cursor.fetchone()
        try:
            return Account(*record)
        except TypeError:
            raise AccountNotFoundException(f'Account with given id {account_id} was not found')

    def update_account(self, account: Account) -> Account:
        self.get_single_account_by_id(account.account_id) #Check that the record exists

        sql = """update account set owner_id = %s, balance = %s, account_type = %s where account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (account.owner_id, account.balance, account.type, account.account_id))
        connection.commit()
        return account

    def delete_account_by_id(self, account_id: int) -> bool:
        self.get_single_account_by_id(account_id) #Check that the record exists

        sql = """delete from account where account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [account_id])
        connection.commit()
        return True