from abc import ABC, abstractmethod

from entities.client import Client

class ClientService(ABC):

    @abstractmethod
    def add_new_client(self, client: Client) -> Client:
        pass

    @abstractmethod
    def get_client_by_id(self, client_id: int) -> Client:
        pass

    @abstractmethod
    def get_all_clients(self) -> []:
        pass

    @abstractmethod
    def update_client(self, client: Client) -> Client:
        pass

    @abstractmethod
    def delete_client_by_id(self, client_id: int) -> bool:
        pass
