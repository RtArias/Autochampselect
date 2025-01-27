import sys
import pyautogui
import psutil
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QMessageBox, QApplication, QScrollArea, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon

class ChampionSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selecciona tu Campeón")
        self.setGeometry(100, 100, 800, 600)

        # Crear un área de desplazamiento
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Crear un widget contenedor para los botones
        self.button_container = QWidget()
        self.layout = QGridLayout(self.button_container)

        # Lista de campeones
        self.champions = [
            "AatroxSquare.webp", "Ahri_OriginalSquare.webp", "AkaliSquare.webp", "Akshan_OriginalSquare.webp", "AlistarSquare.webp", "AmumuSquare.webp", "AniviaSquare.webp", "AnnieSquare.webp", "Aphelios_OriginalSquare.webp", "AsheSquare.webp", "Aurelion_SolSquare.webp", "Aurora_OriginalSquare.webp", "AzirSquare.webp", "BardSquare.webp", "Bel%27Veth_OriginalSquare.webp", "BlitzcrankSquare.webp", "BrandSquare.webp", "BraumSquare.webp", "Briar_OriginalSquare.webp", "Caitlyn_OriginalSquare.webp", "CamilleSquare.webp", "CassiopeiaSquare.webp", "Cho%27GathSquare.webp", "CorkiSquare.webp", "DariusSquare.webp", "DianaSquare.webp", "Dr._Mundo_OriginalSquare.webp", "DravenSquare.webp", "EkkoSquare.webp", "EliseSquare.webp", "EvelynnSquare.webp", "EzrealSquare.webp", "Fiddlesticks_OriginalSquare.webp", "FioraSquare.webp", "FizzSquare.webp", "GalioSquare.webp", "GangplankSquare.webp", "GarenSquare.webp", "GnarSquare.webp", "GragasSquare.webp", "GravesSquare.webp", "Gwen_OriginalSquare.webp", "Hecarim_OriginalSquare.webp", "HeimerdingerSquare.webp", "Hwei_OriginalSquare.webp", "IllaoiSquare.webp", "IreliaSquare.webp", "Ivern_OriginalSquare.webp", "JannaSquare.webp", "Jarvan_IVSquare.webp", "Jax_OriginalSquare.webp", "Jayce_OriginalSquare.webp", "Jhin_OriginalSquare.webp", "JinxSquare.webp", "K%27Sante_OriginalSquare.webp", "Kai%27SaSquare.webp", "KalistaSquare.webp", "KarmaSquare.webp", "KarthusSquare.webp", "Kassadin_OriginalSquare.webp", "KatarinaSquare.webp", "Kayle_OriginalSquare.webp", "KaynSquare.webp", "KennenSquare.webp", "Kha%27ZixSquare.webp", "Kindred_OriginalSquare.webp", "KledSquare.webp", "Kog%27MawSquare.webp", "LeBlancSquare.webp", "Lee_Sin_OriginalSquare.webp", "LeonaSquare.webp", "Lillia_OriginalSquare.webp", "LissandraSquare.webp", "LucianSquare.webp", "LuluSquare.webp", "LuxSquare.webp", "MalphiteSquare.webp", "MalzaharSquare.webp", "MaokaiSquare.webp", "Master_YiSquare.webp", "Milio_OriginalSquare.webp", "Miss_Fortune_OriginalSquare.webp", "Mordekaiser_OriginalSquare.webp", "MorganaSquare.webp", "Naafiri_OriginalSquare.webp", "NamiSquare.webp", "NasusSquare.webp", "NautilusSquare.webp", "NeekoSquare.webp", "NidaleeSquare.webp", "Nilah_OriginalSquare.webp", "NocturneSquare.webp", "Nunu_OriginalSquare.webp", "OlafSquare.webp", "OriannaSquare.webp", "OrnnSquare.webp", "Pantheon_OriginalSquare.webp", "PoppySquare.webp", "Pyke_OriginalSquare.webp", "Qiyana_OriginalSquare.webp", "QuinnSquare.webp", "RakanSquare.webp", "RammusSquare.webp", "Rek%27SaiSquare.webp", "Rell_OriginalSquare.webp", "Renata_Glasc_OriginalSquare.webp", "RenektonSquare.webp", "RengarSquare.webp", "RivenSquare.webp", "RumbleSquare.webp", "RyzeSquare.webp", "Samira_OriginalSquare.webp", "SejuaniSquare.webp", "Senna_OriginalSquare.webp", "Seraphine_OriginalSquare.webp", "Sett_OriginalSquare.webp", "Shaco_OriginalSquare.webp", "ShenSquare.webp", "ShyvanaSquare.webp", "SingedSquare.webp", "SionSquare.webp", "Sivir_OriginalSquare.webp", "Skarner_OriginalSquare.webp", "Smolder_OriginalSquare.webp", "SonaSquare.webp", "SorakaSquare.webp", "SwainSquare.webp", "SylasSquare.webp", "Syndra_OriginalSquare.webp", "Tahm_KenchSquare.webp", "TaliyahSquare.webp", "TalonSquare.webp", "TaricSquare.webp", "Teemo_OriginalSquare.webp", "ThreshSquare.webp", "TristanaSquare.webp", "TrundleSquare.webp", "TryndamereSquare.webp", "Twisted_FateSquare.webp", "TwitchSquare.webp", "Udyr_OriginalSquare.webp", "UrgotSquare.webp", "VarusSquare.webp", "VayneSquare.webp", "VeigarSquare.webp", "Vel%27KozSquare.webp", "Vex_OriginalSquare.webp", "Viego_OriginalSquare.webp", "ViktorSquare.webp", "ViSquare.webp", "VladimirSquare.webp", "Volibear_OriginalSquare.webp", "WarwickSquare.webp", "WukongSquare.webp", "XayahSquare.webp", "XerathSquare.webp", "Xin_ZhaoSquare.webp", "YasuoSquare.webp", "Yone_OriginalSquare.webp", "YorickSquare.webp", "Yuumi_OriginalSquare.webp", "ZacSquare.webp", "ZedSquare.webp", "Zeri_OriginalSquare.webp", "ZiggsSquare.webp", "ZileanSquare.webp", "Zoe_OriginalSquare.webp", "ZyraSquare.webp",
            
        ]
        
        for i, champion in enumerate(self.champions):
            button = QPushButton()
            pixmap = QPixmap(f"champions/{champion}")

            if pixmap.isNull():
                print(f"No se pudo cargar la imagen: champions/{champion}")
                continue

            icon = QIcon(pixmap)
            button.setIcon(icon)
            button.setIconSize(pixmap.size() / 2)  # Hacer el icono más pequeño
            button.setFixedSize(50, 50)  # Establecer un tamaño fijo para los botones
            self.layout.addWidget(button, i // 10, i % 10)

            # Conectar el clic del botón a la función que busca y hace clic en la imagen
            button.clicked.connect(lambda checked, champ=champion: self.find_and_click_image(champ))

        # Establecer el widget contenedor en el área de desplazamiento
        scroll_area.setWidget(self.button_container)

        # Establecer el layout principal
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def is_process_running(self, process_name):
        """Verifica si un proceso específico está en ejecución."""
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == process_name:
                return True
        return False

    def find_and_click_image(self, champion):
        # Verificar si el proceso específico está en ejecución
        if not self.is_process_running("LeagueClientUx.exe"):  
            QMessageBox.warning(self, "Proceso no encontrado", "El proceso no está en ejecución.")
            return

        # Buscar la imagen en la pantalla
        location = pyautogui.locateOnScreen(f"champions/{champion}", confidence=0.8)

        if location is not None:
            # Si se encuentra la imagen, hacer clic en su centro
            pyautogui.click(location)
            QMessageBox.information(self, "Éxito", f"Hice clic en {champion} en la pantalla.")
        else:
            QMessageBox.warning(self, "No encontrado", f"No se pudo encontrar {champion} en la pantalla.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChampionSelector()
    window.show()
    sys.exit(app.exec_())