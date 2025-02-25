import os
import requests
import zipfile  # Import zipfile module
from tqdm import tqdm
import psycopg2  # Import psycopg2 for PostgreSQL connection
from data_handler import handle_data_menu
from db_connection import handle_db_menu

def main():
    while True:
        print("1 - Download Dados da Receita")
        print("2 - Extrair Dados da Receita")
        print("3 - Configurar a Conexão com o Postgres")
        print("3 - Exit")
        choice = input("Select an option: ")
        if choice == '1':
            handle_data_menu()
        elif choice == '2':
            handle_db_menu()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
