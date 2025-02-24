import psycopg2
from psycopg2 import sql

def connect_to_db(host, port, user, password, db_name):
    print("Attempting to connect to the database...")
    try:
        # Attempt to connect to the specified database
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=db_name
        )
        print(f"Connected to the database '{db_name}' successfully.")
        print("Connection established.")
        return connection
    except psycopg2.OperationalError as e:
        # Check if the error is due to the database not existing
        if "database does not exist" in str(e):
            print(f"Database '{db_name}' does not exist. Attempting to create it...")
            create_database(host, port, user, password, db_name)  # Create the database if it does not exist
            print(f"Retrying connection to the database '{db_name}' after creation...")
            # Retry connection after creating the database
            return connect_to_db(host, port, user, password, db_name)
        else:
            print(f"Connection failed: {e}")
            return None

def create_database(host, port, user, password, db_name):
    try:
        print(f"Attempting to create database '{db_name}'...")
        # Connect to the default database to create a new one
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname='postgres'  # Connect to the default 'postgres' database
        )
        print("Connection to 'postgres' database established.")
        connection.autocommit = True  # Enable autocommit mode
        cursor = connection.cursor()
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        print(f"Database '{db_name}' created successfully.")
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Failed to create database '{db_name}': {e}")
        print("Error details:", e)
