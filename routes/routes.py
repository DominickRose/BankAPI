from flask import Flask, jsonify, request

from entities.client import Client
from entities.account import Account

from daos.client_dao_local import ClientDaoLocal
from daos.client_dao_postgres import ClientDaoPostgres

from daos.account_dao_local import AccountDaoLocal
from daos.account_dao_postgres import AccountDaoPostgres

from services.client_service_impl import ClientServiceImpl
from services.account_service_impl import AccountServiceImpl

from exceptions.exceptions import ClientNotFoundException, AccountNotFoundException, AccountOwnershipException, \
    InsufficientFundsException

client_dao = ClientDaoPostgres()
client_service = ClientServiceImpl(client_dao)

account_dao = AccountDaoPostgres()
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
        if not client_id.isnumeric():
            return "Invalid URI", 400
        try:
            client = client_service.get_client_by_id(int(client_id))
            return jsonify(client.json()), 200
        except ClientNotFoundException as e:
            return str(e), 404

    @app.put('/clients/<client_id>')
    def update_client(client_id: str):
        if not client_id.isnumeric():
            return "Invalid URI", 400
        try:
            updated_client = Client.from_json(request.json)
            updated_client.client_id = int(client_id)
            client_service.update_client(updated_client)
            return jsonify(updated_client.json()), 200
        except ClientNotFoundException as e:
            return str(e), 404

    @app.delete('/clients/<client_id>')
    def delete_client_by_id(client_id: str):
        if not client_id.isnumeric():
            return "Invalid URI", 400
        try:
            client_service.get_client_by_id(int(client_id))

            #Delete all accounts owned by a client to avoid foreign key errors
            all_accounts = account_service.get_all_client_accounts(int(client_id))
            for account in all_accounts:
                account_service.delete_specific_account_for_client(int(client_id), account.account_id)

            client_service.delete_client_by_id(int(client_id))
            return f"Successfully deleted client with id {client_id}", 205
        except ClientNotFoundException as e:
            return str(e), 404


def account_routes(app: Flask):
    @app.post('/clients/<client_id>/accounts')
    def create_new_account(client_id: str):
        if not client_id.isnumeric():
            return "Invalid URI", 400
        try:
            client_service.get_client_by_id(int(client_id))
            new_account = Account.from_json(request.json)
            account_service.add_account_to_client(int(client_id), new_account)
            return jsonify(new_account.json()), 201
        except ClientNotFoundException as e:
            return str(e), 404

    @app.get('/clients/<client_id>/accounts')
    def get_all_accounts_for_client(client_id: str):
        if not client_id.isnumeric():
            return "Invalid URI", 400
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

    @app.get('/clients/<client_id>/accounts/<account_id>')
    def get_account_by_id(client_id: str, account_id: str):
        if not client_id.isnumeric() or not account_id.isnumeric():
            return "Invalid URI", 400
        try:
            client_service.get_client_by_id(int(client_id))
            account = account_service.get_specific_account_for_client(int(client_id), int(account_id))
            return jsonify(account.json()), 200
        except ClientNotFoundException as e:
            return str(e), 404
        except AccountNotFoundException as e:
            return str(e), 404
        except AccountOwnershipException as e:
            return str(e), 400

    @app.put('/clients/<client_id>/accounts/<account_id>')
    def update_account_by_id(client_id: str, account_id: str):
        if not client_id.isnumeric() or not account_id.isnumeric():
            return "Invalid URI", 400
        try:
            client_service.get_client_by_id(int(client_id))
            account = Account.from_json(request.json)
            account.account_id = int(account_id)
            account.owner_id = int(client_id)
            updated = account_service.update_account_for_client(int(client_id), account)
            return jsonify(updated.json()), 200
        except ClientNotFoundException as e:
            return str(e), 404
        except AccountNotFoundException as e:
            return str(e), 404

    @app.delete('/clients/<client_id>/accounts/<account_id>')
    def delete_account_by_id(client_id: str, account_id: str):
        if not client_id.isnumeric() or not account_id.isnumeric():
            return "Invalid URI", 400
        try:
            client_service.get_client_by_id(int(client_id))
            account_service.delete_specific_account_for_client(int(client_id), int(account_id))
            return f"Successfully deleted account with id {account_id}", 205
        except ClientNotFoundException as e:
            return str(e), 404
        except AccountNotFoundException as e:
            return str(e), 404
        except AccountOwnershipException as e:
            return str(e), 400

    @app.patch('/clients/<client_id>/accounts/<account_id>')
    def make_withdraw_or_deposit(client_id: str, account_id: str):
        if not client_id.isnumeric() or not account_id.isnumeric():
            return "Invalid URI", 400
        try:
            client_service.get_client_by_id(int(client_id))
            if 'withdraw' in request.json:
                amount = request.json['withdraw'] * -1
                account_service.change_money_in_account(int(client_id), int(account_id), amount)
                return f"Withdrew ${-1 * amount} from account with id {account_id}", 200
            elif 'deposit' in request.json:
                amount = request.json['deposit']
                account_service.change_money_in_account(int(client_id), int(account_id), amount)
                return f"Deposited ${amount} into account with id {account_id}", 200
            else:
                return "Either 'withdraw' or 'deposit' must be contained in json body", 400
        except ClientNotFoundException as e:
            return str(e), 404
        except AccountNotFoundException as e:
            return str(e), 404
        except AccountOwnershipException as e:
            return str(e), 400
        except InsufficientFundsException as e:
            return str(e), 422

    @app.patch('/clients/<client_id>/accounts/<start_id>/transfer/<end_id>')
    def transfer_funds(client_id: str, start_id: str, end_id: str):
        if not client_id.isnumeric() or not start_id.isnumeric() or not end_id.isnumeric():
            return "Invalid URI", 400
        try:
            client_service.get_client_by_id(int(client_id))
            if 'amount' in request.json:
                amount = request.json['amount']
                account_service.transfer_funds(int(client_id), int(start_id), int(end_id), amount)
                return f"Succesfully transfered ${amount} from account {start_id} to account {end_id}", 200
            else:
                return "JSON body must contain 'amount' for transfer", 400
        except ClientNotFoundException as e:
            return str(e), 404
        except AccountNotFoundException as e:
            return str(e), 404
        except AccountOwnershipException as e:
            return str(e), 400
        except InsufficientFundsException as e:
            return str(e), 422