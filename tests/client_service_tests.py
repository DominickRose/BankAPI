from entities.client import Client

from daos.client_dao_local import ClientDaoLocal

from exceptions.exceptions import ClientNotFoundException

from services.client_service import ClientService
from services.client_service_impl import ClientServiceImpl

clientDao = ClientDaoLocal()
clientDao.add_client(Client(0, 'John', 'Doe', 0))
clientDao.add_client(Client(0, 'Jane', 'Doe', 0))
clientDao.add_client(Client(0, 'Jack', 'Doe', 0))

clientService: ClientService = ClientServiceImpl(clientDao)

test_client = Client(0, 'Jill', 'Doe', 0)


def test_1_add_new_client():
    added_client = clientService.add_new_client(test_client)
    assert test_client == added_client  # Confirm that what is added is correct


def test_2_get_client_by_id():
    result = clientService.get_client_by_id(test_client.client_id)
    assert result == test_client  # Test that the correct person is retrieved


def test_3_get_all_clients():
    all_clients = clientService.get_all_clients()
    assert len(all_clients) == 4  # Test that all clients are accounted for


def test_4_update_client():
    test_client.last_name = "Buck"
    updated = clientService.update_client(test_client)
    assert updated == test_client  # Test that client is correctly updated


def test_5_delete_client_by_id():
    result = clientService.delete_client_by_id(test_client.client_id)
    assert result  # Check that the DAO confirms deletion
    assert len(clientService.get_all_clients()) == 3  # Check that the DAO deletes


def test_6_access_deleted_client():
    try:
        result = clientService.get_client_by_id(test_client.client_id)
        assert False
    except ClientNotFoundException as e:
        assert str(e) == f"Client with given id {test_client.client_id} does not exist"
