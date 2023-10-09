import streamlit as st
import Services.database as db

def get_items(nTipo):
    db.cursor.execute('SELECT ididentification, nameidentification FROM identification ORDER BY nameidentification')
    items = db.cursor.fetchall()
    if nTipo == 0:
        items.append([0, '<<New>>'])
    else:    
        items.append([0, ' '])
    items.sort(key=lambda x:x[1])
    return items

def add_or_update_item(identification):
    if identification.idcity!=0:
        query = 'UPDATE identification SET nameidentification = (%s) WHERE ididentification = %s'
        db.cursor.execute(query, (identification.nameidentification, identification.ididentification))
    else:
        if identification.nameidentification:
            query = 'INSERT INTO identificationy (nameidentification) VALUES (%s)'
            db.cursor.execute(query, (identification.nameidentification,))
    
def delete_item(item_id):
    db.cursor.execute('DELETE FROM identification WHERE ididentification = '+str(item_id))
    db.cnxn.commit()
    
def get_item_details(item_id):
    db.cursor.execute('SELECT ididentification, nameidentification FROM identification WHERE ididentification ='+ str(item_id))
    item_details = db.cursor.fetchone()
    return  item_details

  
    