from tqdm import tqdm
from scripts.data_handler import handle_data_menu
from scripts.data_unzipper import unzip_data
from scripts.db_connection import handle_db_menu
from scripts.tables_creator import create_tables
from scripts.data_organize import organize_files
from scripts.prepare_files_for_upload import run_preparation
from scripts.data_slice import slice_files

def main():
    try:
        print("Criador do receitaDB iniciado...")
        while True:
            print("1 - Download Dados da Receita")
            print("2 - Extrair Dados da Receita")
            print("3 - Connectar ao Banco")
            print("4 - Preparar o Banco (tabelas)")
            print("5 - Preparar os Arquivos para Upload")
            print("6 - Prepara os Arquivos Part II")
            print("7 - Fatiar os Arquivos")
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
                run_preparation()
            elif choice == '6':
                organize_files()
            elif choice == '7':
                slice_files()
                
                
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
