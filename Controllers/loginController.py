import bcrypt
import streamlit as st
from Services.database import get_db_connection

def get_all_login(nTipo):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT idlogin, nome, active, email, login, perfil, senha FROM login ORDER BY nome')
        classes = [(idlogin, nome, active, email, login,  perfil, senha)
                   for (idlogin, nome, active, email, login, perfil, senha) in cursor.fetchall()]
        conn.close()
        if nTipo == 0:
            classes.append([0, '<<New>>', 0])
        else:    
            classes.append([0, 'Select login...', 0])
        classes.sort(key=lambda x:x[1])
        return classes
    return []

def get_det_login(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT idlogin, active, email, login, nome, perfil, senha FROM login WHERE idlogin = %s", (id,))
        id_data = cursor.fetchone()
        conn.close()
        if id_data:
            return id_data
    return None

def update_login(login):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""UPDATE login 
                       SET active = %s, email = %s, login = %s, nome = %s, perfil = %s, senha = %s 
                       WHERE idlogin = %s""",
                       (login.active, login.email, login.login, login.nome, login.perfil, login.senha, login.idlogin))
        conn.commit()
        conn.close()

def insert_login(login):
    try:
        # Gere a consulta SQL dinamicamente
        sql = "INSERT INTO login ("
        valores_sql = []
        campos_do_modelo = [attr for attr in dir(login) if not callable(getattr(login, attr)) and not attr.startswith("__")]
        for campo in campos_do_modelo:
            valor_do_campo = getattr(login,campo)
            sql += f"{campo}, "
            valores_sql.append(valor_do_campo)
        sql = sql.rstrip(", ")  # Remova a última vírgula
        
        # Execute a consulta SQL
        valores = tuple(getattr(login, campo) for campo in campos_do_modelo)
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
        cursor.execute('DELETE FROM login WHERE idlogin ='+ str(id))
        conn.commit()
        conn.close()

def verify_login(login):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT login, senha, perfil  FROM login WHERE login = %s", (login,))
        id_data = cursor.fetchone()
        conn.close()
        if id_data:
            return id_data
    return None

def check_password(input_password, hashed_password):
    # Certifique-se de que hashed_password está em formato de bytes
    hashed_password_bytes = hashed_password.encode(
        'utf-8') if isinstance(hashed_password, str) else hashed_password
    # Verifique se a senha corresponde ao hash
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password_bytes)
