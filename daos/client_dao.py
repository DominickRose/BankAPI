from entities.client import Client
from abc import ABC

# DAO class for managing client entities
class ClientDAO(ABC):
    def add_client(self, client: Client) -> Client:
        pass

    def get_all_clients(self) -> []:
        pass

    def get_client_by_id(self, client_id: int) -> Client:
        pass

    def update_client(self, client: Client) -> Client:
        pass

    def delete_client_by_id(self, client_id: int) -> bool:
        pass