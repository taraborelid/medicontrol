# Importaciones necesarias para la interfaz gráfica
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget
from PyQt5.QtCore import Qt
# Importar las ventanas específicas para cada módulo
from .farmaco_view import FarmacoWindow
from .laboratorio_view import LaboratorioWindow
from .medicamento_view import MedicamentoWindow
from PyQt5.QtGui import QIcon, QPixmap

# Ventana principal de la aplicación Medicontrol
class MainWindow(QMainWindow):
    
    def __init__(self):
        
        # Constructor de la ventana principal
        # Configura la interfaz con panel de navegación y área de contenido
        
        super().__init__()
        
        # Configuración básica de la ventana
        self.setWindowTitle("Medicontrol")
        self.setGeometry(200, 200, 1050, 600)  # Posición y tamaño de la ventana
        self.setWindowIcon(QIcon("img/image.png"))  # Icono de la aplicación

        # Widget central y layout principal
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout()  # Layout horizontal para dividir en dos paneles
        central.setLayout(main_layout)

        # ===== PANEL IZQUIERDO (Navegación) =====
        # Crear widget para el panel de navegación con fondo azul claro
        left_widget = QWidget()
        left_widget.setStyleSheet("background-color: #E3F2FD;")
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        left_layout.setContentsMargins(20, 30, 20, 30)  # Márgenes interno
        left_layout.setSpacing(20)  # Espacio entre elementos
        
        # Título de la aplicación
        titulo = QLabel("Medicontrol")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #1976D2; margin-bottom: 30px;")
        left_layout.addWidget(titulo)
        
        # Botones de navegación
        btn_farmacos = QPushButton("Fármacos")
        btn_laboratorios = QPushButton("Laboratorios")
        btn_medicamentos = QPushButton("Medicamentos")
        
        # Estilo CSS para los botones
        estilo_boton = """
            QPushButton {
                background-color: #1976D2;
                color: white;
                border-radius: 4px;
                font-size: 14px;
                padding: 5px 0;
                margin: 6px 0;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:focus {
                border: 2px solid #42A5F5;
            }
        """
        
        # Aplicar estilo y agregar botones al layout
        for btn in [btn_farmacos, btn_laboratorios, btn_medicamentos]:
            btn.setFixedWidth(200)  # Ancho fijo para todos los botones
            btn.setStyleSheet(estilo_boton)
            left_layout.addWidget(btn)
        
        left_layout.addStretch()  # Espacio flexible al final
        main_layout.addWidget(left_widget)  # Agregar panel izquierdo al layout principal

        # ===== PANEL DERECHO (Área de contenido) =====
        # Widget para el área de contenido con fondo blanco
        right_widget = QWidget()
        right_widget.setStyleSheet("background-color: #FFFFFF;")
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(0)
        
        # StackedWidget permite cambiar entre diferentes pantallas
        self.stacked = QStackedWidget()
        
        # ===== PANTALLA DE BIENVENIDA (Placeholder) =====
        # Crear pantalla de bienvenida con imagen
        placeholder = QWidget()
        ph_layout = QVBoxLayout(placeholder)
        ph_layout.addStretch()  # Espacio flexible arriba
        
        # Cargar y mostrar imagen de bienvenida
        img = QLabel()
        pixmap = QPixmap("img/placeholder.png")
        img.setPixmap(pixmap.scaled(220, 220, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        img.setAlignment(Qt.Alignment(Qt.AlignmentFlag.AlignRight) | Qt.Alignment(Qt.AlignmentFlag.AlignBottom))
        ph_layout.addWidget(img)
        
        # ===== CREAR INSTANCIAS DE LAS VENTANAS ESPECÍFICAS =====
        # Cada módulo tiene su propia ventana
        self.farmaco_widget = FarmacoWindow()
        self.laboratorio_widget = LaboratorioWindow()
        self.medicamento_widget = MedicamentoWindow()
        
        # ===== AGREGAR TODAS LAS PANTALLAS AL STACKED WIDGET =====
        # El índice determina qué pantalla se muestra
        self.stacked.addWidget(placeholder)           # index 0 - Pantalla de bienvenida
        self.stacked.addWidget(self.farmaco_widget)   # index 1 - Gestión de fármacos
        self.stacked.addWidget(self.laboratorio_widget) # index 2 - Gestión de laboratorios
        self.stacked.addWidget(self.medicamento_widget) # index 3 - Gestión de medicamentos
        
        right_layout.addWidget(self.stacked)
        main_layout.addWidget(right_widget, stretch=1)  # stretch=1 hace que ocupe más espacio

        # ===== CONEXIONES DE EVENTOS =====
        # Conectar los botones con las pantallas correspondientes
        btn_farmacos.clicked.connect(lambda: self.stacked.setCurrentIndex(1))
        btn_laboratorios.clicked.connect(lambda: self.stacked.setCurrentIndex(2))
        btn_medicamentos.clicked.connect(lambda: self.stacked.setCurrentIndex(3))

        # ===== CONFIGURACIÓN INICIAL =====
        # Mostrar la pantalla de bienvenida al iniciar la aplicación
        self.stacked.setCurrentIndex(0)
