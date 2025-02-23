# main.py

import os
import pandas as pd
from db_utils import create_table_from_csv, insert_chunk_into_table, log_import_progress

# Configuração
CSV_FOLDER = "csv_files"
CHUNK_SIZE = 1000  # Quantidade de registros por chunk

def process_csv_file(csv_file, table_name):
    """Processa o arquivo CSV e faz a importação em chunks."""
    # Criar a tabela caso não exista
    create_table_from_csv(csv_file, table_name)

    # Ler o arquivo CSV em chunks
    for chunk_id, chunk in enumerate(pd.read_csv(csv_file, chunksize=CHUNK_SIZE)):
        # Inserir chunk no banco de dados
        insert_chunk_into_table(chunk, table_name)
        # Logar o progresso
        log_import_progress(chunk_id, table_name)
        print(f"Chunk {chunk_id} de {table_name} importado com sucesso.")

def import_csv_files():
    """Importa todos os arquivos CSV da pasta configurada."""
    for csv_file in os.listdir(CSV_FOLDER):
        if csv_file.endswith(".csv"):
            table_name = os.path.splitext(csv_file)[0]  # Usando o nome do arquivo como nome da tabela
            print(f"Iniciando importação do arquivo: {csv_file}")
            process_csv_file(os.path.join(CSV_FOLDER, csv_file), table_name)
    print("Importação concluída!")

if __name__ == "__main__":
    import_csv_files()
