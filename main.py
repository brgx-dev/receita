from tqdm import tqdm
from scripts.data_handler import handle_data_menu
from scripts.data_unzipper import unzip_data
from scripts.db_connection import handle_db_menu  # Importing the new function

def main():
    try:
        print("Criador do receitaDB iniciado...")  # Debugging statement
        while True: 
            print("1 - Download Dados da Receita")
            print("2 - Extrair Dados da Receita") 
            print("3 - Connectar ao Banco")  # New option
            choice = input("Escolha uma opção: ")
            if choice == '1':
                handle_data_menu()
            elif choice == '2':
                unzip_data()  # Call to unzip_data without parameters
            elif choice == '3':
                handle_db_menu()  # Call to handle_db_menu
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
