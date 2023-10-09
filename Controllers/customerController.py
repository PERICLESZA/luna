import streamlit as st
import Services.database as db

def get_items(nTipo):

    sql_query = 'SELECT idcustomer, CONCAT(name , " - " ,  phone) as name FROM customer WHERE LENGTH(name)>0 AND LENGTH(phone)>0  ORDER BY name'
    getItems = db.execute_query(sql_query)
    if nTipo == 0:
       getItems.append([0, '<<New>>'])
    else:    
       getItems.append([0, ' '])
    return getItems

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
        # db.execute_query(sql, valores_sql)
        
        db.cursor.execute(sql, valores_sql)

        # Faça o commit da transação
        db.cnxn.commit()

    except Exception as e:
        print(str(e))
        st.error(f"Erro ao atualizar dados: {str(e)}")
    

def add_or_update_item(customer):
    if customer.idcity!=0:
        st.write('update, mas não!')
    else:
        if customer.name:
            query = 'INSERT INTO customer (name, phone) VALUES (%s, %s)'
            db.cursor.execute(query, (customer.name, customer.phone))
    
def delete_item(item_id):
    db.cursor.execute('DELETE FROM customer WHERE idcustomer = '+str(item_id))
    db.cnxn.commit()
    
def get_item_details(item_id):
    
    # try:
        # Crie um cursor para executar consultas SQL
        cur = db.cnxn.cursor(dictionary=True)  # Use dictionary=True para obter resultados como dicionários

        # Consulta SQL para obter os nomes dos campos da tabela
        cur.execute(f"SELECT * FROM customer WHERE idcustomer = %s", (item_id,))

        # Obtenha o registro selecionado como um dicionário
        registro = cur.fetchone()

        # Feche o cursor e a conexão
        cur.close()

        # Retorne o registro
        return registro

    # except Exception as e:
    #     st.error(f"Erro ao obter dados: {str(e)}")
    #     return {}
    