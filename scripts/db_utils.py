import psycopg2
import os

def setup_postgres_connection():
    host = input("Enter the PostgreSQL host: ")
    port = input("Enter the PostgreSQL port: ")
    user = input("Enter the PostgreSQL user: ")
    password = input("Enter the PostgreSQL password: ")
    db_name = input("Enter the PostgreSQL database name: ")

    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=db_name
        )
        print("Connection successful. Checking for database...")
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(f"CREATE DATABASE {db_name}")
                print(f"Database '{db_name}' created.")
        
        print("All is okay.")
        
        with open('.env', 'w') as env_file:
            env_file.write(f"DB_HOST={host}\n")
            env_file.write(f"DB_PORT={port}\n")
            env_file.write(f"DB_USER={user}\n")
            env_file.write(f"DB_PASS={password}\n")
            env_file.write(f"DB_NAME={db_name}\n")

    except Exception as e:
        print("Connection failed. Not saved to .env file.")
        print(f"Error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

def setup_postgres_table_schema():
    pass

def upload_all_data():
    pass
