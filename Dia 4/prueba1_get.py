# Primera prueba de acceso a una url publica con requests

import requests
import pandas as pd
import json

url = 'https://jsonplaceholder.typicode.com/posts/1'

try:
    r = requests.get(url)
    
    # Comprobamos el código de estado (200 significa que todo va bien, 3xx,4xx,5xx son problemas)
    print(f"Código de estado: {r.status_code}")
    
    if r.status_code == 200:
        df = pd.DataFrame([r.json()])
        print("Contenido de la url introducida:")
        print("(1) Formato filas:")
        for i in r.json():
            print(i,":", r.json()[i]) # Formato filas de cadenas
        print(f"(2) Formato tabla con pandas:\n{df.T}") # Formato tabla con pandas
        print(f"(3) Formato diccionario de phyton:\n{r.json()}") # Formato diccionario de phyton
        print(f"(4) Formato bonito de como se ve en la web con json:\n{json.dumps(r.json(), indent=2)}")
        
    else:
        print(f"Error en el servidor: {r.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error de red: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")