import os
import requests
from bs4 import BeautifulSoup

def fetch_folders(base_url):
    for attempt in range(3):
        try:
            response = requests.get(base_url)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            print("Attempt {} failed: {}".format(attempt + 1, e))
            if attempt == 2:
                return []
    
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    folders = []
    
    for link in soup.find_all('a'):
        folder_name = link.get('href')
        if folder_name and folder_name.endswith('/'):
            folders.append(folder_name.strip('/'))
    return folders

def download_data(selected_folder):
    base_url = "http://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/"
    folder_url = os.path.join(base_url, selected_folder)
    response = requests.get(folder_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    zip_files = [link.get('href') for link in soup.find_all('a') if link.get('href').endswith('.zip')]
    
    if not zip_files:
        print("No zip files found in the selected folder.")
        return
    
    for zip_file in zip_files:
        zip_file_url = os.path.join(folder_url, zip_file)
        if not os.path.exists("csv_files"):
            os.makedirs("csv_files")
        zip_file_path = os.path.join("csv_files", zip_file)
        zip_response = requests.get(zip_file_url)
        with open(zip_file_path, 'wb') as f:
            f.write(zip_response.content)
        print("Downloaded {}".format(zip_file_path))
