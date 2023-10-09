import streamlit as st
import Services.database as db

def get_items(nTipo):
    sql_query = 'SELECT idcity, name_city FROM city ORDER BY name_city'
    items = db.execute_query(sql_query)
    #items = db.cursor.fetchall()
    if nTipo == 0:
        items.append([0, '<<New>>'])
    else:    
        items.append([0, ' '])
    items.sort(key=lambda x:x[1])
    return items


def add_or_update_item(city):
    if city.idcity!=0:
        query = 'UPDATE city SET name_city = (%s) WHERE idcity = %s'
        db.cursor.execute(query, (city.name_city, city.idcity))
    else:
        if city.name_city:
            query = 'INSERT INTO city (name_city) VALUES (%s)'
            db.cursor.execute(query, (city.name_city,))
    
def delete_item(item_id):
    db.cursor.execute('DELETE FROM city WHERE idcity = '+str(item_id))
    db.cnxn.commit()
    
def get_item_details(item_id):
    # st.write(item_id)
    db.cursor.execute('SELECT idcity, name_city FROM city WHERE idcity ='+ str(item_id))
    item_details = db.cursor.fetchone()
    return  item_details

  
    