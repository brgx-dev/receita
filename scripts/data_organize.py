import os
import shutil

# Define the mapping of file suffixes to folder names
file_table_mapping = {
    ".EMPRECSV": "empresas",
    ".ESTABELE": "estabelecimentos",
    ".SOCIOCSV": "socios",
    ".SIMPLES.CSV": "simples",
    ".CNAECSV": "cnae",
    ".MOTICSV": "motivo",
    ".MUNICCSV": "municipio",
    ".NATJUCSV": "natureza",
    ".PAISCSV": "pais",
    ".QUALSCSV": "qualificacao",
}

def organize_files():
    upload_directory = 'upload_files'
    
    # Scan the upload_files directory
    for file_suffix, folder_name in file_table_mapping.items():
        # Create the folder if it doesn't exist
        folder_path = os.path.join(upload_directory, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # Check for files containing the suffix
        matching_files = [f for f in os.listdir(upload_directory) if file_suffix in f]
        for file_name in matching_files:
            file_path = os.path.join(upload_directory, file_name)
            print(f"Moving {file_name} to {folder_name} folder.")
            shutil.move(file_path, folder_path)

if __name__ == "__main__":
    organize_files()
