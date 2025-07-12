from .connectiondb import Connectiondb

class Medicamento():

    def __init__(self, nombre, presentacion, precio_actual, stock, fecha_vencimiento, farmaco_id, laboratorio_id, medicamento_id=None):
        self.nombre = nombre
        self.presentacion = presentacion
        self.precio_actual = precio_actual
        self.stock = stock
        self.fecha_vencimiento = fecha_vencimiento
        self.farmaco_id = farmaco_id
        self.laboratorio_id = laboratorio_id
        self.medicamento_id = medicamento_id

    def __str__(self):
        return f'medicamento[{self.nombre},{self.farmaco_id},{self.presentacion},{self.precio_actual},{self.stock},{self.fecha_vencimiento},{self.laboratorio_id}]'
    
def guardar_medicamento(medicamento):
    conn = Connectiondb()
    
    sql_guardar_medicamento = f'''
        INSERT INTO medicamento(nombre, presentacion, precio_actual, stock, fecha_vencimiento, farmaco_id, laboratorio_id) VALUES (?, ?, ?, ?, ?, ?, ?);
'''
    
    try:
        conn.cursor.execute(sql_guardar_medicamento, (medicamento.nombre, medicamento.presentacion, medicamento.precio_actual, medicamento.stock, medicamento.fecha_vencimiento, medicamento.farmaco_id, medicamento.laboratorio_id))
        conn.connection.commit()
        conn.close_connection()
    except Exception as e:
        return f'Error al insertar valores en la tabla medicamento: {e}'

def listar_medicamento():
    conn = Connectiondb()

    sql_listar_medicamento = f'''
    SELECT 
        m.medicamento_id AS ID,
        m.nombre AS medicamento,
        f.nombre AS farmaco,
        m.presentacion, 
        m.precio_actual,
        m.stock, 
        m.fecha_vencimiento, 
        l.nombre AS laboratorio
    FROM medicamento as m 
    INNER JOIN farmaco as f ON m.farmaco_id = f.farmaco_id 
    INNER JOIN laboratorio as l ON m.laboratorio_id = l.laboratorio_id
    ;
'''
    try:
        conn.cursor.execute(sql_listar_medicamento)
        listar_genero = conn.cursor.fetchall()
        conn.close_connection()
        return listar_genero
    except Exception as e:
        return f'Error al listar medicamento: {e}'
    
def actualizar_medicamento(medicamento):
    conn = Connectiondb()

    sql_actualizar_medicamento = f'''
    UPDATE medicamento SET nombre = ?, presentacion = ?, precio_actual = ?, stock = ?, fecha_vencimiento = ?, farmaco_id = ?, laboratorio_id = ? WHERE medicamento_id = ?;
'''
    try:
        conn.cursor.execute(sql_actualizar_medicamento,(medicamento.nombre, medicamento.presentacion, medicamento.precio_actual, medicamento.stock,
        medicamento.fecha_vencimiento, medicamento.farmaco_id, medicamento.laboratorio_id, medicamento.medicamento_id))
        conn.connection.commit()
        conn.close_connection()
    except Exception as e:
        return f'Error al actualizar medicamento: {e}'
    
def eliminar_medicamento(id):
    conn = Connectiondb()

    sql_eliminar_medicamento = '''
    DELETE FROM medicamento WHERE medicamento_id = ?;
'''
    try:
        conn.cursor.execute(sql_eliminar_medicamento, (id,))
        conn.connection.commit()
        conn.close_connection()
    except Exception as e:
        return f'Error al eliminar medicamento: {e}'

