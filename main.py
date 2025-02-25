from tqdm import tqdm
from scripts.data_handler import handle_data_menu
from scripts.data_unzipper import unzip_data

def main():
    try:
        print("Criador do receitaDB iniciado...")  # Debugging statement
        while True: 
            print("1 - Download Dados da Receita")
            print("2 - Extrair Dados da Receita") 
            choice = input("Escolha uma opção: ")
            if choice == '1':
                handle_data_menu()
            elif choice == '2':
                unzip_data()  # Call to unzip_data without parameters
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
