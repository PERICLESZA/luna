import streamlit as st
from Services.database import get_db_connection

def get_all_percentcheck(nTipo):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT                  
                            idpercentcheck,
                            formula,
                            valuereturn,
                            valuereturntype
                          FROM percentcheck ORDER BY idpercentcheck''')
        
        classes = [(idpercentcheck, formula, valuereturn, valuereturntype)
                   for (idpercentcheck, formula, valuereturn, valuereturntype) in cursor.fetchall()]
        conn.close()
        if nTipo == 0:
            classes.append([0, '<<New>>', '', ''])
        elif nTipo == 1:    
            classes.append([0, 'Select percentcheck...', 0, 0])
        classes.sort(key=lambda x:x[0])
        return classes
    return []


def get_det_percentcheck(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT 
                            idpercentcheck, 
                            formula, 
                            valuereturn, 
                            valuereturntype 
                          FROM percentcheck WHERE idpercentcheck = %s""", (id,))
        id_data = cursor.fetchone()
        conn.close()
        if id_data:
            return id_data
    return None

def update_percentcheck(percentcheck):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""UPDATE percentcheck SET 
                            formula = %s, 
                            valuereturn = %s, 
                            valuereturntype = %s 
                          WHERE idpercentcheck = %s""",
                       (percentcheck.formula, 
                        percentcheck.valuereturn, 
                        percentcheck.valuereturntype,
                        percentcheck.idpercentcheck))
        conn.commit()
        conn.close()


def insert_percentcheck(percentcheck):
    try:
        # Gere a consulta SQL dinamicamente
        sql = "INSERT INTO percentcheck ("
        valores_sql = []
        campos_do_modelo = [attr for attr in dir(percentcheck) if not callable(getattr(percentcheck, attr)) and not attr.startswith("__")]
        for campo in campos_do_modelo:
            valor_do_campo = getattr(percentcheck,campo)
            sql += f"{campo}, "
            valores_sql.append(valor_do_campo)
        sql = sql.rstrip(", ")  # Remova a última vírgula
        
        # Execute a consulta SQL
        valores = tuple(getattr(percentcheck, campo) for campo in campos_do_modelo)
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

def delete_percentcheck(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM percentcheck WHERE idstatus ='+ str(id))
        conn.commit()
        conn.close()
