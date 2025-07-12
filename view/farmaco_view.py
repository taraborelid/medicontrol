from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit, QMessageBox, QDialog, QFormLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from model import farmaco_dao
from view.utils import confirmar_eliminacion, seleccionar_fila, foreign_key_en_uso

# Ventana para la gestión de fármacos
class FarmacoWindow(QWidget):
    
    
    def __init__(self):
        # Constructor  que onfigura la interfaz con tabla y botones de acción
       
        super().__init__()
        
        # Configuración básica de la ventana
        self.setWindowTitle("Gestión de Fármacos")
        self.setGeometry(200, 200, 500, 400)  # Posición y tamaño
        
        # Layout principal (vertical)
        layout = QVBoxLayout()
        self.setLayout(layout)

        
        # Crear tabla para mostrar los fármacos
        self.table = QTableWidget()
        self.table.setColumnCount(4)  # 4 columnas: ID, Nombre, Descripción, Tipo
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción", "Tipo"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)  # Seleccionar filas completas
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # No permitir edición directa
        layout.addWidget(self.table)

        # Botones de accion
        # Layout horizontal para los botones
        btn_layout = QHBoxLayout()
        
        # Crear botones para las operaciones CRUD
        self.btn_add = QPushButton("Agregar")
        self.btn_edit = QPushButton("Editar")
        self.btn_delete = QPushButton("Eliminar")
        
        # Agregar botones al layout horizontal
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)

        # CSS para personalizar la apariencia de los botones
        estilo_botones = """
            QPushButton {
                background-color: #1976D2;
                color: white;
                border-radius: 4px;
                font-size: 13px;
                padding: 4px 0;
                margin: 2px 8px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QPushButton:focus {
                border: 2px solid #42A5F5;
            }
        """
        
        # Aplicar estilo a todos los botones
        self.btn_add.setStyleSheet(estilo_botones)
        self.btn_edit.setStyleSheet(estilo_botones)
        self.btn_delete.setStyleSheet(estilo_botones)

        # Conectar los botones con sus funciones correspondientes
        self.btn_add.clicked.connect(self.agregar_farmaco)
        self.btn_edit.clicked.connect(self.editar_farmaco)
        self.btn_delete.clicked.connect(self.eliminar_farmaco)

        
        self.cargar_farmacos()
        

    # Funcion para listar los farmacos
    def cargar_farmacos(self):

        farmacos = farmaco_dao.listar_farmaco()
        if isinstance(farmacos, str):
            QMessageBox.critical(self, "Error", farmacos)
            return
        
        # Configurar el número de filas en la tabla
        self.table.setRowCount(len(farmacos))
        
        # Llenar la tabla con los datos de cada fármaco
        for row, farmaco in enumerate(farmacos): 
            self.table.setItem(row, 0, QTableWidgetItem(str(farmaco[0])))  # ID
            self.table.setItem(row, 1, QTableWidgetItem(str(farmaco[1])))  # Nombre
            self.table.setItem(row, 2, QTableWidgetItem(str(farmaco[2])))  # Descripción
            self.table.setItem(row, 3, QTableWidgetItem(str(farmaco[3])))  # Tipo

    # Funcion para agregar los farmacos
    def agregar_farmaco(self):
       
        # Muestra el diálogo de entrada de datos
        dialog = FarmacoDialog(self)
        
        # Si el usuario acepta el diálogo
        if dialog.exec() == QDialog.Accepted:
            nombre, descripcion, tipo = dialog.get_data() # obtenemos los datos ingresados
            f = farmaco_dao.Farmaco(nombre, descripcion, tipo) # creamos el objeto 
            farmaco_dao.guardar_farmaco(f) # lo guardamos en la base de datos
            
            # Actualizamos los datos
            self.cargar_farmacos()
            
    # funcion para editar farmacos
    def editar_farmaco(self):
        
        row = seleccionar_fila(self.table, self, "farmaco") # validamos si se selecciono una fila
        if row is None:
            return
        nombre = self.table.item(row, 1).text() # Obtenemos los datos de la tabla seleccionada
        descripcion = self.table.item(row, 2).text() 
        tipo = self.table.item(row, 3).text() 
        farmacos = farmaco_dao.listar_farmaco() # obteneemos una lista de todos los farmacos
        farmaco_id = farmacos[row][0] # de la lista de farmacos, buscamnos la id de la fila que hemos seleccionado
        dialog = FarmacoDialog(self, nombre, descripcion, tipo) # Crear y mostrar el diálogo con los datos actuales
        
        
        if dialog.exec() == QDialog.Accepted: # Si el usuario acepta los cambios
            n, d, t = dialog.get_data() # Obtener los nuevos datos
            f = farmaco_dao.Farmaco(n, d, t, farmaco_id) # Crear objeto Farmaco actualizado y guardarlo
            farmaco_dao.actualizar_farmaco(f)
            self.cargar_farmacos() # cargamos la tabla para mostrar los datos
    
    # funcion para eliminar el farmaco
    def eliminar_farmaco(self):
        
        row = seleccionar_fila(self.table, self, "farmaco")
        if row is None:
            return
        if not confirmar_eliminacion(self, "farmaco"): # confirmacion para la eliminacion
            return
        farmacos = farmaco_dao.listar_farmaco()
        farmaco_id = farmacos[row][0]
        if foreign_key_en_uso(farmaco_id, "farmaco_id"): # Verificar si el fármaco está siendo usado en medicamentos
            QMessageBox.warning(self, "No permitido", "No se puede eliminar el fármaco porque está siendo utilizado en medicamentos.")
            return
        farmaco_dao.eliminar_farmaco(farmaco_id)
        self.cargar_farmacos()


class FarmacoDialog(QDialog):
    """
    Diálogo para agregar o editar un fármaco
    Ventana emergente con campos para ingresar los datos del fármaco
    """
    
    def __init__(self, parent=None, nombre="", descripcion="", tipo=""): 
        """
        Constructor del diálogo
        Args:
            parent: Ventana padre
            nombre: Nombre del fármaco (para edición)
            descripcion: Descripción del fármaco (para edición)
            tipo: Tipo del fármaco (para edición)
        """
        super().__init__(parent)    
        
        # Configuración básica del diálogo
        self.setWindowTitle("Fármaco") #setWindowTitle es el titulo de la ventana
        layout = QFormLayout(self) #QFormLayout es el layout de la ventana
        self.nombre = QLineEdit(nombre) #QLineEdit es el campo de texto de la ventana
        self.descripcion = QLineEdit(descripcion) 
        self.tipo = QLineEdit(tipo) 
        
        # ===== AGREGAR CAMPOS AL LAYOUT =====
        layout.addRow("Nombre:", self.nombre) #addRow es el metodo para agregar un campo a la ventana
        layout.addRow("Descripción:", self.descripcion) 
        layout.addRow("Tipo:", self.tipo) 
        
        # ===== BOTONES DEL DIÁLOGO =====
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel) #QDialogButtonBox es el boton de la ventana
        buttons.accepted.connect(self.accept) #accept es el metodo para aceptar la ventana
        buttons.rejected.connect(self.reject) #reject es el metodo para rechazar la ventana
        layout.addWidget(buttons) #addWidget es el metodo para agregar un boton a la ventana
    
    def get_data(self): #get_data es el metodo para obtener los datos de la ventana
        return self.nombre.text(), self.descripcion.text(), self.tipo.text() 

