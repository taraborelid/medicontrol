from PyQt5.QtWidgets import QApplication
from view.main_view import MainWindow
from model.tables import create_table, insertar_datos_ejemplo

if __name__ == "__main__":
    import sys
    create_table()
    insertar_datos_ejemplo()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())