import streamlit as st
from Services.database import get_db_connection

def get_all_store(nTipo):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT idstore, nmstore FROM store ORDER BY nmstore')
        classes = [(idstore, nmstore)
                   for (idstore, nmstore) in cursor.fetchall()]
        conn.close()
        if nTipo == 0:
            classes.append([0, '<<New>>', 0])
        elif nTipo == 1:    
            classes.append([0, 'Select store...', 0])
        classes.sort(key=lambda x:x[0])
        return classes
    return []

def get_det_store(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT idstore, nmstore FROM store WHERE idstore = %s", (id,))
        id_data = cursor.fetchone()
        conn.close()
        if id_data:
            return id_data
    return None

def update_store(store):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE store SET nmstore = %s  WHERE idstore = %s",
                       (store.nmstore, store.idstatus))
        conn.commit()
        conn.close()

def insert_store(store):
    try:
        # Gere a consulta SQL dinamicamente
        sql = "INSERT INTO store ("
        valores_sql = []
        campos_do_modelo = [attr for attr in dir(store) if not callable(getattr(store, attr)) and not attr.startswith("__")]
        for campo in campos_do_modelo:
            valor_do_campo = getattr(store,campo)
            sql += f"{campo}, "
            valores_sql.append(valor_do_campo)
        sql = sql.rstrip(", ")  # Remova a última vírgula
        
        # Execute a consulta SQL
        valores = tuple(getattr(store, campo) for campo in campos_do_modelo)
        sql += ") VALUES " + str(valores)
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
    except Exception as e:
        print(str(e))
        st.error(f"Erro ao atualizar dados: {str(e)}")

def delete_status(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM store WHERE idstore ='+ str(id))
        conn.commit()
        conn.close()
