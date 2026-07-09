# Primera prueba de escritura en una url publica con requests
import requests
import pandas as pd

url = 'https://jsonplaceholder.typicode.com/posts'

TOKEN = "token_secreto"

cabeceras = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json; charset=UTF-8'
}

nuevo_post = {
    'userId': 11,
    'id': 'x',
    'title': 'Entrada de Saúl',
    'body': 'Prueba dia 4 de la libreria requests con peticiones POST.',
}

try:
    print("Enviando datos al servidor remoto")
    # Hacemos el POST pasando los datos (json) y las cabeceras de seguridad (headers)
    r = requests.post(url, json=nuevo_post, headers=cabeceras)
    
    # El código de estado 201 significa "Created" (Creado con éxito en REST API)
    print(f"Código de estado del servidor: {r.status_code}")
    
    if r.status_code == 201:
        print("\nRecurso creado con exito")
        print("Respuesta del servidor (id asignado por la API):")
        print(pd.DataFrame([r.json()]).T)
    else:
        print(f"El servidor rechazó la petición. Estado: {r.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error de red: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")