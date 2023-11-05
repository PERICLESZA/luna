import streamlit as st
from Services.database import get_db_connection

def get_all_bank(nTipo):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM Bank ORDER BY name')
        classes = [(id, name) for (id, name) in cursor.fetchall()]
        conn.close()
        if nTipo == 0:
            classes.append([0, '<<New>>'])
        else:    
            classes.append([0, 'Select class...'])
    
        st.write(classes)        
        classes.sort(key=lambda x:x[1])
        
        return classes
    
    return []

def get_det_bank(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Bank WHERE id = %s", (id,))
        id_data = cursor.fetchone()
        conn.close()
        if id_data:
            return id_data
    return None

def update_bank(bank):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Bank SET name = %s WHERE id = %s", (bank.name, bank.id))
        conn.commit()
        conn.close()

def insert_bank(bank):
    try:
        # Gere a consulta SQL dinamicamente
        sql = "INSERT INTO Bank ("
        valores_sql = []
        campos_do_modelo = [attr for attr in dir(bank) if not callable(getattr(bank, attr)) and not attr.startswith("__")]
        for campo in campos_do_modelo:
            valor_do_campo = getattr(bank,campo)
            sql += f"{campo}, "
            valores_sql.append(valor_do_campo)
        sql = sql.rstrip(", ")  # Remova a última vírgula
        
        # Execute a consulta SQL
        valores = tuple(getattr(bank, campo) for campo in campos_do_modelo)
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

def delete_bank(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Bank WHERE id ='+ str(id))
        conn.commit()
        conn.close()
