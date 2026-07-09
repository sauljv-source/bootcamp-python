# Primera prueba de acceso a una url publica con requests

import requests
import pandas as pd

url = 'https://jsonplaceholder.typicode.com/posts/1'

try:
    r = requests.get(url)
    
    # Comprobamos el código de estado (200 significa que todo va bien, 3xx,4xx,5xx son problemas)
    print(f"Código de estado: {r.status_code}")
    
    if r.status_code == 200:
        df = pd.DataFrame([r.json()])
        print("Contenido de la url introducida:")
        print(f"Formato tabla:\n{df.T}") # Formato tabla
        print(f"Formato diccionario de phyton:\n{r.json()}") # Formato diccionario de phyton

    else:
        print(f"Error en el servidor: {r.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error de red o peticion HTTP: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")