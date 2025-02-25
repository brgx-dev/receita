import os
import requests
import zipfile
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup

def handle_data_menu():
    base_url = "http://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/"
    while True:
        print("1 - Download most recent data")
        print("2 - Unzip All Data")
        print("3 - Exit")
        choice = input("Select an option: ")
        if choice == '1':
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
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

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

def unzip_data(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall("unzipped_csv_files")  # Change to the specified folder
    print("Unzipped {} to unzipped_csv_files/".format(zip_file_path))
