import os
import psycopg2
import pandas as pd

from db_connection import load_env_variables

def connect_to_db():
    """Connect to the PostgreSQL database using environment variables."""
    env_vars = load_env_variables()
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
    cursor.execute("SELECT file_name FROM import_log ORDER BY upload_time DESC LIMIT 1;")
    result = cursor.fetchone()
    return result[0] if result else None

def get_table_columns(table_name):
    """Retrieve column names from the SQL file."""
    with open('sql/data.sql', 'r') as file:
        sql_content = file.read()
    # Assuming the SQL file contains a CREATE TABLE statement
    # Extract column names based on the table_name
    # This is a placeholder; implement actual parsing logic as needed
    return ['column1', 'column2', 'column3']  # Replace with actual column names

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

                    # Insert data into the database
                    for index, row in df.iterrows():
                        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
                        try:
                            cursor.execute(insert_query, tuple(row))
                            print(f"Successfully uploaded {file} to {table_name}.")
                        except Exception as e:
                            print(f"Error uploading {file}: {e}")

                    # Log the upload
                    cursor.execute("INSERT INTO import_log (folder_name, file_name) VALUES (%s, %s);", (folder, file))
                    connection.commit()

    cursor.close()
    connection.close()

if __name__ == "__main__":
    upload_csv_to_db()
