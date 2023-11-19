import streamlit as st
from Services.database import get_db_connection

def get_all_status(nTipo):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT idstatus, description, emphasis FROM status ORDER BY description')
        classes = [(idstatus, description, emphasis)
                   for (idstatus, description, emphasis) in cursor.fetchall()]
        conn.close()
        if nTipo == 0:
            classes.append([0, '<<New>>', 0])
        else:    
            classes.append([0, 'Select status...', 0])
        classes.sort(key=lambda x:x[1])
        return classes
    return []

def get_det_status(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT idstatus, description, emphasis FROM status WHERE idstatus = %s", (id,))
        id_data = cursor.fetchone()
        conn.close()
        if id_data:
            return id_data
    return None

def update_status(status):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE status SET description = %s, emphasis=%s WHERE idstatus = %s",
                       (status.description, status.emphasis, status.idstatus))
        conn.commit()
        conn.close()

def insert_status(status):
    try:
        # Gere a consulta SQL dinamicamente
        sql = "INSERT INTO status ("
        valores_sql = []
        campos_do_modelo = [attr for attr in dir(status) if not callable(getattr(status, attr)) and not attr.startswith("__")]
        for campo in campos_do_modelo:
            valor_do_campo = getattr(status,campo)
            sql += f"{campo}, "
            valores_sql.append(valor_do_campo)
        sql = sql.rstrip(", ")  # Remova a última vírgula
        
        # Execute a consulta SQL
        valores = tuple(getattr(status, campo) for campo in campos_do_modelo)
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
        cursor.execute('DELETE FROM status WHERE idstatus ='+ str(id))
        conn.commit()
        conn.close()
