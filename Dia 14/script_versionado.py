# Script para crear una nueva versión de un depósito en Zenodo

import requests
import os
from dotenv import load_dotenv

URL = "https://sandbox.zenodo.org/api/deposit/depositions"

load_dotenv()
TOKEN = os.getenv("Token_Zenodo_Sandbox")
if not TOKEN:
    print("La variable de entorno 'TOKEN' no esta configurada.")
    exit(1)

cabeceras_json = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

cabeceras_archivo = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/octet-stream'
}

# ID del depósito original ya publicado
DEPOSITO_ORIGINAL_ID = "570557"

try:
    url_version = f"{URL}/{DEPOSITO_ORIGINAL_ID}/actions/newversion"
    r = requests.post(url_version, headers=cabeceras_json)
    
    print(f"Código de estado del servidor: {r.status_code}")
    
    if r.status_code == 201:
        print("Nueva versión generada con éxito.")
        data = r.json()
        url_nuevo_borrador = data['links']['latest_draft']
        
        # Hacemos un GET para obtener los datos (ID y bucket) de este nuevo borrador
        r_detalles = requests.get(url_nuevo_borrador, headers=cabeceras_json)
        nuevo_deposito_data = r_detalles.json()
        nuevo_id = nuevo_deposito_data['id']
        nuevo_bucket = nuevo_deposito_data['links']['bucket']
        
        print(f"Nuevo depósito borrador creado con ID: {nuevo_id}")
        
        url_archivos_borrador = f"{URL}/{nuevo_id}/files"
        r_files = requests.get(url_archivos_borrador, headers=cabeceras_json)
        
        if r_files.status_code == 200:
            archivos_heredados = r_files.json()
            for archivo_viejo in archivos_heredados:
                file_id = archivo_viejo['id']
                url_borrar_archivo = f"{URL}/{nuevo_id}/files/{file_id}"
                r_del = requests.delete(url_borrar_archivo, headers=cabeceras_json)
                if r_del.status_code == 204:
                    print(f"Archivo heredado eliminado correctamente del borrador.")
        
        nuevo_archivo = "fichero_nuevo.txt"
        with open(nuevo_archivo, "wb") as f:
            f.write(b"Contenido de prueba para el Zenodo Sandbox.")

        url_subida = f"{nuevo_bucket}/{nuevo_archivo}"

        with open(nuevo_archivo, "rb") as fp:
            r_file = requests.put(url_subida, data=fp, headers=cabeceras_archivo)

        if r_file.status_code in [200, 201]:
            print("Fichero subido correctamente al bucket.")
        else:
            print(f"Error al subir fichero: {r_file.text}")
            exit(1)
            
        r_publicacion = requests.post(f"{URL}/{nuevo_id}/actions/publish", headers=cabeceras_json)
        if r_publicacion.status_code == 202:
            print("Depósito publicado oficialmente en Zenodo Sandbox.")
            print(f"Enlace web: {r_publicacion.json().get('links', {}).get('html', 'No disponible')}")
        else:
            print(f"Error al publicar: {r_publicacion.text}")
                        
    else:
        print(f"El servidor rechazó la petición de versionado: {r.text}")
        exit(1)

except Exception as e:
    print(f"Error inesperado: {e}")
    exit(1)