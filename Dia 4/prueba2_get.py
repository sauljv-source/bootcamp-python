# Segunda prueba de acceso a una url publica con requests
# Leer multiples datos

import requests
import pandas as pd

url = 'https://jsonplaceholder.typicode.com/posts'

try:
    r = requests.get(url)
    
    # Comprobamos el código de estado (200 significa que todo va bien, 3xx,4xx,5xx son problemas)
    print(f"Código de estado: {r.status_code}")
    
    if r.status_code == 200:
        df = pd.DataFrame(r.json()) # r.json() ya es una lista
        # df.head() imprime los 5 primeros diccionarios de nuestra lista de diccionarios, 5 primeras filas
        print("Primeros cinco posts del contenido de la url introducida:")
        print(f"Formato tabla reducida:\n{df.head()}")
        print("Contenido de la url introducida:")
        print(f"Formato tabla:\n{df}")
        print(f"Total de registros recibidos: {len(df)}")
        print(f"Columnas detectadas: {list(df.columns)}")

    else:
        print(f"Error en el servidor: {r.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error de red o peticion HTTP: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")