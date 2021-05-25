from flask import Flask, jsonify, request

from entities.client import Client
from entities.account import Account

from daos.client_dao_local import ClientDaoLocal
from daos.account_dao_local import AccountDaoLocal

from services.client_service_impl import ClientServiceImpl
from services.account_service_impl import AccountServiceImpl

from exceptions.exceptions import ClientNotFoundException, AccountNotFoundException, AccountOwnershipException, \
    InsufficientFundsException

client_dao = ClientDaoLocal()
client_service = ClientServiceImpl(client_dao)

account_dao = AccountDaoLocal()
account_service = AccountServiceImpl(account_dao)


def client_routes(app: Flask):
    @app.post('/clients')
    def add_client():
        new_client = Client.from_json(request.json)
        client_service.add_new_client(new_client)
        return jsonify(new_client.json()), 201

    @app.get('/clients')
    def get_all_clients():
        all_clients = client_service.get_all_clients()
        all_clients_json = [client.json() for client in all_clients]
        return jsonify(all_clients_json), 200

    @app.get('/clients/<client_id>')
    def get_client_by_id(client_id: str):
        try:
            client = client_service.get_client_by_id(int(client_id))
            return jsonify(client.json()), 200
        except ClientNotFoundException as e:
            return str(e), 404

    @app.put('/clients/<client_id>')
    def update_client(client_id: str):
        try:
            updated_client = Client.from_json(request.json)
            updated_client.client_id = int(client_id)
            client_service.update_client(updated_client)
            return jsonify(updated_client.json()), 200
        except ClientNotFoundException as e:
            return str(e), 404

    @app.delete('/clients/<client_id>')
    def delete_client_by_id(client_id: str):
        try:
            client_service.delete_client_by_id(int(client_id))
            return f"Successfully deleted client with id {client_id}", 205
        except ClientNotFoundException as e:
            return str(e), 404


def account_routes(app: Flask):
    @app.post('/clients/<client_id>/accounts')
    def create_new_account(client_id: str):
        try:
            client_service.get_client_by_id(int(client_id))
            new_account = Account.from_json(request.json)
            account_service.add_account_to_client(int(client_id), new_account)
            return jsonify(new_account.json()), 201
        except ClientNotFoundException as e:
            return str(e), 404

    @app.get('/clients/<client_id>/accounts')
    def get_all_accounts_for_client(client_id: str):
        try:
            client_service.get_client_by_id(int(client_id))
            lower_bound = request.args.get('amountGreaterThan')
            upper_bound = request.args.get('amountLessThan')
            if lower_bound == None and upper_bound == None:
                all_accounts = account_service.get_all_client_accounts(int(client_id))
            else:
                all_accounts = account_service.get_all_client_accounts_in_range(int(client_id), int(lower_bound),
                                                                                int(upper_bound))
            all_accounts_json = [account.json() for account in all_accounts]
            return jsonify(all_accounts_json), 200
        except ClientNotFoundException as e:
            return str(e), 404
