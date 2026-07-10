# Miniproyecto final semana 1
# Extracción masiva de datos, filtracion de dichos datos y los pasa a un csv

import pandas as pd
import requests

# URL de ejemplo, deberia funcionar con cualquiera
URL = 'https://dummyjson.com/users'

'''
Url para probar:
https://dummyjson.com/users (Diccionario) (la mejor para filtrar datos)
https://dummyjson.com/posts (Diccionario)
https://jsonplaceholder.typicode.com/users (Lista)
https://jsonplaceholder.typicode.com/posts (Lista)
https://rickandmortyapi.com/api/character (Diccionario)
https://pokeapi.co/api/v2/pokemon (Diccionario)
'''

TOKEN = 'token_secreta'

cabeceras = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json; charset=utf-8'
}

try:
    r = requests.get(URL, headers=cabeceras)
    if r.status_code == 200:
        json_puro = r.json()
        lista_datos_cruda = None
        
        # Caso 1: Json es una lista
        if isinstance(json_puro, list):
            lista_datos_cruda = json_puro
    
        # Caso 2: El Json es un diccionario
        elif isinstance(json_puro, dict):
            for clave, valor in json_puro.items():
                # Buscamos una clave con un valor que sea una lista y que su longitud sea mayor que cero, que no este vacia, los datos que nos interesan, users en este caso
                if isinstance(valor, list) and len(valor) > 0:
                    print(f"Datos anidados detectados. Extrayendo desde la clave: '{clave}'")
                    lista_datos_cruda = valor
                    break 
    
        df_original = pd.json_normalize(lista_datos_cruda)
        
        print("\nColumnas disponibles para filtrar:")
        print(list(df_original.columns))
        # Todas las entradas, dinamicamente, y para que no exista sensitividad ante mayusculas
        # Diccionario que relaciona la entrada en minuscula con la entrada original de la web
        mapeo_columnas = {col.lower(): col for col in df_original.columns}
        
        while True:
            filtrado = input("\n¿Por que categoría quieres filtrar los datos?: ").strip().lower()
            
            if filtrado in mapeo_columnas:
                # Recuperamos el nombre real exacto que necesita Pandas
                filtrado = mapeo_columnas[filtrado]
                break
            else:
                print(f"'{filtrado}' no existe en el registro. Introduce una columna válida.")
        
        while True:
            # Mirar documentacion especifica de cada url para saber que datos son utiles tras filtrarlos
            valor_buscado = input(f"¿Que valor buscas para filtrar en la columna '{filtrado}'?: ").strip()
            # Convertimos a string temporalmente para evitar fallos si meten números por teclado ya que input() nos va a dar un string siempre
            # .astype(str) para transformar el dato de la url en texto, string
            # .str es por necesidad de pandas, si no lo pones da error las funciones .lower() o del estilo
            df_filtrado = df_original[df_original[filtrado].astype(str).str.lower() == valor_buscado.lower()].copy()
            
            if not df_filtrado.empty:
                print(f"Filtrado con éxito. Se encontraron {len(df_filtrado)} filas.")
                break
            else:
                print(f"No hay ningún registro donde '{filtrado}' sea igual a '{valor_buscado}'. Inténtalo de nuevo.")

        nombre_archivo = f"usuarios_filtrados_{filtrado}_{valor_buscado}.csv"
        df_filtrado.to_csv(nombre_archivo, index=False, encoding='utf-8')
        print(f"\nArchivo '{nombre_archivo}' creado y guardado con éxito.")

    else:
        print(f"Error del servidor. Código: {r.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error de red: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")