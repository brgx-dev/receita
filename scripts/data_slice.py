import os
import glob

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

def slice_files():
    upload_dir = 'upload_files'
    
    for folder_name, folder_key in file_table_mapping.items():
        folder_path = os.path.join(upload_dir, folder_key)
        if not os.path.exists(folder_path):
            continue
        
        # Get all files in the folder
        files = glob.glob(os.path.join(folder_path, '*'))
        line_count = 0
        file_index = 1
        output_file_path = os.path.join(folder_path, f"{str(file_index).zfill(3)}_{folder_key}.csv")
        output_file = open(output_file_path, 'w')
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='ISO-8859-1') as f:
                for line in f:
                    output_file.write(line)
                    line_count += 1
                    
                    # Check if we reached 2M lines
                    if line_count >= 2000000:
                        output_file.close()
                        file_index += 1
                        line_count = 0
                        output_file_path = os.path.join(folder_path, f"{str(file_index).zfill(3)}_{folder_key}.csv")
                        print(f"Creating new output file: {output_file_path}")
                        output_file = open(output_file_path, 'w')
        
        output_file.close()
        
        # Delete original files
        for file_path in files:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
