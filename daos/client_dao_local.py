from daos.client_dao import ClientDAO
from entities.client import Client

from exceptions.exceptions import ClientNotFoundException

class ClientDaoLocal(ClientDAO):
    local_clients = {}
    current_client_id = 1

    def add_client(self, client: Client) -> Client:
        client.client_id = ClientDaoLocal.current_client_id
        ClientDaoLocal.current_client_id += 1
        ClientDaoLocal.local_clients[client.client_id] = client
        return ClientDaoLocal.local_clients[client.client_id]


    def get_all_clients(self) -> []:
        all_clients = list(ClientDaoLocal.local_clients.values())
        return all_clients

    def get_client_by_id(self, client_id: int) -> Client:
        try:
            client = ClientDaoLocal.local_clients[client_id]
            return client
        except KeyError as e:
            raise ClientNotFoundException(f'Client with given id {client_id} does not exist')

    def update_client(self, client: Client) -> Client:
        if client.client_id not in ClientDaoLocal.local_clients:
            raise ClientNotFoundException(f'Client with given id {client.client_id} does not exist')

        ClientDaoLocal.local_clients[client.client_id] = client
        return client

    def delete_client_by_id(self, client_id: int) -> bool:
        try:
            del ClientDaoLocal.local_clients[client_id]
            return True
        except KeyError as e:
            raise ClientNotFoundException(f'Client with given id {client_id} does not exist')
