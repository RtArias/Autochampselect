import os
import pyautogui
from PIL import Image
import time
import threading
import tkinter as tk
from tkinter import messagebox
import requests
import sys
import zipfile
from io import BytesIO

# Configuración del repositorio de GitHub
GITHUB_USER = "RtArias" 
GITHUB_REPO = "Autochampselect" 
CURRENT_VERSION = "v0.1" 

# Lista de imágenes adicionales para detener el autoclick
imagenes_para_detener = [
    os.path.join(os.path.dirname(__file__), "imagen1.png"),
    os.path.join(os.path.dirname(__file__), "imagen2.png")
]

def check_for_update():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        release_data = response.json()
        latest_version = release_data["tag_name"]

        if latest_version != CURRENT_VERSION:
            print(f"Actualización disponible: {latest_version}")
            download_url = release_data["assets"][0]["browser_download_url"]
            download_and_update(download_url, latest_version)
        else:
            print("Ya tienes la última versión.")
    else:
        print("No se pudo verificar la última versión. Verifica tu conexión.")

def download_and_update(download_url, latest_version):
    print("Descargando la nueva versión...")
    response = requests.get(download_url)
    if response.status_code == 200:

        with zipfile.ZipFile(BytesIO(response.content)) as z:
            extraction_path = os.path.dirname(sys.executable)
            z.extractall(extraction_path)
            print(f"Actualización completada a la versión {latest_version}.")
            restart_program()
    else:
        print("No se pudo descargar la nueva versión.")

def restart_program():
    print("Reiniciando el programa...")
    os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == "__main__":
    check_for_update()

ruta_imagen = os.path.join(os.path.dirname(__file__), "cartel.png")

autoclick_activo = False

def verificar_imagen(ruta_imagen):
    """Verifica si la imagen existe, tiene permisos correctos y es válida."""
    try:
        if not os.path.exists(ruta_imagen):
            print(f"Error: La imagen '{ruta_imagen}' no existe.")
            return False
        img = Image.open(ruta_imagen)
        img.verify()
        print(f"Imagen '{ruta_imagen}' cargada correctamente.")
        return True
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        return False

def detener_si_imagen_detectada():
    """Detiene el autoclick si una de las imágenes especificadas aparece en pantalla."""
    global autoclick_activo
    for imagen in imagenes_para_detener:
        if verificar_imagen(imagen):
            try:
                if pyautogui.locateOnScreen(imagen, confidence=0.8):
                    print(f"Imagen encontrada: {imagen}. Deteniendo autoclick...")
                    autoclick_activo = False
                    return True
            except Exception as e:
                print(f"Error al buscar la imagen para detener: {e}")
    return False

def click_slow_download():
    """Busca y hace clic en el botón 'ACEPTAR' mientras autoclick esté activo."""
    global autoclick_activo

    if not verificar_imagen(ruta_imagen):
        messagebox.showerror("Error", "La imagen no es válida o no existe.")
        return

    while autoclick_activo:
        if detener_si_imagen_detectada():
            break

        try:
            print("Buscando el botón 'ACEPTAR'...")
            button_location = pyautogui.locateOnScreen(ruta_imagen, confidence=0.8)
            if button_location:
                pyautogui.click(pyautogui.center(button_location))
                print("Hizo clic en el botón 'ACEPTAR'")
                time.sleep(5) 
            else:
                print("Botón no encontrado, buscando nuevamente...")
            time.sleep(1) 
        except Exception as e:
            print(f"Error al buscar el botón: {e}")
            time.sleep(2)  

def iniciar_autoclick():
    """Activa el autoclick en un hilo separado."""
    global autoclick_activo
    if not autoclick_activo:
        autoclick_activo = True
        threading.Thread(target=click_slow_download, daemon=True).start()
        print("Autoclick activado.")

def detener_autoclick():
    """Desactiva el autoclick."""
    global autoclick_activo
    autoclick_activo = False
    print("Autoclick desactivado.")

def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Auto champ select v0.1")
    ventana.geometry("300x200")

    etiqueta = tk.Label(ventana, text="Aceptar automaticamente", font=("Arial", 14))
    etiqueta.pack(pady=10)

    boton_activar = tk.Button(ventana, text="Activar ", font=("Arial", 12),
                              bg="green", fg="white", command=iniciar_autoclick)
    boton_activar.pack(pady=5)

    boton_desactivar = tk.Button(ventana, text="Desactivar ", font=("Arial", 12),
                                 bg="red", fg="white", command=detener_autoclick)
    boton_desactivar.pack(pady=5)

    ventana.mainloop()

crear_interfaz()
