from abc import ABC

from entities.client import Client

class ClientService(ABC):
    def add_new_client(self, client: Client) -> Client:
        pass

    def get_client_by_id(self, client_id: int) -> Client:
        pass

    def get_all_clients(self) -> []:
        pass

    def update_client(self, client: Client) -> Client:
        pass

    def delete_client_by_id(self, client_id: int) -> bool:
        pass
