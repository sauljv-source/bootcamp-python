# Script de subida de datos/metadatos a Zenodo (POST Y PUT)

import requests
import os
from dotenv import load_dotenv
from pathlib import Path

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

# Cabecera específica para flujo de datos binarios (no json)
cabeceras_archivo = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/octet-stream'
}

# Creamos el post donde subir archivo + metadatos

try:
    r = requests.post(URL,json={}, headers=cabeceras_json)
    print(f"Código de estado del servidor: {r.status_code}")
    if r.status_code == 201:
        print("Recurso en Zenodo Sandbox generado con exito.")
        data = r.json()
        data_id = data['id']
        data_url = data['links']['bucket']
        print(f"Depósito creado con éxito. ID: {data_id}")
    else:
        print(f"El servidor rechazó la petición: {r.text}")
        exit(1)
except Exception as e:
    print(f"Error inesperado: {e}")

# Subimos el archivo a post creado

# Primero creamos el fichero si no existe y escribimos algo de informacion
archivo = "fichero_prueba.txt"
with open(archivo, "wb") as f:
    f.write(b"Contenido de prueba para el Zenodo Sandbox.")

url_subida = f"{data_url}/{archivo}"

with open(archivo, "rb") as fp:
    r_file = requests.put(url_subida, data=fp, headers=cabeceras_archivo)

if r_file.status_code in [200, 201]:
    print("Fichero subido correctamente al bucket.")
else:
    print(f"Error al subir fichero: {r_file.text}")
    exit(1)

# Subimos los metadatos del archivo

# Escribimos los metadatos
metadata = {
  "metadata": {
    "title": "Granular gas of rotating disks: trajectory data of N=25 particles in a circular confinement at packing fraction 0.25",
    "description": "Trajectory data from a granular gas experiment with rotating disk particles driven by air flow. The dataset contains particle positions (x, y) and orientation angle (theta) for N=25 particles at packing fraction 0.25. Recordings were performed at 900 fps using a high-speed camera. The data is provided in CSV format with one file per experimental condition. The confinement is circular with a diameter of 0.725 m.",
    "access_right": "open",
    "upload_type": "dataset",
    "license": "cc-by-4.0",
    "language": "eng",
    "keywords": [
      "granular matter",
      "active matter",
      "chiral active matter",
      "rotating disks",
      "particle tracking",
      "granular gas",
      "packing fraction",
      "quasi-2D",
      "trajectory data"
    ],
    "creators": [
      {
        "name": "Jimenez Vela, Saul",
        "affiliation": "Universidad de Extremadura",
        "orcid": "0009-0002-2923-7047"
      }
    ]
}
}

r_metadata = requests.put(f"{URL}/{data_id}", headers=cabeceras_json, json=metadata)
if r_metadata.status_code == 200:
    print("Metadatos grabados correctamente.")
else:
    print(f"Error al actualizar metadatos: {r_metadata.text}")
    exit(1)

# Publicamos

r_publicacion = requests.post(f"{URL}/{data_id}/actions/publish", headers=cabeceras_json)
if r_publicacion.status_code == 202:
    print("\nDepósito publicado oficialmente en Zenodo Sandbox.")
    print(f"Enlace web: {r_publicacion.json().get('links', {}).get('html', 'No disponible')}")
else:
    print(f"Error al publicar: {r_publicacion.text}")