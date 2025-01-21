import os
import pyautogui
from PIL import Image
import time
import threading
import tkinter as tk
from tkinter import messagebox


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


def click_slow_download():
    """Busca y hace clic en el botón 'ACEPTAR' mientras autoclick esté activo."""
    global autoclick_activo

    if not verificar_imagen(ruta_imagen):
        messagebox.showerror("Error", "La imagen no es válida o no existe.")
        return

    while autoclick_activo:
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
    ventana.geometry("300x150")

   
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
