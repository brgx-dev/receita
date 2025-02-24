import os
import requests
import zipfile  # Import zipfile module
from tqdm import tqdm
import psycopg2  # Import psycopg2 for PostgreSQL connection
from data_fetcher import fetch_folders, download_data
from dependency_installer import install_dependencies
from db_utils import setup_postgres_connection, setup_postgres_table_schema, upload_all_data
from data_unzipper import unzip_data

def fetch_folders(base_url):
    # Function to fetch available folders from the base URL
    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(base_url)
            response.raise_for_status()  # Raise an error for bad responses
            break  # Exit the loop if the request was successful
        except requests.exceptions.RequestException as e:
            print("Attempt {} failed: {}".format(attempt + 1, e))
            if attempt == 2:  # Last attempt
                return []  # Return an empty list if all attempts fail
    # Parse the response to extract folder links (this will depend on the HTML structure)
    # For now, let's assume we return a list of folder URLs
    import pandas as pd

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    folders = []
    
    # Assuming the folders are listed in <a> tags within a specific section
    for link in soup.find_all('a'):
        folder_name = link.get('href')
        if folder_name and folder_name.endswith('/'):  # Check if it's a folder
            folders.append(folder_name.strip('/'))  # Remove trailing slash
    return folders

def download_data(selected_folder):
    base_url = "http://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/"
    folder_url = os.path.join(base_url, selected_folder)
    # Fetch the list of zip files in the selected folder
    response = requests.get(folder_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    zip_files = [link.get('href') for link in soup.find_all('a') if link.get('href').endswith('.zip')]
    
    if not zip_files:
        print("No zip files found in the selected folder.")
        return
    
    for zip_file in zip_files:
        zip_file_url = os.path.join(folder_url, zip_file)
    if not os.path.exists("csv_files"):
        os.makedirs("csv_files")  # Create the csv_files directory if it doesn't exist
    zip_file_path = os.path.join("csv_files", zip_file)  # Save to the csv_files directory
    # Ensure the csv_files directory exists
    if not os.path.exists("csv_files"):
        os.makedirs("csv_files")  # Create the csv_files directory if it doesn't exist

    # Use requests to download the files
    for zip_file in zip_files:
        zip_file_url = os.path.join(folder_url, zip_file)
        zip_file_path = os.path.join("csv_files", zip_file)  # Save to the csv_files directory
        
        # Download with progress bar
        with requests.get(zip_file_url, stream=True) as r:
            r.raise_for_status()  # Raise an error for bad responses
            total_size = int(r.headers.get('content-length', 0))
            with open(zip_file_path, 'wb') as f, tqdm(
                desc=zip_file,
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in r.iter_content(chunk_size=1024):
                    size = f.write(data)
                    bar.update(size)
    print("Download completed.")
    # Function to download data from the specified folder URL
    pass

def unzip_data(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall("unzipped_csv_files")  # Change to the specified folder
    print("Unzipped {} to unzipped_csv_files/".format(zip_file_path))

def setup_postgres_connection():
    # Function to setup PostgreSQL connection
    host = input("Enter the PostgreSQL host: ")
    port = input("Enter the PostgreSQL port (default 5436): ")
    if not port or not port.isdigit() or int(port) <= 0:
        port = "5436"  # Set to default if invalid input
    user = input("Enter the PostgreSQL user: ")
    password = input("Enter the PostgreSQL password: ")
    db_name = input("Enter the PostgreSQL database name: ")

    # Test the connection
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=db_name
        )
        print("Connection successful. Checking for database...")
        
        # Check if the database exists, and create it if it does not
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'receita'")
            exists = cursor.fetchone()
            if not exists:
                cursor.execute("CREATE DATABASE receita")
                print("Database 'receita' created.")
        
        print("All is okay.")
        
        print("All is okay.")
        
        # Save to .env file
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
            connection.close()  # Close the connection if it was established

def setup_postgres_table_schema():
    # Function to setup PostgreSQL table schema
    pass

def upload_all_data():
    # Function to upload all data to PostgreSQL
    pass

import platform
import subprocess

def install_dependencies():
    os_type = platform.system()
    if os_type == "Darwin":  # macOS
        subprocess.run(["brew", "install", "postgresql"])
    elif os_type == "Linux":
        subprocess.run(["sudo", "apt", "install", "postgresql"])
    else:
        print("Unsupported OS. Please install PostgreSQL manually.")

def main():
    install_dependencies()
    connection = None  # Initialize connection variable
    choice = None  # Initialize choice variable
    while True:
        print("1 - Download most recent data")
        print("2 - Unzip All Data")
        print("3 - Setup PostgreSQL Connection")  # Add this line to display option 3
        if choice == '3': 
            connection = setup_postgres_connection()
        elif choice == '4':
            if connection:
                create_table(connection)
            else:
                print("Please establish a connection first.")
        elif choice == '5':
            if connection:
                data_frame = pd.read_csv("csv_files/your_data_file.csv")  # Placeholder for actual CSV file
                upload_data_to_db(connection, data_frame)
            else:
                print("Please establish a connection first.")
        print("6 - Exit")
        choice = input("Select an option: ")
        if choice == '6':
            break
        if choice == '1':
            base_url = "http://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/"
            folders = fetch_folders(base_url)
            print("Available folders:")
            for i, folder in enumerate(folders, start=1):
                print("{} - {}".format(i, folder))
            folder_choice = int(input("Select a folder to download: ")) - 1
            if 0 <= folder_choice < len(folders):
                download_data(folders[folder_choice])
            else:
                print("Invalid choice.")
        elif choice == '2':
            # Automatically unzip all zip files in the csv_files directory
            for zip_file in os.listdir("csv_files"):
                if zip_file.endswith(".zip"):
                    zip_file_path = os.path.join("csv_files", zip_file)
                    unzip_data(zip_file_path)

if __name__ == "__main__":
    main()
