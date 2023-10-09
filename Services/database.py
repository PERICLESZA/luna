import streamlit as st
import mysql.connector
from mysql.connector import Error

try:
    cnxn = mysql.connector.connect(
        host='mysql.cedroinfo.com.br',
        port='3306',
        database='cedroibr7',
        user='cedroibr7',
        password='Acd3590t',
        connect_timeout= 520)
    
    if cnxn.is_connected():
        db_info = cnxn.get_server_info()
        print("Conectado com MySQL Server version ", db_info)
        cursor = cnxn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Você está conectado com obanco de dados:  ", record)
        
except Error as e:
    print("Erro enquanto se conectava ao MySQL", e)
    
# Função que executa uma consulta SQL
def execute_query(sql_query):
    # Conectar ao banco de dados
    db = mysql.connector.connect(
        host='mysql.cedroinfo.com.br',
        port='3306',
        database='cedroibr7',
        user='cedroibr7',
        password='Acd3590t',
        connect_timeout= 520
    )
   
    # Usar um cursor dentro de um bloco 'with'
    with db.cursor() as cursor:
        # Executar a consulta SQL
        cursor.execute(sql_query)

        # Ler os resultados
        results = cursor.fetchall()

    # A conexão será fechada automaticamente quando sair do bloco 'with'
    return results