import streamlit as st
from Services.database import get_db_connection
import pandas as pd

def get_cashflow(idCustomer, campoExtra):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        if campoExtra:
            sql = '''SELECT 
                        idcashflow,
                        DATE_FORMAT(dtcashflow, '%Y/%m/%d') as dtcashflow,
                        TIME_FORMAT(tchaflow, '%H:%i') as tchaflow,
                        check_number,
                        valueflow,
                        centsflow,
                        percentflow,
                        valuepercentflow,
                        cents2flow,
                        valuewire,
                        totalflow,
                        totaltopay,
                        status.description,
                        store.nmstore,
                        fk_idstatus
            FROM cashflow 
            LEFT JOIN status ON cashflow.fk_idstatus = status.idstatus 
            LEFT JOIN store  ON cashflow.fk_idstore = store.idstore 
            WHERE fk_idcustomer = %s '''
        else:
            sql = '''SELECT 
                        idcashflow,
                        DATE_FORMAT(dtcashflow, '%Y/%m/%d') as dtcashflow,
                        TIME_FORMAT(tchaflow, '%H:%i') as tchaflow,
                        check_number,
                        valueflow,
                        centsflow,
                        percentflow,
                        valuepercentflow,
                        cents2flow,
                        valuewire,
                        totalflow,
                        totaltopay,
                        status.description,
                        store.nmstore
            FROM cashflow 
            LEFT JOIN status ON cashflow.fk_idstatus = status.idstatus 
            LEFT JOIN store  ON cashflow.fk_idstore = store.idstore 
            WHERE fk_idcustomer = %s '''

        cursor.execute(sql, (idCustomer,))
        columns = [description[0] for description in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        conn.close()
        return data
    return pd.DataFrame()  # Retorna um DataFrame vazio se a conexão falhar

def get_all_exchange(nTipo, nCompany):
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

def update_exchange(exchange):
    try:
        # Gere a consulta SQL dinamicamente
        sql = "UPDATE cashflow SET "
        valores_sql = []
        campos_do_modelo = [attr for attr in dir(exchange) if not callable(getattr(exchange, attr)) and not attr.startswith("__")]
        for campo in campos_do_modelo:
            valor_do_campo = getattr(exchange,campo)
            sql += f"{campo} = %s, "
            valores_sql.append(valor_do_campo)
        sql = sql.rstrip(", ")  # Remova a última vírgula
        sql += f" WHERE idcashflow = {exchange.idcashflow}"
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

def insert_exchange(exchange):
    try:
        # Gere a consulta SQL dinamicamente
        sql = "INSERT INTO cashflow ("
        valores_sql = []
        campos_do_modelo = [attr for attr in dir(exchange) if not callable(
            getattr(exchange, attr)) and not attr.startswith("__")]
        for campo in campos_do_modelo:
            valor_do_campo = getattr(exchange, campo)
            sql += f"{campo}, "
            valores_sql.append(valor_do_campo)
        sql = sql.rstrip(", ")  # Remova a última vírgula

        # Execute a consulta SQL
        valores = tuple(getattr(exchange, campo) for campo in campos_do_modelo)
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
        st.error(f"Erro ao inserir dados: {str(e)}")

def delete_exchange(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cashflow WHERE idcashflow =' + str(id))
        conn.commit()
        conn.close()

def get_cashflow_rp(start_date, end_date, customer_code, status_filter, store_filter):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        sql2 = ""
        sql3 = ""
        sql4 = ""
        
        params = [start_date, end_date, 
                  customer_code, customer_code, customer_code,
                  status_filter, status_filter, status_filter,
                  store_filter, store_filter, store_filter, ]

        # 'Id', 'Date', 'Time', 'Check', 'Value', 'Cents1', 'pComiss', 'Comiss', 'Cents2',
        # 'Wire', 'Reciev', 'Pay', 'Name', 'Ok', 'Status', 'Store'

        sql = """
            SELECT
            cashflow.idcashflow, 
            CAST(cashflow.dtcashflow AS CHAR) AS dtcashflow,
            CAST(cashflow.tchaflow  AS CHAR)  AS dtchaflow, 
            customer.name, 
            cashflow.check_number, 
            cashflow.valueflow, 
            cashflow.centsflow, 
            cashflow.percentflow, 
            cashflow.valuepercentflow, 
            cashflow.cents2flow, 
            cashflow.valuewire, 
            cashflow.totalflow, 
            cashflow.totaltopay, 
            cashflow.cashflowok,                         
            status.description 
            FROM cashflow 
            INNER JOIN customer ON cashflow.fk_idcustomer = customer.idcustomer 
            LEFT JOIN status ON cashflow.fk_idstatus = status.idstatus 
            LEFT JOIN store ON cashflow.fk_idstore = store.idstore
            WHERE cashflow.dtcashflow BETWEEN %s AND %s 
            AND (((cashflow.fk_idcustomer = %s) OR (%s IS NULL) or (%s = 0) )
            AND ((cashflow.fk_idstatus = %s) OR (%s IS NULL) or (%s = 0))
            AND ((cashflow.fk_idstore = %s) OR (%s IS NULL) or (%s = 0)))
            """

        # if customer_code > 0:
        #     sql2 = " AND (cashflow.fk_idcustomer = %s OR %s IS NULL) "
        # if status_filter > 0:
        #     sql3 = "AND (cashflow.fk_idstatus = %s OR %s IS NULL)"
        # if store_filter > 0:
        #    sql4 = "AND (cashflow.fk_idstore = %s OR %s IS NULL)"

        # if customer_code == 0 and status_filter == 0 and store_filter == 0:
        #     params = [start_date, end_date]
        # elif customer_code == 0 and status_filter > 0:
        #     params = [start_date, end_date, status_filter]
        # elif customer_code > 0 and status_filter == 0:
        #     params = [start_date, end_date, customer_code]

        sql = sql #+ sql2 + sql3 + sql4

        print(sql)
        print(params)
        # Execute a consulta SQL e obtenha o DataFrame resultante
        cursor.execute(sql, params)
        columns = [description[0] for description in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        conn.close()
        return data
    return pd.DataFrame()  # Retorna um DataFrame vazio se a conexão falhar