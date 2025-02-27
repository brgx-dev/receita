import os
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from tqdm import tqdm
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection information
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Create a database connection
def create_db_connection():
    try:
        connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(connection_string)
        connection = engine.connect()
        print("Database connection established.")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Check import log
def check_import_log(connection):
    print("Checking import log...")
    query = "SELECT * FROM import_log"
    return pd.read_sql(query, connection)

# Upload CSV files to the database
def upload_csv_files(connection):
    file_table_mapping = {
        ".EMPRESCSV": "empresas",
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

    print("Starting the upload process for CSV files.")
    for file_suffix, table_name in file_table_mapping.items():
        print(f"Checking for files containing: {file_suffix}")
        matching_files = [f for f in os.listdir('unzipped_csv_files') if file_suffix in f]
        if matching_files:
            for file_path in matching_files:
                print(f"Found file: {file_path}")
        for file_path in matching_files:
            print(f"Processing file: {file_path}")
            for chunk in pd.read_csv(f'unzipped_csv_files/{file_path}', chunksize=50000, on_bad_lines='skip', encoding='ISO-8859-1'):
                print(f"Reading file: {file_path}")
                try:
                    chunk.to_sql(table_name, connection, if_exists='append', index=False)
                    # Log the upload in import_log
                    log_upload(connection, file_suffix, table_name)
                    print(f"Successfully uploaded {file_path} to {table_name}.")
                except pd.errors.ParserError as e:
                    print(f"Error parsing {file_path}: {e}")
                except Exception as e:
                    print(f"Error uploading {file_suffix} to {table_name}: {e}")
                    print("Upload failed.")

# Log the upload in the import_log table
def log_upload(connection, file_suffix, table_name):
    query = f"INSERT INTO import_log (file_name, table_name, upload_time) VALUES ('{file_suffix}', '{table_name}', NOW()) RETURNING id"
    print(f"Executing query: {query}")
    with connection.cursor() as cursor:
        cursor.execute(query)
    connection.commit()

def main():
    connection = create_db_connection()
    if connection:
        print("Connection established, proceeding to upload CSV files.")
        upload_csv_files(connection)
    connection.close()

if __name__ == "__main__":
    main()
