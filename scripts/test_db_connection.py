from db_connection import connect_to_db

def main():
    # Replace these values with your actual database connection parameters
    host = "157.173.105.102"
    port = 5432
    user = "your_username"  # Replace with your PostgreSQL username
    password = "your_password"  # Replace with your PostgreSQL password
    db_name = "receita"  # The database name to connect to or create

    # Attempt to connect to the database
    connection = connect_to_db(host, port, user, password, db_name)

    if connection:
        # Perform any database operations here
        connection.close()  # Close the connection when done

if __name__ == "__main__":
    main()
