from .connectiondb import Connectiondb

class Laboratorio():

    def __init__(self, nombre, direccion, telefono, laboratorio_id=None):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.laboratorio_id = laboratorio_id

    def __str__(self):
        return f'Laboratorio[{self.nombre},{self.direccion},{self.telefono}]'
    
def guardar_laboratorio(laboratorio):
    conn = Connectiondb()
    
    sql_guardar_laboratorio = f'''
        INSERT INTO laboratorio(nombre, direccion, telefono) VALUES (?, ?, ?);
'''
    
    try:
        conn.cursor.execute(sql_guardar_laboratorio, (laboratorio.nombre, laboratorio.direccion, laboratorio.telefono))
        conn.connection.commit()
        conn.close_connection()
    except Exception as e:
        return f'Error al insertar valores en la tabla laboratorio: {e}'

def listar_laboratorio():
    conn = Connectiondb()

    sql_listar_laboratorio = f'''
    SELECT * FROM laboratorio;
'''
    try:
        conn.cursor.execute(sql_listar_laboratorio)
        listar_genero = conn.cursor.fetchall()
        conn.close_connection()
        return listar_genero
    except Exception as e:
        return f'Error al listar laboratorio: {e}'
    
def actualizar_laboratorio(laboratorio):
    conn = Connectiondb()

    sql_actualizar_laboratorio = f'''
    UPDATE laboratorio SET nombre = ?, direccion = ?, telefono = ? WHERE laboratorio_id = ?;
'''
    try:
        conn.cursor.execute(sql_actualizar_laboratorio,(laboratorio.nombre, laboratorio.direccion, laboratorio.telefono, laboratorio.laboratorio_id))
        conn.connection.commit()
        conn.close_connection
    except Exception as e:
        return f'Error al actualizar laboratorio: {e}'
    
def eliminar_laboratorio(id):
    conn = Connectiondb()

    sql_eliminar_laboratorio = '''
    DELETE FROM laboratorio WHERE laboratorio_id = ?;
'''
    try:
        conn.cursor.execute(sql_eliminar_laboratorio, (id,))
        conn.connection.commit()
        conn.close_connection
    except Exception as e:
        return f'Error al eliminar laboratorio: {e}'

