import streamlit as st
from Services.database import get_db_connection

def update_parameter(parameter):
    try:
        # Gere a consulta SQL dinamicamente
        sql = "UPDATE parameters SET "
        valores_sql = []
        campos_do_modelo = [attr for attr in dir(parameter) if not callable(getattr(parameter, attr)) and not attr.startswith("__")]
        for campo in campos_do_modelo:
            valor_do_campo = getattr(parameter,campo)
            sql += f"{campo} = %s, "
            valores_sql.append(valor_do_campo)
        sql = sql.rstrip(", ")  # Remova a última vírgula
        # sql += f" WHERE idcustomer = {parameter.idcustomer}"
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
    
def get_det_parameter():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor = conn.cursor(dictionary=True)  # Use dictionary=True para obter resultados como dicionários
        cursor.execute("SELECT * FROM parameters")
        parameter_data = cursor.fetchone()
        conn.close()
        if parameter_data:
            return parameter_data
    return None    