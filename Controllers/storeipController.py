import streamlit as st
from Services.database import get_db_connection

def get_all_storeip(nTipo):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        if nTipo == 4:
            cursor.execute("""SELECT storeip.ipstore, store.nmstore
                                FROM storeip
                                JOIN store ON storeip.idstore = store.idstore;""")
        else:
            cursor.execute('SELECT ipstore, idstore FROM storeip ORDER BY idstore')
        
        classes = [(ipstore, idstore)
                   for (ipstore, idstore) in cursor.fetchall()]
        conn.close()
        if nTipo == 0:
            classes.append(['<<New>>', 0])
        elif nTipo == 1:    
            classes.append(['Select IP storeip...', 0 ])
        classes.sort(key=lambda x:str(x[1]))
        return classes
    return []

def get_det_storeip(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ipstore, idstore FROM storeip WHERE ipstore = %s", (id,))
        id_data = cursor.fetchone()
        conn.close()
        if id_data:
            return id_data
    return None

def update_storeip(storeip, ipOrigin):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        
        cursor.execute("UPDATE storeip SET ipstore = %s, idstore = %s  WHERE ipstore = %s",
                       (storeip.ipstore, storeip.idstore, ipOrigin))
        conn.commit()
        conn.close()

def insert_storeip(storeip):
    try:
        # Gere a consulta SQL dinamicamente
        sql = "INSERT INTO storeip ("
        valores_sql = []
        campos_do_modelo = [attr for attr in dir(storeip) if not callable(getattr(storeip, attr)) and not attr.startswith("__")]
        for campo in campos_do_modelo:
            valor_do_campo = getattr(storeip,campo)
            sql += f"{campo}, "
            valores_sql.append(valor_do_campo)
        sql = sql.rstrip(", ")  # Remova a última vírgula
        
        # Execute a consulta SQL
        valores = tuple(getattr(storeip, campo) for campo in campos_do_modelo)
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

def delete_storeip(storeip):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM storeip WHERE ipstore =' +
                       storeip.ipstore + ' and idstore =' + str(storeip.idstore))
        conn.commit()
        conn.close()
