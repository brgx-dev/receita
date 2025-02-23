# db_utils.py

import psycopg2
from psycopg2 import sql
import pandas as pd
from config import DB_CONFIG

def get_connection():
    """Cria e retorna uma conexão com o banco de dados PostgreSQL."""
    return psycopg2.connect(
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"]
    )

def create_table_from_csv(csv_file, table_name):
    """Cria uma tabela no banco de dados a partir do CSV."""
    conn = get_connection()
    cur = conn.cursor()
    
    df = pd.read_csv(csv_file)
    columns = df.columns.tolist()
    
    # Criar a query para criação da tabela
    create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {table} ({columns});").format(
        table=sql.Identifier(table_name),
        columns=sql.SQL(', ').join(map(sql.Identifier, columns))
    )
    
    cur.execute(create_table_query)
    conn.commit()
    
    cur.close()
    conn.close()

def insert_chunk_into_table(df, table_name):
    """Insere um chunk de dados no banco de dados."""
    conn = get_connection()
    cur = conn.cursor()

    for i, row in df.iterrows():
        insert_query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values});").format(
            table=sql.Identifier(table_name),
            columns=sql.SQL(', ').join(map(sql.Identifier, df.columns)),
            values=sql.SQL(', ').join(map(sql.Placeholder, df.columns))
        )
        cur.execute(insert_query, tuple(row))
    
    conn.commit()
    cur.close()
    conn.close()
    
def log_import_progress(chunk_id, table_name):
    """Registra o progresso da importação no banco de dados."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO import_log (chunk_id, table_name)
        VALUES (%s, %s);
    """, (chunk_id, table_name))
    conn.commit()
    cur.close()
    conn.close()
