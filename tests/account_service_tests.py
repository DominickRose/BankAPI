from entities.account import Account

from daos.account_dao_local import AccountDaoLocal

from exceptions.exceptions import AccountNotFoundException
from exceptions.exceptions import AccountOwnershipException
from exceptions.exceptions import InsufficientFundsException

from services.account_service import AccountService
from services.account_service_impl import AccountServiceImpl

accountDao = AccountDaoLocal()
accountDao.add_account(Account(0, 1, 100, ''))
accountDao.add_account(Account(0, 1, 200, ''))
accountDao.add_account(Account(0, 2, 50, ''))
accountDao.add_account(Account(0, 2, 450, ''))

accountService: AccountService = AccountServiceImpl(accountDao)

test_account = Account(0, 0, 175, '')


def test_1_add_account():
    accountService.add_account_to_client(1, test_account)
    assert test_account.owner_id == 1  # Confirm the owner is being associated with the account


def test_2_retrieve_client_accounts1():
    results = accountService.get_all_client_accounts(1)
    assert len(results) == 3


def test_3_retrieve_client_accounts2():
    results = accountService.get_all_client_accounts(2)
    assert len(results) == 2


def test_4_retrieve_accounts_in_range1():
    results = accountService.get_all_client_accounts_in_range(1, 150, 250)
    assert len(results) == 2


def test_5_retrieve_accounts_in_range2():
    results = accountService.get_all_client_accounts_in_range(1, 0, 50)
    assert len(results) == 0


def test_5_1_retrieve_specific_account():
    result = accountService.get_specific_account_for_client(1, test_account.account_id)
    assert result == test_account


def test_6_update_account():
    test_account.balance = 300
    updated_account = accountService.update_account_for_client(1, test_account)
    assert test_account.balance == updated_account.balance


def test_7_delete_specific_account():
    result = accountService.delete_specific_account_for_client(1, test_account.account_id)
    assert result  # Confrim deletion
    assert len(accountService.get_all_client_accounts(1)) == 2  # Prove deletion


def test_8_invalid_delete():
    try:
        # Delete an already deleted account
        result = accountService.delete_specific_account_for_client(1, test_account.account_id)
        assert False
    except AccountNotFoundException as e:
        assert str(e) == f"Account with given id {test_account.account_id} was not found"


def test_9_invalid_delete2():
    try:
        result = accountService.delete_specific_account_for_client(2, 1)  # Try to delete an unowned account
        assert False
    except AccountOwnershipException as e:
        assert str(e) == "Client with id 2 does not own account with id 1"


def test_10_change_money1():
    accountService.change_money_in_account(1, 1, 50)
    assert accountService.get_specific_account_for_client(1, 1).balance == 150


def test_11_change_money1():
    accountService.change_money_in_account(1, 1, -75)
    assert accountService.get_specific_account_for_client(1, 1).balance == 75


def test_12_overwithdraw():
    try:
        accountService.change_money_in_account(1, 1, -500)
        assert False
    except InsufficientFundsException as e:
        assert str(e) == "Account with id 1 lacks funds for withdraw"


def test_13_invalid_access():
    try:
        accountService.change_money_in_account(2, 1, 50)
        assert False
    except AccountOwnershipException as e:
        assert str(e) == "Client with id 2 does not own account with id 1"


def test_14_transfer_funds():
    accountService.transfer_funds(1, 1, 2, 50)
    account1 = accountService.get_specific_account_for_client(1, 1)
    account2 = accountService.get_specific_account_for_client(1, 2)
    assert account1.balance == 25 and account2.balance == 250


def test_15_invalid_transfer():
    try:
        accountService.transfer_funds(1, 1, 2, 50)
        assert False
    except InsufficientFundsException as e:
        assert str(e) == "Account with id 1 lacks funds for withdraw"
