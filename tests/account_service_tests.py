from entities.account import Account

from daos.account_dao_local import AccountDaoLocal
from daos.account_dao_postgres import AccountDaoPostgres

from exceptions.exceptions import AccountNotFoundException
from exceptions.exceptions import AccountOwnershipException
from exceptions.exceptions import InsufficientFundsException

from services.account_service import AccountService
from services.account_service_impl import AccountServiceImpl

from unittest.mock import MagicMock

account_dao = AccountDaoPostgres()

accounts = [
    Account(1, 1, 100, ''),
    Account(2, 1, 200, ''),
    Account(3, 2, 50, ''),
    Account(4, 3, 450, '')
]
account_dao.get_all_accounts = MagicMock(return_value= accounts)

accountService: AccountService = AccountServiceImpl(account_dao)

test_account = Account(0, 0, 175, 'Checking')
test_account2 = Account(0, 0, 175, 'Savings')

def test_1_add_account():
    accountService.add_account_to_client(1, test_account)
    assert test_account.owner_id == 1  # Confirm the owner is being associated with the account


def test_2_1_retrieve_client_accounts():
    results = accountService.get_all_client_accounts(1)
    assert len(results) == 2


def test_2_2_retrieve_client_accounts():
    results = accountService.get_all_client_accounts(2)
    assert len(results) == 1


def test_3_1_retrieve_accounts_in_range():
    results = accountService.get_all_client_accounts_in_range(1, 150, 250)
    assert len(results) == 1


def test_4_retrieve_specific_account():
    result = accountService.get_specific_account_for_client(1, test_account.account_id)
    assert result.account_id == test_account.account_id


def test_5_update_account():
    test_account.balance = 300
    updated_account = accountService.update_account_for_client(1, test_account)
    assert test_account.balance == updated_account.balance


def test_6_1_delete_specific_account():
    result = accountService.delete_specific_account_for_client(1, test_account.account_id)
    assert result  # Confrim deletion


def test_6_2_invalid_delete():
    try:
        # Delete an already deleted account
        result = accountService.delete_specific_account_for_client(1, test_account.account_id)
        assert False
    except AccountNotFoundException as e:
        assert str(e) == f"Account with given id {test_account.account_id} was not found"
    accountService.add_account_to_client(1, test_account)


def test_6_3__invalid_delete2():
    try:
        result = accountService.delete_specific_account_for_client(2, test_account.account_id)  # Try to delete an unowned account
        assert False
    except AccountOwnershipException as e:
        assert str(e) == f"Client with id 2 does not own account with id {test_account.account_id}"


def test_7_1_change_money():
    accountService.change_money_in_account(1, test_account.account_id, 50)
    assert accountService.get_specific_account_for_client(1, test_account.account_id).balance == 350


def test_7_2_change_money():
    accountService.change_money_in_account(1, test_account.account_id, -75)
    assert accountService.get_specific_account_for_client(1, test_account.account_id).balance == 275


def test_7_3_overwithdraw():
    try:
        accountService.change_money_in_account(1, test_account.account_id, -500)
        assert False
    except InsufficientFundsException as e:
        assert str(e) == f"Account with id {test_account.account_id} lacks funds for withdraw"


def test_7_4_invalid_access():
    try:
        accountService.change_money_in_account(2, test_account.account_id, 50)
        assert False
    except AccountOwnershipException as e:
        assert str(e) == f"Client with id 2 does not own account with id {test_account.account_id}"


def test_8_1_transfer_funds():
    accountService.add_account_to_client(1, test_account2)
    accountService.transfer_funds(1, test_account.account_id, test_account2.account_id, 50)
    account1 = accountService.get_specific_account_for_client(1, test_account.account_id)
    account2 = accountService.get_specific_account_for_client(1, test_account2.account_id)
    assert account1.balance == 225 and account2.balance == 225


def test_8_2_invalid_transfer():
    try:
        accountService.transfer_funds(1, test_account.account_id, test_account2.account_id, 500)
        assert False
    except InsufficientFundsException as e:
        assert str(e) == f"Account with id {test_account.account_id} lacks funds for withdraw"