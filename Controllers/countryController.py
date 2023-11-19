import streamlit as st
from Services.database import get_db_connection

def get_all_country(nTipo):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT idcountry, namecountry FROM country ORDER BY namecountry')
        classes = [(idcountry, namecountry)
                   for (idcountry, namecountry) in cursor.fetchall()]
        conn.close()
        if nTipo == 0:
            classes.append([0, '<<New>>'])
        else:    
            classes.append([0, 'Select Country...'])
        classes.sort(key=lambda x:x[1])
        return classes
    return []

def get_det_country(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT idcountry, namecontry FROM country WHERE idcountry = %s", (id,))
        id_data = cursor.fetchone()
        conn.close()
        if id_data:
            return id_data
    return None

def update_country(status):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE country SET namecountry = %s WHERE idcountry = %s",
                       (status.namecountry, status.idcountry))
        conn.commit()
        conn.close()


def insert_country(country):
    try:
        # Gere a consulta SQL dinamicamente
        sql = "INSERT INTO country ("
        valores_sql = []
        campos_do_modelo = [attr for attr in dir(country) if not callable(
            getattr(country, attr)) and not attr.startswith("__")]
        for campo in campos_do_modelo:
            valor_do_campo = getattr(country, campo)
            sql += f"{campo}, "
            valores_sql.append(valor_do_campo)
        sql = sql.rstrip(", ")  # Remova a última vírgula
        
        # Execute a consulta SQL
        valores = tuple(getattr(country, campo) for campo in campos_do_modelo)
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


def delete_country(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM country WHERE idcountry =' + str(id))
        conn.commit()
        conn.close()
