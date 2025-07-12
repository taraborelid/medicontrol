from .connectiondb import Connectiondb

class Farmaco():

    def __init__(self, nombre, descripcion, tipo, farmaco_id=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.tipo = tipo
        self.farmaco_id = farmaco_id

    def __str__(self):
        return f'Farmaco[{self.nombre},{self.descripcion},{self.tipo}]'
    
def guardar_farmaco(farmaco):
    conn = Connectiondb()
    
    sql_guardar_farmaco = f'''
        INSERT INTO farmaco(nombre, descripcion, tipo) VALUES (?, ?, ?);
'''
    
    try:
        conn.cursor.execute(sql_guardar_farmaco, (farmaco.nombre, farmaco.descripcion, farmaco.tipo))
        conn.connection.commit()
        conn.close_connection()
    except Exception as e:
        return f'Error al insertar valores en la tabla Farmaco: {e}'

def listar_farmaco():
    conn = Connectiondb()

    sql_listar_farmaco = f'''
    SELECT * FROM farmaco;
'''
    try:
        conn.cursor.execute(sql_listar_farmaco)
        listar_genero = conn.cursor.fetchall()
        conn.close_connection()
        return listar_genero
    except Exception as e:
        return f'Error al listar farmaco: {e}'
    
def actualizar_farmaco(farmaco):
    conn = Connectiondb()

    sql_actualizar_farmaco = f'''
    UPDATE farmaco SET nombre = ?, descripcion = ?, tipo = ? WHERE farmaco_id = ?;
'''
    try:
        conn.cursor.execute(sql_actualizar_farmaco,(farmaco.nombre, farmaco.descripcion, farmaco.tipo, farmaco.farmaco_id))
        conn.connection.commit()
        conn.close_connection
    except Exception as e:
        return f'Error al actualizar farmaco: {e}'
    
def eliminar_farmaco(id):
    conn = Connectiondb()

    sql_eliminar_farmaco = '''
    DELETE FROM farmaco WHERE farmaco_id = ?;
'''
    try:
        conn.cursor.execute(sql_eliminar_farmaco, (id,))
        conn.connection.commit()
        conn.close_connection
    except Exception as e:
        return f'Error al eliminar farmaco: {e}'


