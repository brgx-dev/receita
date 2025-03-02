import os
import psycopg2
import pandas as pd

from dotenv import load_dotenv

def connect_to_db():
    """Connect to the PostgreSQL database using environment variables."""
    load_dotenv()  # Load environment variables from .env file
    env_vars = {
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_PORT": os.getenv("DB_PORT"),
        "DB_USER": os.getenv("DB_USER"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD"),
        "DB_NAME": os.getenv("DB_NAME"),
    }
    try:
        connection = psycopg2.connect(
            dbname=env_vars['DB_NAME'],
            user=env_vars['DB_USER'],
            password=env_vars['DB_PASSWORD'],
            host=env_vars['DB_HOST'],
            port=env_vars['DB_PORT']
        )
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def get_last_uploaded_file(cursor):
    """Retrieve the last uploaded file from the import_log table."""
    cursor.execute("SELECT table_name FROM import_log ORDER BY timestamp DESC LIMIT 1;")
    result = cursor.fetchone()
    return result[0] if result else None

def get_table_columns(table_name):
    """Retrieve column names from the SQL file."""
    with open('../sql/data.sql', 'r') as file:
        sql_content = file.read()
    # Assuming the SQL file contains a CREATE TABLE statement
    # Extract column names based on the table_name
    columns = []
    lines = sql_content.splitlines()
    inside_table = False
    for line in lines:
        line = line.strip()
        if line.startswith(f"CREATE TABLE IF NOT EXISTS {table_name}"):
            inside_table = True
        elif inside_table and line.startswith(");"):
            break
        elif inside_table and line and not line.startswith("--"):
            column_definition = line.split()[0]  # Get the column name
            columns.append(column_definition)
    return columns

def upload_csv_to_db():
    """Upload CSV files to the PostgreSQL database."""
    connection = connect_to_db()
    if connection is None:
        return

    cursor = connection.cursor()
    last_uploaded_file = get_last_uploaded_file(cursor)

    os.chdir('upload_files')
    for folder in os.listdir():
        if os.path.isdir(folder):
            for file in os.listdir(folder):
                if file.endswith('.csv'):
                    file_number, table_name = file.split('_', 1)
                    table_name = table_name[:-4]  # Remove .csv extension
                    if last_uploaded_file and last_uploaded_file >= file:
                        continue  # Skip already uploaded files

                    columns = get_table_columns(table_name)
                    df = pd.read_csv(os.path.join(folder, file))

                    print(f"Preparing to upload {file} to {table_name}...")
                    print("Loading...")
                    total_rows = df.shape[0]
                    for index, row in df.iterrows():
                        # Use COPY command to upload the CSV file
                        try:
                            cursor.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER DELIMITER ';'", f)
                            print(f"Successfully uploaded {file} to {table_name}.")
                            print(f"Total rows uploaded: {df.shape[0]}")
                            print(f"Current table: {table_name}")
                            print(f"Processing next file...\n")
                        except Exception as e:
                            print(f"Error uploading {file}: {e}")
                        # Update loading progress
                        print(f"Loading... {((index + 1) / total_rows) * 100:.2f}% complete")
                    connection.commit()

    cursor.close()
    connection.close()

if __name__ == "__main__":
    upload_csv_to_db()
