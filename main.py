from tqdm import tqdm
from scripts.data_handler import handle_data_menu
from scripts.data_unzipper import unzip_data
from scripts.db_connection import handle_db_menu
from scripts.tables_creator import create_tables
from scripts.upload_csv_db import main as upload_csv

def main():
    try:
        print("Criador do receitaDB iniciado...")
        while True:
            print("1 - Download Dados da Receita")
            print("2 - Extrair Dados da Receita")
            print("3 - Connectar ao Banco")
            print("4 - Preparar o Banco (tabelas)")
            print("5 - Upload CSVs to DB")
            choice = input("Escolha uma opção: ")
            if choice == '1':
                handle_data_menu()
            elif choice == '2':
                unzip_data()
            elif choice == '3':
                handle_db_menu()
            elif choice == '4':
                create_tables()
            elif choice == '5':
                upload_csv()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
