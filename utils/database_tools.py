from utils.connection_util import connection

def reset_databases():
    sql = """
        drop table account;
        drop table client;
        create table client(
	        client_id int primary key generated always as identity,
            first_name varchar(24),
            last_name varchar(24)
        );
        create table account (
	        account_id int primary key generated always as identity,
	        owner_id int,
	        balance int,
	        account_type varchar(25),
	    constraint fk_account_owner foreign key (owner_id) references client(client_id)
        );
    """

    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()

reset_databases()