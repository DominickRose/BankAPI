from daos.account_dao import AccountDao
from daos.account_dao_local import AccountDaoLocal

from entities.account import Account

from exceptions.exceptions import AccountNotFoundException

accountDAO: AccountDao = AccountDaoLocal()

test_account = Account(0, 1, 0, '')


def test_1_create_account():
    accountDAO.add_account(test_account)
    assert test_account.account_id != 0


def test_2_get_all_accounts():
    account1 = Account(0, 1, 0, '')
    account2 = Account(0, 1, 0, '')
    account3 = Account(0, 1, 0, '')
    accountDAO.add_account(account1)
    accountDAO.add_account(account2)
    accountDAO.add_account(account3)
    all_accounts = accountDAO.get_all_accounts()
    assert len(all_accounts) >= 3


def test_4_get_single_account():
    result = accountDAO.get_single_account_by_id(test_account.account_id)
    assert result == test_account


def test_5_update_account():
    test_account.balance = 500
    try:
        result = accountDAO.update_account(test_account)
        assert result.balance == test_account.balance
    except AccountNotFoundException as e:
        assert False


def test_6_update_invalid_account():
    invalid_account = Account(0, 1, 0, '')
    try:
        result = accountDAO.update_account(invalid_account)
        assert False
    except AccountNotFoundException as e:
        assert str(e) == "Account with given id 0 was not found"


def test_7_delete_account():
    try:
        result = accountDAO.delete_account_by_id(test_account.account_id)
        assert result
    except AccountNotFoundException as e:
        assert False


def test_8_delete_invalid_account():
    invalid_account = Account(0, 1, 0, '')
    try:
        result = accountDAO.delete_account_by_id(invalid_account.account_id)
        assert False
    except AccountNotFoundException as e:
        assert str(e) == "Account with given id 0 was not found"
