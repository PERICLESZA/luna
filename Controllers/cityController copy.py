import streamlit as st
from Services.database import get_db_connection

def get_all_cities(nTipo):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT idcity, name_city FROM city ORDER BY name_city')
        cities = [(idcity, name_city) for (idcity, name_city) in cursor.fetchall()]
        conn.close()
        if nTipo == 0:
            cities.append([0, '<<New>>'])
        else:    
            cities.append([0, ' '])
        cities.sort(key=lambda x:x[1])
        return cities
    return []

def get_item_details(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT idcity, name_city FROM city WHERE idcity = %s", (id,))
        city_data = cursor.fetchone()
        conn.close()
        if city_data:
            return city_data
    return None

def update_city(city):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE city SET name_city = %s WHERE idcity = %s", (city.name_city, city.idcity))
        conn.commit()
        conn.close()

def insert_city(name_city):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO city (name_city) VALUES (%s)", (name_city,))
        conn.commit()
        conn.close()

def delete_city(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM city WHERE idcity ='+ str(id))
        conn.commit()
        conn.close()
