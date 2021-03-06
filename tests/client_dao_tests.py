from daos.client_dao import ClientDAO
from daos.client_dao_local import ClientDaoLocal
from daos.client_dao_postgres import ClientDaoPostgres

from entities.client import Client

from exceptions.exceptions import ClientNotFoundException

# Create DAOs for testing
#clientDAO: ClientDAO = ClientDaoLocal()
clientDAO: ClientDAO = ClientDaoPostgres()


def test_1_add_client():  # Test that a client is being stored and returned on success
    test_client = Client(0, 'John', 'Doe')
    result = clientDAO.add_client(test_client)
    assert test_client == result


def test_2_add_client_id():  # Test that adding a client changes the id
    test_client = Client(0, 'Jane', 'Doe')
    result = clientDAO.add_client(test_client)
    assert result.client_id != 0


def test_3_get_all_clients():  # Test that all clients are being found
    all_clients = clientDAO.get_all_clients()
    assert len(all_clients) >= 2


def test_4_get_client_by_id():  # Test we can get a single client from their id
    all_clients = clientDAO.get_all_clients()
    for client in all_clients:
        try:
            found_client = clientDAO.get_client_by_id(client.client_id)
            assert found_client.client_id == client.client_id
        except ClientNotFoundException as e:
            assert False


def test_5_get_non_existent_client():  # Test that an exception is thrown when searching for a non-existen
    try:
        found_client = clientDAO.get_client_by_id(0)
        assert False
    except ClientNotFoundException as e:
        assert str(e) == "Client with given id 0 does not exist"


def test_6_update_client():  # Test clients are updated correctly
    test_client = Client(0, 'John', 'Doe')
    clientDAO.add_client(test_client)
    client_to_update = clientDAO.get_client_by_id(test_client.client_id)
    client_to_update.last_name = 'Buck'
    try:
        results = clientDAO.update_client(client_to_update)
        assert client_to_update.last_name == results.last_name
    except ClientNotFoundException as e:
        assert False


def test_7_update_nonexistent_client():  # Test we can't update a non-existent client
    try:
        test_client = Client(0, 'bad', 'client')
        found_client = clientDAO.update_client(test_client)
        assert False
    except ClientNotFoundException as e:
        assert str(e) == "Client with given id 0 does not exist"


def test_8_delete_client():  # Test clients can be deleted
    try:
        test_client = Client(0, 'John', 'Doe')
        clientDAO.add_client(test_client)
        result = clientDAO.delete_client_by_id(test_client.client_id)
        assert result
    except ClientNotFoundException as e:
        assert False


def test_9_invalid_delete():  # Test we can't delete what does't exists
    try:
        result = clientDAO.delete_client_by_id(0)
        assert False
    except ClientNotFoundException as e:
        assert str(e) == "Client with given id 0 does not exist"