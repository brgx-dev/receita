import psycopg2
import os
import logging
from psycopg2 import pool
from dotenv import load_dotenv

def load_env_variables():
    """Load environment variables from .env file."""
    load_dotenv()  # Load environment variables from .env file
    env_vars = {
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_PORT": os.getenv("DB_PORT"),
        "DB_USER": os.getenv("DB_USER"),
        "DB_PASS": os.getenv("DB_PASS"),
        "DB_NAME": os.getenv("DB_NAME"),
    }
    print("Loaded environment variables:", env_vars)  # Debugging statement
    return env_vars

def handle_db_menu():
    env_vars = load_env_variables()
    host = env_vars.get("DB_HOST")
    port = env_vars.get("DB_PORT")
    user = env_vars.get("DB_USER")
    password = env_vars.get("DB_PASS")
    db_name = env_vars.get("DB_NAME")

    # Prompt for missing environment variables
    if not host:
        host = input("Please enter the database host: ")
    if not port:
        port = input("Please enter the database port: ")
    if not user:
        user = input("Please enter the database user: ")
    if not password:
        password = input("Please enter the database password: ")
    if not db_name:
        db_name = input("Please enter the database name: ")

    # Test the connection
    connection = None
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname='postgres'  # Connect to the default database to create a new database
        )
        connection.autocommit = True  # Set autocommit mode to allow CREATE DATABASE
        print("Connection successful. Checking for database...")
        
        # Check if the database exists, and create it if it does not
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
            try:
                exists = cursor.fetchone()
                if not exists:
                    cursor.execute(f"CREATE DATABASE {db_name}")  # Create the database
                    print(f"Database '{db_name}' created.")
            except psycopg2.errors.InvalidCatalogName:
                cursor.execute(f"CREATE DATABASE {db_name}")
                print(f"Database '{db_name}' created.")
        
        print("All is okay.")
        
        # Save to .env file only if the connection is successful
        with open('.env', 'w') as env_file:
            env_file.write(f"DB_HOST={host}\n")
            env_file.write(f"DB_PORT={port}\n")
            env_file.write(f"DB_USER={user}\n")
            env_file.write(f"DB_PASS={password}\n")
            env_file.write(f"DB_NAME={db_name}\n")

    except Exception as e:
        print("Connection failed. Not saved to .env file.")
        print(f"Error: {e}")
        if "database" in str(e) and "does not exist" in str(e):
            print(f"Database '{db_name}' does not exist. Attempting to create it...")
            # Close the current connection before creating the database
            if connection:
                connection.close()
            # Create a new connection to execute the CREATE DATABASE command
            connection = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                dbname='postgres'  # Connect to the default database to create a new database
            )
            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE {db_name}")
                print(f"Database '{db_name}' created.")
        else:
            print("Connection failed. Not saved to .env file.")
            print(f"Error: {e}")
    finally:
        if connection:
            connection.close()  # Close the connection if it was established

def setup_postgres_table_schema():
    # Function to setup PostgreSQL table schema
    pass

def upload_all_data():
    # Function to upload all data to PostgreSQL
    pass
