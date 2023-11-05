from Services.database import get_db_connection

def get_all_ids(nTipo):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT ididentification, nameidentification FROM identification ORDER BY nameidentification')
        ids = [(ididentification, nameidentification) for (ididentification, nameidentification) in cursor.fetchall()]
        conn.close()
        if nTipo == 0:
            ids.append([0, '<<New>>'])
        else:    
            ids.append([0, ' '])
        ids.sort(key=lambda x:x[1])
        return ids
    return []

def get_det_identification(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ididentification, nameidentification FROM identification WHERE ididentification = %s", (id,))
        id_data = cursor.fetchone()
        conn.close()
        if id_data:
            return id_data
    return None

def update_identification(identification):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE identification SET nameidentification = %s WHERE ididentification = %s", (identification.nameidentification, identification.ididentification))
        conn.commit()
        conn.close()

def insert_identification(nameidentification):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO identification (nameidentification) VALUES (%s)", (nameidentification,))
        conn.commit()
        conn.close()

def delete_identification(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM identification WHERE ididentification ='+ str(id))
        conn.commit()
        conn.close()
