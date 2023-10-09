import streamlit as st
import Services.database as db

def get_items(nTipo):
    db.cursor.execute('SELECT idclasscustomer, description FROM classcustomer ORDER BY description')
    items = db.cursor.fetchall()
    if nTipo == 0:
        items.append([0, '<<New>>'])
    else:    
        items.append([0, ' '])
    items.sort(key=lambda x:x[1])
    return items

def add_or_update_item(classCustomer):
    if classCustomer.idclasscustomer!=0:
        query = 'UPDATE classcustomer SET description = (%s) WHERE idclascustomer = %s'
        db.cursor.execute(query, (classCustomer.description, classCustomer.idclasscustomer))
    else:
        if classCustomer.description:
            query = 'INSERT INTO classcustomer (description) VALUES (%s)'
            db.cursor.execute(query, (classCustomer.description,))
    
def delete_item(item_id):
    db.cursor.execute('DELETE FROM classcustomer WHERE idclasscustomer = '+str(item_id))
    db.cnxn.commit()
    
def get_item_details(item_id):
    db.cursor.execute('SELECT idclasscustomer, description FROM classcustomer WHERE idclasscustomer ='+ str(item_id))
    item_details = db.cursor.fetchone()
    return  item_details