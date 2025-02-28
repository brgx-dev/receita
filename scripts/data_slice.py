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

        try:
            for file_path in files:
                print(f"Processing file: {file_path}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            output_file.write(line)
                            line_count += 1
                            if line_count >= 1000000:
                                output_file.close()
                                print(f"Created file with {line_count} lines, moving to next file.")
                                file_index += 1
                                line_count = 0
                                output_file_path = os.path.join(folder_path, f"{str(file_index).zfill(3)}_{folder_key}.csv")
                                print(f"Creating new output file: {output_file_path}")
                                output_file = open(output_file_path, 'w')
                    print(f"Finished processing file: {file_path}")
                except UnicodeDecodeError:
                    with open(file_path, 'r', encoding='ISO-8859-1') as f:
                        for line in f:
                            output_file.write(line)
                            line_count += 1
                            if line_count >= 1000000:
                                output_file.close()
                                print(f"Created file with {line_count} lines, moving to next file.")
                                file_index += 1
                                line_count = 0
                                output_file_path = os.path.join(folder_path, f"{str(file_index).zfill(3)}_{folder_key}.csv")
                                print(f"Creating new output file: {output_file_path}")
                                output_file = open(output_file_path, 'w')
                    print(f"Finished processing file: {file_path} with ISO-8859-1 encoding")
        finally:
            output_file.close()

        # Delete original files
        for file_path in files:
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

if __name__ == "__main__":
    slice_files()
