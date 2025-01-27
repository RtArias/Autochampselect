import sys
import threading
import time
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton
from champion_selector import ChampionSelector 
from autoaccept import buscar_y_hacer_click  
from update_check import check_for_update  

# Ruta de la imagen que se busca
RUTA_IMAGEN = os.path.join(os.path.dirname(__file__), "cartel.png")

# Variable global para controlar el autoclick
autoclick_activo = False

def start_autoclick():
    """Inicia el autoclick en un hilo separado."""
    global autoclick_activo
    if not autoclick_activo:
        autoclick_activo = True
        threading.Thread(target=autoclick_loop, daemon=True).start()
        print("Autoaccept activado.")

def stop_autoclick():
    """Detiene el autoclick."""
    global autoclick_activo
    autoclick_activo = False
    print("Autoaccept desactivado.")

def autoclick_loop():
    """Bucle continuo para buscar la imagen y hacer clic mientras autoclick esté activo."""
    global autoclick_activo
    while autoclick_activo:
        if buscar_y_hacer_click(RUTA_IMAGEN, confidence=0.8):
            print("Imagen detectada y clic realizada.")
        else:
            print("Imagen no encontrada, buscando nuevamente...")
        time.sleep(1)  # Pausa entre intentos

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Champ Select")
        self.setGeometry(100, 100, 800, 600)

        # Verifica actualizaciones antes de iniciar
        check_for_update()

        # Crea el contenedor de pestañas
        tab_widget = QTabWidget()

        # Pestaña 1: Selección de campeones
        tab_widget.addTab(ChampionSelector(), "Seleccionar Campeón")

        # Pestaña 2: Bloquear Campeón
        block_tab = QWidget()
        block_layout = QVBoxLayout()
        block_tab.setLayout(block_layout)
        tab_widget.addTab(block_tab, "Bloquear Campeón")

        # Pestaña 3: Activar/Desactivar Autoclick
        autoclick_tab = QWidget()
        autoclick_layout = QVBoxLayout()
        start_button = QPushButton("Activar Autoaccept")
        stop_button = QPushButton("Desactivar Autoaccept")
        start_button.clicked.connect(start_autoclick)
        stop_button.clicked.connect(stop_autoclick)
        autoclick_layout.addWidget(start_button)
        autoclick_layout.addWidget(stop_button)
        autoclick_tab.setLayout(autoclick_layout)
        tab_widget.addTab(autoclick_tab, "Autoaccept")

        # Configura el widget central de la ventana
        self.setCentralWidget(tab_widget)


if __name__ == "__main__":
    # Inicializa la aplicación PyQt
    app = QApplication(sys.argv)

    # Crea la ventana principal
    main_window = MainWindow()
    main_window.show()

    # Ejecuta el bucle principal de la aplicación
    sys.exit(app.exec_())
