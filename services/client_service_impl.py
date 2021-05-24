from entities.client import Client

from daos.client_dao import ClientDAO

from services.client_service import ClientService


class ClientServiceImpl(ClientService):
    def __init__(self, client_dao: ClientDAO):
        self.client_dao = client_dao

    def add_new_client(self, client: Client) -> Client:
        return self.client_dao.add_client(client)

    def get_client_by_id(self, client_id: int) -> Client:
        return self.client_dao.get_client_by_id(client_id)

    def get_all_clients(self) -> []:
        return self.client_dao.get_all_clients()

    def update_client(self, client: Client) -> Client:
        return self.client_dao.update_client(client)

    def delete_client_by_id(self, client_id: int) -> bool:
        return self.client_dao.delete_client_by_id(client_id)
