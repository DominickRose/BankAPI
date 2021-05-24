from daos.client_dao import ClientDAO
from daos.account_dao import AccountDao

from entities.client import Client
from entities.account import Account

from exceptions.exceptions import ClientNotFoundException, AccountNotFoundException

clientDAO: ClientDAO = None
accountDAO: AccountDao = None

class TestClientDAO:
    def test_1_add_client(self):
        test_client = Client(0, 'John', 'Doe', 0)
        result = clientDAO.add_client(test_client)
        assert test_client == result

    def test_2_add_client_id(self):
        test_client = Client(0, 'Jane', 'Doe', 0)
        result = clientDAO.add_client(test_client)
        assert result.client_id == 2

    def test_3_get_all_clients(self):
        all_clients = clientDAO.get_all_clients()
        assert len(all_clients) == 2

    def test_4_get_client_by_id(self):
        all_clients = clientDAO.get_all_clients()
        for client in all_clients:
            try:
                found_client = clientDAO.get_client_by_id(client.client_id)
                assert found_client == client
            except ClientNotFoundException as e:
                assert False

    def test_5_get_non_existent_client(self):
        try:
            found_client = clientDAO.get_client_by_id(3)
            assert False
        except ClientNotFoundException as e:
            assert str(e) == "Client with given id 3 does not exist"

    def test_6_update_client(self):
        client_to_update = clientDAO.get_client_by_id(1)
        try:
            results = clientDAO.update_client(client_to_update)
            assert client_to_update == results
        except ClientNotFoundException as e:
            assert False

    def test_7_update_nonexistent_client(self):
        try:
            test_client = Client(5, 'bad', 'client', 0)
            found_client = clientDAO.update_client(test_client)
            assert False
        except ClientNotFoundException as e:
            assert str(e) == "Client with given id 5 does not exist"

    def test_8_delete_client(self):
        try:
            result = clientDAO.delete_client_by_id(1)
            assert result
        except ClientNotFoundException as e:
            assert False

    def test_9_invalid_delete(self):
        try:
            result = clientDAO.delete_client_by_id(42)
            assert False
        except ClientNotFoundException as e:
            assert str(e) == "Client with given id 42 does not exist"

class TestAccountDAO:
    pass