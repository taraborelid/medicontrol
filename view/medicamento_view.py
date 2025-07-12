from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QMessageBox, QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QComboBox, QSpinBox, QDateEdit
from PyQt5.QtCore import Qt, QDate
from model import medicamento_dao, farmaco_dao, laboratorio_dao
from view.utils import confirmar_eliminacion, seleccionar_fila, foreigne_key_necesarias

class MedicamentoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Medicamentos")
        self.setGeometry(200, 200, 800, 400)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Fármaco", "Presentación", "Precio Actual", "Stock", "Fecha Vencimiento", "Laboratorio"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Agregar")
        self.btn_edit = QPushButton("Editar")
        self.btn_delete = QPushButton("Eliminar")
        self.btn_refresh = QPushButton("Actualizar")

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_refresh)

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
        self.btn_refresh.setStyleSheet(estilo_botones)

        self.btn_add.clicked.connect(self.agregar_medicamento)
        self.btn_edit.clicked.connect(self.editar_medicamento)
        self.btn_delete.clicked.connect(self.eliminar_medicamento)
        self.btn_refresh.clicked.connect(self.cargar_medicamentos)

        self.cargar_medicamentos()

    def cargar_medicamentos(self):
        medicamentos = medicamento_dao.listar_medicamento()
        if isinstance(medicamentos, str):
            QMessageBox.critical(self, "Error", medicamentos)
            return
        self.table.setRowCount(len(medicamentos))
        for row, med in enumerate(medicamentos):
            for col, value in enumerate(med):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def agregar_medicamento(self):
        if not foreigne_key_necesarias():
            QMessageBox.warning(self, "No permitido", "No se puede agregar un medicamento sin antes tenes al menos un farmaco y un laboratorio.")
            return
        dialog = MedicamentoDialog(self)
        if dialog.exec() == QDialog.Accepted:
            nombre, presentacion, precio_actual, stock, fecha_vencimiento, farmaco_id, laboratorio_id = dialog.get_data()
            m = medicamento_dao.Medicamento(nombre, presentacion, precio_actual, stock, fecha_vencimiento, farmaco_id, laboratorio_id)
            medicamento_dao.guardar_medicamento(m)
            self.cargar_medicamentos()

    def editar_medicamento(self):
        row = seleccionar_fila(self.table, self, "medicamento")
        if row is None:
            return
        # Obtener datos actuales de la fila
        nombre = self.table.item(row, 1).text()
        farmaco_nombre = self.table.item(row, 2).text()
        presentacion = self.table.item(row, 3).text()
        precio_actual = float(self.table.item(row, 4).text())
        stock = int(self.table.item(row, 5).text())
        fecha_vencimiento = self.table.item(row, 6).text()
        laboratorio_nombre = self.table.item(row, 7).text()
        medicamentos = medicamento_dao.listar_medicamento()
        medicamento_id = medicamentos[row][0]
        dialog = MedicamentoDialog(self, nombre, presentacion, precio_actual, stock, fecha_vencimiento, farmaco_nombre, laboratorio_nombre)
        if dialog.exec() == QDialog.Accepted:
            n, p, precio, s, fv, farmaco_id, laboratorio_id = dialog.get_data()
            m = medicamento_dao.Medicamento(n, p, precio, s, fv, farmaco_id, laboratorio_id, medicamento_id)
            medicamento_dao.actualizar_medicamento(m)
            self.cargar_medicamentos()

    def eliminar_medicamento(self):
        row = seleccionar_fila(self.table, self, "medicamento")
        if row is None:
            return
        if not confirmar_eliminacion(self, "medicamento"):
            return
        medicamentos = medicamento_dao.listar_medicamento()
        medicamento_id = medicamentos[row][0]
        medicamento_dao.eliminar_medicamento(medicamento_id)
        self.cargar_medicamentos()
    

class MedicamentoDialog(QDialog):
    def __init__(self, parent=None, nombre="", presentacion="", precio_actual=0.0, stock=0, fecha_vencimiento="", farmaco_nombre="", laboratorio_nombre=""):
        super().__init__(parent)
        self.setWindowTitle("Medicamento")
        layout = QFormLayout(self)
        self.nombre = QLineEdit(nombre)
        self.presentacion = QLineEdit(presentacion)
        self.precio_actual = QLineEdit(str(precio_actual))
        self.stock = QSpinBox()
        self.stock.setMinimum(0)
        self.stock.setMaximum(1000000)
        self.stock.setValue(stock)
        self.fecha_vencimiento = QDateEdit()
        self.fecha_vencimiento.setCalendarPopup(True)
        if fecha_vencimiento:
            try:
                self.fecha_vencimiento.setDate(QDate.fromString(fecha_vencimiento, "yyyy-MM-dd"))
            except:
                self.fecha_vencimiento.setDate(QDate.currentDate())
        else:
            self.fecha_vencimiento.setDate(QDate.currentDate())
        # ComboBox para fármaco
        self.farmaco_combo = QComboBox()
        self.farmacos = farmaco_dao.listar_farmaco()
        self.farmaco_id_map = {}
        for f in self.farmacos:
            self.farmaco_combo.addItem(f[1])
            self.farmaco_id_map[f[1]] = f[0]
        if farmaco_nombre:
            idx = self.farmaco_combo.findText(farmaco_nombre)
            if idx >= 0:
                self.farmaco_combo.setCurrentIndex(idx)
        # ComboBox para laboratorio
        self.laboratorio_combo = QComboBox()
        self.laboratorios = laboratorio_dao.listar_laboratorio()
        self.laboratorio_id_map = {}
        for l in self.laboratorios:
            self.laboratorio_combo.addItem(l[1])
            self.laboratorio_id_map[l[1]] = l[0]
        if laboratorio_nombre:
            idx = self.laboratorio_combo.findText(laboratorio_nombre)
            if idx >= 0:
                self.laboratorio_combo.setCurrentIndex(idx)
        layout.addRow("Nombre:", self.nombre)
        layout.addRow("Presentación:", self.presentacion)
        layout.addRow("Precio Actual:", self.precio_actual)
        layout.addRow("Stock:", self.stock)
        layout.addRow("Fecha Vencimiento:", self.fecha_vencimiento)
        layout.addRow("Fármaco:", self.farmaco_combo)
        layout.addRow("Laboratorio:", self.laboratorio_combo)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    def get_data(self):
        nombre = self.nombre.text()
        presentacion = self.presentacion.text()
        precio_actual = float(self.precio_actual.text())
        stock = self.stock.value()
        fecha_vencimiento = self.fecha_vencimiento.date().toString("yyyy-MM-dd")
        farmaco_id = self.farmaco_id_map[self.farmaco_combo.currentText()]
        laboratorio_id = self.laboratorio_id_map[self.laboratorio_combo.currentText()]
        return nombre, presentacion, precio_actual, stock, fecha_vencimiento, farmaco_id, laboratorio_id
