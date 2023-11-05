import streamlit as st
from Services.database import get_db_connection

def get_all_customers(nTipo, nCompany):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        sql = 'SELECT idcustomer, CONCAT(name , " - " ,  phone) as name FROM customer WHERE LENGTH(name)>0 AND LENGTH(phone)>0 ORDER BY name'
        cursor.execute(sql)
        customers = [(idcustomer, name) for (idcustomer, name) in cursor.fetchall()]
        conn.close()
        if nTipo == 0:
            customers.append([0, '<<New>>'])
        else:    
            customers.append([0, ' '])
        customers.sort(key=lambda x:x[0])
        return customers
    return []

def update_customer(customer):
    try:
        # Gere a consulta SQL dinamicamente
        sql = "UPDATE customer SET "
        valores_sql = []
        campos_do_modelo = [attr for attr in dir(customer) if not callable(getattr(customer, attr)) and not attr.startswith("__")]
        for campo in campos_do_modelo:
            valor_do_campo = getattr(customer,campo)
            sql += f"{campo} = %s, "
            valores_sql.append(valor_do_campo)
        sql = sql.rstrip(", ")  # Remova a última vírgula
        sql += f" WHERE idcustomer = {customer.idcustomer}"
        # Execute a consulta SQL
        print(sql)
        print(valores_sql)
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(sql, valores_sql)
            conn.commit()
            conn.close()

    except Exception as e:
        print(str(e))
        st.error(f"Erro ao atualizar dados: {str(e)}")
    
def get_det_customer(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor = conn.cursor(dictionary=True)  # Use dictionary=True para obter resultados como dicionários
        cursor.execute("SELECT * FROM customer WHERE idcustomer = %s", (id,))
        city_data = cursor.fetchone()
        conn.close()
        if city_data:
            return city_data
    return None    

def insert_customer(customer):
    try:
        # Gere a consulta SQL dinamicamente
        sql = "INSERT INTO customer ("
        valores_sql = []
        campos_do_modelo = [attr for attr in dir(customer) if not callable(getattr(customer, attr)) and not attr.startswith("__")]
        for campo in campos_do_modelo:
            valor_do_campo = getattr(customer,campo)
            sql += f"{campo}, "
            valores_sql.append(valor_do_campo)
        sql = sql.rstrip(", ")  # Remova a última vírgula
        
        # Execute a consulta SQL
        valores = tuple(getattr(customer, campo) for campo in campos_do_modelo)
        sql += ") VALUES " + str(valores)
        print(sql)
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
    except Exception as e:
        print(str(e))
        st.error(f"Erro ao atualizar dados: {str(e)}")
