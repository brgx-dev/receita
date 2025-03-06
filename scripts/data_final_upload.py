import os
import psycopg2
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)

def connect_to_db():
    """Connect to the PostgreSQL database using environment variables."""
    load_dotenv()  # Load environment variables from .env file
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def upload_csv_to_db():
    """Upload CSV files to the PostgreSQL database."""
    connection = connect_to_db()
    cursor = connection.cursor()
    
    # Set session replication role
    cursor.execute("SET session_replication_role = 'replica';")
    os.chdir('upload_files')

    for folder in sorted(os.listdir()):
        if os.path.isdir(folder):
            os.chdir(folder)
            table_name = folder  # Use folder name as table name
            for file in sorted(os.listdir(), key=lambda x: x):
                if file.endswith('.csv'):
                    logging.info(f"Processing folder: {folder}, file: {file}")  # Log the current folder and file
                    # Use copy_from method to upload the CSV data with FORCE QUOTE
                    with open(file, 'r') as f:
                        cursor.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV DELIMITER ';' QUOTE '\"' NULL '' FORCE_NULL (*)", f)
                    connection.commit()
            # Log the upload
            cursor.execute("INSERT INTO import_log (chunk_id, table_name) VALUES (%s, %s)", (1, table_name))  # Assuming chunk_id is 1 for simplicity
            logging.info(f"Finished uploading folder: {folder}")  # Log when the folder upload is complete
            os.chdir('..')  # Go back to upload_files directory

    cursor.close()
    connection.close()

if __name__ == "__main__":
    upload_csv_to_db()
