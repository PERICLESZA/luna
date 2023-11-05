import streamlit as st
import Services.database as db
from Services.database import get_db_connection

def get_all_classes(nTipo):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT idclasscustomer, description FROM classcustomer ORDER BY description')
        classes = [(idclasscustomer, description) for (idclasscustomer, description) in cursor.fetchall()]
        conn.close()
        if nTipo == 0:
            classes.append([0, '<<New>>'])
        else:    
            classes.append([0, 'Select class...'])
        classes.sort(key=lambda x:x[1])
        return classes
    return []

def delete_item(item_id):
    db.cursor.execute('DELETE FROM classcustomer WHERE idclasscustomer = '+str(item_id))
    db.cnxn.commit()
    
def get_det_class(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT idclasscustomer, description FROM classcustomer WHERE idclasscustomer ='+ str(id))
        city_data = cursor.fetchone()
        conn.close()
        if city_data:
            return city_data
    return None

def update_class(classC):
    print(classC)
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE classcustomer SET description = %s WHERE idclasscustomer = %s", (classC.description, classC.idclasscustomer))
        conn.commit()
        conn.close()

def insert_class(description):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO classcustomer (description) VALUES (%s)", (description,))
        conn.commit()
        conn.close()

def delete_class(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM classcustomer WHERE idclasscustomer ='+ str(id))
        conn.commit()
        conn.close()
