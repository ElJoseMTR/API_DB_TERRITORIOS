import mysql.connector


connection = None  

def connect_db():
    global connection
    connection = mysql.connector.connect(
    host="146.59.154.144",
    user="u1250_gWqIzBon87",
    password="HNqGHD+TXd9ecIIlLIR^r9k5",
    database="s1250_territoriossantuario",
    port=3306,
    charset="utf8mb4",
    collation="utf8mb4_unicode_ci",
    
)

        

def get_connection():
    if connection is None or not connection.is_connected():
        connect_db()
    return connection

def close_connection():
    global connection
    if connection and connection.is_connected():
        connection.close()
