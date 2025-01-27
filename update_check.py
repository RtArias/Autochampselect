import os
import requests
import sys
import zipfile
from io import BytesIO

GITHUB_USER = "RtArias"
GITHUB_REPO = "Autochampselect"
CURRENT_VERSION = "v0.2"


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

