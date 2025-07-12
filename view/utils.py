from PyQt5.QtWidgets import QMessageBox
from model.connectiondb import Connectiondb

def seleccionar_fila(tabla, parent, entidad="elemento"):
    selected_rows = tabla.selectionModel().selectedRows()
    if not selected_rows or tabla.currentRow() == -1:
        QMessageBox.warning(parent, "Selecciona", f"Debes seleccionar un {entidad} para editar.")
        return None
    return selected_rows[0].row() # se devuelve la fila seleccionada

def confirmar_eliminacion(parent, entidad="elemento"):
    respuesta = QMessageBox.question(
        parent,
        "Confirmar eliminación",
        f"¿Estás seguro que deseas eliminar el {entidad}?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No # el boton no esta seleccionado por defecto
    )
    return respuesta == QMessageBox.Yes

def foreign_key_en_uso(id, entidad_id = "elemento"):
    """
    Verifica si un valor de columna (farmaco_id o laboratorio_id) está en uso en la tabla medicamento.
    """
    # Retorna True si el farmaco está en uso en medicamentos
    conn = Connectiondb()
    cursor = conn.cursor
    cursor.execute(f"SELECT COUNT(*) FROM medicamento WHERE {entidad_id} = ?", (id,))
    count = cursor.fetchone()[0]
    conn.close_connection()
    return count > 0

def foreigne_key_necesarias():
    """
    Retorna True si hay al menos un fármaco y al menos un laboratorio cargado.
    """
    conn = Connectiondb()
    cursor = conn.cursor
    cursor.execute("SELECT COUNT(*) FROM farmaco")
    farmaco_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM laboratorio")
    laboratorio_count = cursor.fetchone()[0]
    conn.close_connection()
    return farmaco_count > 0 and laboratorio_count > 0
