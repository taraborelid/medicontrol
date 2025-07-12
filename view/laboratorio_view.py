from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit, QMessageBox, QDialog, QFormLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from model import laboratorio_dao
from view.utils import confirmar_eliminacion, seleccionar_fila, foreign_key_en_uso

class LaboratorioWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Laboratorios")
        self.setGeometry(200, 200, 500, 400)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Direccion", "Telefono"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Agregar")
        self.btn_edit = QPushButton("Editar")
        self.btn_delete = QPushButton("Eliminar")
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)

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
        self.btn_add.setStyleSheet(estilo_botones)
        self.btn_edit.setStyleSheet(estilo_botones)
        self.btn_delete.setStyleSheet(estilo_botones)

        self.btn_add.clicked.connect(self.agregar_laboratorio)
        self.btn_edit.clicked.connect(self.editar_laboratorio)
        self.btn_delete.clicked.connect(self.eliminar_laboratorio)

        self.cargar_laboratorios()

    def cargar_laboratorios(self):
        laboratorios = laboratorio_dao.listar_laboratorio()
        if isinstance(laboratorios, str):
            QMessageBox.critical(self, "Error", laboratorios)
            return
        self.table.setRowCount(len(laboratorios))
        for row, laboratorio in enumerate(laboratorios):
            self.table.setItem(row, 0, QTableWidgetItem(str(laboratorio[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(laboratorio[1])))
            self.table.setItem(row, 2, QTableWidgetItem(str(laboratorio[2])))
            self.table.setItem(row, 3, QTableWidgetItem(str(laboratorio[3])))

    def agregar_laboratorio(self):
        dialog = LaboratorioDialog(self)
        if dialog.exec() == QDialog.Accepted:
            nombre, direccion, telefono = dialog.get_data()
            f = laboratorio_dao.Laboratorio(nombre, direccion, telefono)
            laboratorio_dao.guardar_laboratorio(f)
            self.cargar_laboratorios()

    def editar_laboratorio(self):
        row = seleccionar_fila(self.table, self, "laboratorio")
        if row is None:
            return
        nombre = self.table.item(row, 1).text()
        direccion = self.table.item(row, 2).text()
        telefono = self.table.item(row, 3).text()
        laboratorios = laboratorio_dao.listar_laboratorio()
        laboratorio_id = laboratorios[row][0]
        dialog = LaboratorioDialog(self, nombre, direccion, telefono)
        if dialog.exec() == QDialog.Accepted:
            n, d, t = dialog.get_data()
            l = laboratorio_dao.Laboratorio(n, d, t, laboratorio_id)
            laboratorio_dao.actualizar_laboratorio(l)
            self.cargar_laboratorios()

    def eliminar_laboratorio(self):
        row = seleccionar_fila(self.table, self, "laboratorio")
        if row is None:
            return
        if not confirmar_eliminacion(self, "laboratorio"):
            return
        laboratorios = laboratorio_dao.listar_laboratorio()
        laboratorio_id = laboratorios[row][0]
        if foreign_key_en_uso(laboratorio_id, "laboratorio_id"):
            QMessageBox.warning(self, "No permitido", "No se puede eliminar el laboratorio porque está siendo utilizado en medicamentos.")
            return
        laboratorio_dao.eliminar_laboratorio(laboratorio_id)
        self.cargar_laboratorios()

class LaboratorioDialog(QDialog):
    def __init__(self, parent=None, nombre="", direccion="", telefono=""):
        super().__init__(parent)
        self.setWindowTitle("Laboratorio")
        layout = QFormLayout(self)
        self.nombre = QLineEdit(nombre)
        self.direccion = QLineEdit(direccion)
        self.telefono = QLineEdit(telefono)
        layout.addRow("Nombre:", self.nombre)
        layout.addRow("Direccion:", self.direccion)
        layout.addRow("Telefono:", self.telefono)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    def get_data(self):
        return self.nombre.text(), self.direccion.text(), self.telefono.text()

