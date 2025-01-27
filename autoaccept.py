import pyautogui
import time
import os
import threading

# Ruta de la imagen a buscar
RUTA_IMAGEN = os.path.join(os.path.dirname(__file__), "cartel.png")

# Variable global para controlar el autoclick
autoclick_activo = False

def buscar_y_hacer_click(ruta_imagen, confidence=0.8):
    """Busca una imagen en pantalla y hace clic en ella si se encuentra."""
    try:
        button_location = pyautogui.locateOnScreen(ruta_imagen, confidence=confidence)
        if button_location:
            pyautogui.click(pyautogui.center(button_location))
            return True
        return False
    except Exception as e:
        print(f"Error al buscar la imagen: {e}")
        return False

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
    """Bucle continuo para buscar la imagen y hacer clic mientras el autoclick esté activo."""
    global autoclick_activo
    while autoclick_activo:
        if buscar_y_hacer_click(RUTA_IMAGEN, confidence=0.8):
            print("Imagen detectada y clic realizada.")
        else:
            print("Imagen no encontrada, buscando nuevamente...")
        time.sleep(1)  # Pausa entre intentos

# Para pruebas locales:
if __name__ == "__main__":
    print("Iniciando autoclick...")
    start_autoclick()
    time.sleep(10)  # Tiempo durante el cual el autoclick estará activo
    stop_autoclick()
    print("Autoclick finalizado.")
