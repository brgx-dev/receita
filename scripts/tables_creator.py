import os
import psycopg2
from dotenv import load_dotenv

def create_tables():
    load_dotenv()
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_port = os.getenv("DB_PORT")

    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_pass,
            port=db_port
        )
        conn.autocommit = True
        cursor = conn.cursor()

        with open("sql/data.sql", "r") as f:
            sql_script = f.read()

        try:
            cursor.execute(sql_script)
            print("Tabelas criadas com sucesso!")
        except (Exception, psycopg2.Error) as error:
            print(f"Erro ao executar o script SQL: {error}")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_tables()
