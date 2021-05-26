from psycopg2 import connect, OperationalError
import os

def make_connection():
    try:
        con = connect(
            host = os.environ.get('host'),
            database = os.environ.get('database'),
            user = os.environ.get('username'),
            password = os.environ.get('password'),
            port = os.environ.get('port')
        )
        return con
    except OperationalError as e:
        print(e)

connection = make_connection()