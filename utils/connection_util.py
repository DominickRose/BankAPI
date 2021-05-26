from psycopg2 import connect, OperationalError

def make_connection():
    try:
        con = connect(
            host = 'database-1.cumk1bpwzhqs.us-west-1.rds.amazonaws.com',
            database = 'postgres',
            user = 'domrose42',
            password = 'twistyma3r!',
            port = '5432'
        )
        return con
    except OperationalError as e:
        print(e)

connection = make_connection()