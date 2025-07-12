from .connectiondb import Connectiondb

def create_table():
    conn = Connectiondb()
    
    # Verificar que la conexión se estableció correctamente
    if conn.cursor is None:
        return 'Error: No se pudo establecer conexión con la base de datos'

    sql_farmaco = '''
           CREATE TABLE IF NOT EXISTS farmaco(
           farmaco_id INTEGER PRIMARY KEY AUTOINCREMENT,
           nombre VARCHAR(100),
           descripcion TEXT,
           tipo VARCHAR(100)
           ) 
    ''' 

    sql_laboratorio = '''
           CREATE TABLE IF NOT EXISTS laboratorio(
           laboratorio_id INTEGER PRIMARY KEY AUTOINCREMENT,
           nombre VARCHAR(100),
           direccion VARCHAR(100),
           telefono VARCHAR(100)
           ) 
    ''' 

    sql_medicamento = '''
           CREATE TABLE IF NOT EXISTS medicamento(
           medicamento_id INTEGER PRIMARY KEY AUTOINCREMENT,
           nombre VARCHAR(100),
           presentacion VARCHAR(100),
           precio_actual DECIMAL(10,2),
           stock INT,
           fecha_vencimiento DATE,
           farmaco_id INTEGER,
           laboratorio_id INTEGER,
           FOREIGN KEY (farmaco_id) REFERENCES farmaco(farmaco_id),
           FOREIGN KEY (laboratorio_id) REFERENCES laboratorio(laboratorio_id)
           ) 
    ''' 

    try:
        conn.cursor.execute(sql_farmaco)
        conn.close_connection()
        conn = Connectiondb()
        if conn.cursor is None:
            return 'Error: No se pudo establecer conexión con la base de datos'
        conn.cursor.execute(sql_laboratorio)
        conn.close_connection()
        conn = Connectiondb()
        if conn.cursor is None:
            return 'Error: No se pudo establecer conexión con la base de datos'
        conn.cursor.execute(sql_medicamento)
        conn.close_connection()
        return 'Tablas creadas exitosamente'
    except Exception as e:
        return f'Error al crear las tablas: {e}'

def insertar_datos_ejemplo():
    conn = Connectiondb()
    
    # Verificar que la conexión se estableció correctamente
    if conn.cursor is None:
        return 'Error: No se pudo establecer conexión con la base de datos'
    
    cursor = conn.cursor

    try:
        # FÁRMACOS
        cursor.execute("SELECT COUNT(*) FROM farmaco")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO farmaco (nombre, descripcion, tipo) VALUES ('Paracetamol', 'Analgésico/antipirético', 'Venta Libre')")
            cursor.execute("INSERT INTO farmaco (nombre, descripcion, tipo) VALUES ('Ibuprofeno', 'Antiinflamatorio no esteroideo (AINE)', 'Venta Libre')")
            cursor.execute("INSERT INTO farmaco (nombre, descripcion, tipo) VALUES ('Aspirina (Ácido acetilsalicílico)', 'Analgésico/antipirético/antiinflamatorio', 'Venta Libre')")
            cursor.execute("INSERT INTO farmaco (nombre, descripcion, tipo) VALUES ('Amoxicilina', 'Antibiótico', 'Receta')")
            cursor.execute("INSERT INTO farmaco (nombre, descripcion, tipo) VALUES ('Ciprofloxacino', 'Antibiótico', 'Receta')")
            cursor.execute("INSERT INTO farmaco (nombre, descripcion, tipo) VALUES ('Salbutamol', 'Broncodilatador', 'Receta')")

        # LABORATORIOS
        cursor.execute("SELECT COUNT(*) FROM laboratorio")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO laboratorio (nombre, direccion, telefono) VALUES ('Laboratorio Bagó', 'Av. del Libertador 5200, Buenos Aires', '+54 11 4309 8500')")
            cursor.execute("INSERT INTO laboratorio (nombre, direccion, telefono) VALUES ('Laboratorios Roemmers', 'Av. Pueyrredón 2446, Buenos Aires', '+54 11 4821 0100')")
            cursor.execute("INSERT INTO laboratorio (nombre, direccion, telefono) VALUES ('Laboratorios Raffo', 'Av. Belgrano 2222, Buenos Aires', '+54 11 4389 1000')")
            cursor.execute("INSERT INTO laboratorio (nombre, direccion, telefono) VALUES ('Bayer', 'Kaiser-Wilhelm-Allee 1, Leverkusen', '+49 214 30 1')")

        # MEDICAMENTOS 
        cursor.execute("SELECT COUNT(*) FROM medicamento")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO medicamento (nombre, presentacion, precio_actual, stock, fecha_vencimiento, farmaco_id, laboratorio_id) VALUES ('Paracetamol 500mg', 'Caja', 100, 50, '2025-12-31', 1, 1)")
            cursor.execute("INSERT INTO medicamento (nombre, presentacion, precio_actual, stock, fecha_vencimiento, farmaco_id, laboratorio_id) VALUES ('Ibuprofeno 400mg', 'Comprimidos', 150, 75, '2025-06-30', 2, 2)")
            cursor.execute("INSERT INTO medicamento (nombre, presentacion, precio_actual, stock, fecha_vencimiento, farmaco_id, laboratorio_id) VALUES ('Aspirina 100mg', 'Tabletas', 80, 100, '2025-09-15', 3, 3)")
            cursor.execute("INSERT INTO medicamento (nombre, presentacion, precio_actual, stock, fecha_vencimiento, farmaco_id, laboratorio_id) VALUES ('Amoxicilina 500mg', 'Cápsulas', 200, 30, '2025-03-20', 4, 4)")
            cursor.execute("INSERT INTO medicamento (nombre, presentacion, precio_actual, stock, fecha_vencimiento, farmaco_id, laboratorio_id) VALUES ('Ciprofloxacino 500mg', 'Comprimidos', 180, 25, '2025-07-10', 5, 1)")

        if conn.connection:
            conn.connection.commit()
        conn.close_connection()
        return 'Datos de ejemplo insertados exitosamente'
        
    except Exception as e:
        return f'Error al insertar datos de ejemplo: {e}'