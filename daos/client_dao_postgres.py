from entities.client import Client
from daos.client_dao import ClientDAO

from exceptions.exceptions import ClientNotFoundException

from utils.connection_util import connection

class ClientDaoPostgres(ClientDAO):
    def add_client(self, client: Client) -> Client:
        sql = """insert into client (first_name, last_name) values (%s, %s) returning client_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (client.first_name, client.last_name))
        connection.commit()
        client_id = cursor.fetchone()[0]
        client.client_id = client_id
        return client

    def get_all_clients(self) -> []:
        sql = """select * from client"""
        cursor = connection.cursor()
        cursor.execute(sql)
        all_records = cursor.fetchall()
        return [Client(*record) for record in all_records]

    def get_client_by_id(self, client_id: int) -> Client:
        sql = """select * from client where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        record = cursor.fetchone()
        try:
            return Client(*record)
        except TypeError:
            raise ClientNotFoundException(f'Client with given id {client_id} does not exist')

    def update_client(self, client: Client) -> Client:
        self.get_client_by_id(client.client_id) #Check the given record exists

        sql = """update client set first_name = %s, last_name = %s where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (client.first_name, client.last_name, client.client_id))
        connection.commit()
        return client

    def delete_client_by_id(self, client_id: int) -> bool:
        self.get_client_by_id(client_id) #Check the given record exists

        sql = """delete from client where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        connection.commit()
        return True