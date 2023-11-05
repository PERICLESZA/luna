import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='mysql.cedroinfo.com.br',
            port='3306',
            database='cedroibr7',
            user='cedroibr7',
            password='Acd3590t'
        )
        return connection
    except Exception as e:
        print(f"Erro na conexão com o banco de dados: {e}")
        return None
