from daos.account_dao import AccountDao
from daos.account_dao_local import AccountDaoLocal
from daos.account_dao_postgres import AccountDaoPostgres
from daos.client_dao_postgres import ClientDaoPostgres

from entities.account import Account
from entities.client import Client

from exceptions.exceptions import AccountNotFoundException

#accountDAO: AccountDao = AccountDaoLocal()
account_dao: AccountDao = AccountDaoPostgres()
client_dao = ClientDaoPostgres()

# Ensure there is an existent client to own test accounts
test_client = Client(0, "Johnny", "Test")
client_dao.add_client(test_client)

test_account = Account(0, test_client.client_id, 0, 'Roth IRA')


def test_1_create_account():
    account_dao.add_account(test_account)
    assert test_account.account_id != 0


def test_2_get_all_accounts():
    account1 = Account(0, test_client.client_id, 0, 'Checking')
    account2 = Account(0, test_client.client_id, 0, 'Savings')
    account3 = Account(0, test_client.client_id, 0, 'Checking')
    account_dao.add_account(account1)
    account_dao.add_account(account2)
    account_dao.add_account(account3)
    all_accounts = account_dao.get_all_accounts()
    assert len(all_accounts) >= 3


def test_4_get_single_account():
    result = account_dao.get_single_account_by_id(test_account.account_id)
    assert result.account_id == test_account.account_id


def test_5_update_account():
    test_account.balance = 500
    try:
        result = account_dao.update_account(test_account)
        assert result.balance == test_account.balance
    except AccountNotFoundException as e:
        assert False


def test_6_update_invalid_account():
    invalid_account = Account(0, 1, 0, 'Checking')
    try:
        result = account_dao.update_account(invalid_account)
        assert False
    except AccountNotFoundException as e:
        assert str(e) == "Account with given id 0 was not found"


def test_7_delete_account():
    try:
        result = account_dao.delete_account_by_id(test_account.account_id)
        assert result
    except AccountNotFoundException as e:
        assert False


def test_8_delete_invalid_account():
    invalid_account = Account(0, 1, 0, 'Savings')
    try:
        result = account_dao.delete_account_by_id(invalid_account.account_id)
        assert False
    except AccountNotFoundException as e:
        assert str(e) == "Account with given id 0 was not found"
