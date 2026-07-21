import pandas as pd
import requests
import os
from dotenv import load_dotenv
import ast

def descargar_ficheros_filtrados(df_filtrado, cabeceras, params, filtrado, valor_buscado):
    try:
        if 'files' in df_filtrado.columns:
            contador_descargas = 0
            
            # Creamos la carpeta filtrada que contendrá tanto el .csv como las subcarpetas para los archivos de los experimentos
            nombre_carpeta_principal = f"resultados_zenodo_{params['q']}_{filtrado}_{valor_buscado}"
            os.makedirs(nombre_carpeta_principal, exist_ok=True)
            
            for idx, row in df_filtrado.iterrows():
                try:
                    archivos_registro = row.get('files', None)
                    
                    if archivos_registro is None:
                        continue
                        
                    if hasattr(archivos_registro, "tolist"):
                        archivos_registro = archivos_registro.tolist()
                    elif isinstance(archivos_registro, str):
                        try:
                            archivos_registro = ast.literal_eval(archivos_registro)
                        except Exception:
                            continue
                    
                    if not isinstance(archivos_registro, list):
                        continue

                    # Identificador único para crear las subcarpetas de cada experimento dentro de la carpeta principal
                    id_experimento = row.get('id', f"experimento_{idx}")
                    valor_exp = row.get(f'{filtrado}')
                    nombre_subcarpeta_exp = f"exp_{id_experimento}_{filtrado}_{valor_exp}"
                    ruta_subcarpeta_exp = os.path.join(nombre_carpeta_principal, nombre_subcarpeta_exp)
                    os.makedirs(ruta_subcarpeta_exp, exist_ok=True)

                    for archivo in archivos_registro:
                        if isinstance(archivo, dict):
                            links_dict = archivo.get('links', {})
                            url_self = links_dict.get('self')
                            
                            if url_self:
                                contador_descargas += 1
                                
                                try:
                                    nombre_original = archivo.get('key')
                                    if not nombre_original:
                                        nombre_original = f"fichero_{contador_descargas}.bin"
                                        
                                    print(f"[{contador_descargas}] Descargando archivo: {nombre_original}")
                                    
                                    ruta_guardado = os.path.join(ruta_subcarpeta_exp, nombre_original)
                                    r_fichero = requests.get(url_self, headers=cabeceras, stream=True)
                                    
                                    if r_fichero.status_code == 200:
                                        with open(ruta_guardado, 'wb') as f_out:
                                            for chunk in r_fichero.iter_content(chunk_size=8192):
                                                if chunk:
                                                    f_out.write(chunk)
                                    else:
                                        print(f"Error {r_fichero.status_code} al intentar descargar.")
                                        
                                except Exception as e:
                                    print(f"Error: {e}")
                                    
                except Exception:
                    continue
                
            print(f"\nProceso de descarga finalizado. Se han guardado {contador_descargas} ficheros en subcarpetas.")
            return nombre_carpeta_principal
        else:
            print("La columna 'files' no existe en el DataFrame filtrado.")
            return None
            
    except Exception as e:
        print(f"Error crítico: {e}")
        return None

URL = 'https://sandbox.zenodo.org/api/records'

load_dotenv()
TOKEN = os.getenv("Token_Zenodo_Sandbox")
if not TOKEN:
    print("La variable de entorno 'TOKEN' no esta configurada.")
    exit(1)

cabeceras = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json; charset=utf-8'
}

# Buscamos en la web de Zenodo datasets relacionazos con el clima
params = {
    "q": "climate",
    "type": "dataset",
    "size": 100,
    "page": 1
}

try:
    r = requests.get(URL, headers=cabeceras, params=params)
    if r.status_code == 200:
        data = r.json()
        '''
        {
        "aggregations": { ... },
        "links": { ... },
        "hits": {
            "total": ...,
            "hits": [
            { "id": ... },
            { "id": ... }
            ]
        }
        }
        '''
        registros = data.get('hits', {}).get('hits', [])
        print(f"Se han encontrado {len(registros)} registros.")
    
        if not registros:
            print("No hay registros para procesar.")
            exit(1)

        df_original = pd.json_normalize(registros)

        archivo_total = f"zenodo_{params['q']}_todos_los_registros.csv"
        df_original.to_csv(archivo_total, index=False, encoding='utf-8')
        print(f"\nGuardado el archivo con todos los registros creado: {archivo_total}")
        
        # Columnas por las que filtrar, campos muy grandes o listas infiltrables las quitamos de las opciones
        columnas_utiles = []
        for i in df_original.columns:
            
            muestra = df_original[i].dropna()
            if muestra.empty or isinstance(muestra.iloc[0], (list, dict)):
                continue
                
            num_unicos = muestra.nunique()
            longitud_media = muestra.astype(str).str.len().mean()
            
            if 1 < num_unicos < 40 and longitud_media < 40:
                columnas_utiles.append(i)

        print("\nColumnas utiles disponibles para filtrar:")
        for i in columnas_utiles:
            print(f" - {i} ({df_original[i].nunique()} valores únicos)")
        mapeo_columnas = {col.lower(): col for col in columnas_utiles}
        
        while True:
            filtrado = input("\n¿Por que categoría quieres filtrar los datos?: ").strip().lower()
            
            if filtrado in mapeo_columnas:
                filtrado = mapeo_columnas[filtrado]
                break
            else:
                print(f"'{filtrado}' no existe en el registro. Introduce una columna válida.")
        
        while True:
            # Mostramos un par de ejemplos reales que existan en esa columna para guiar al usuario
            valores_muestra = [item.item() if hasattr(item, 'item') else item for item in df_original[filtrado].dropna().unique()[:5]]
            print(f"(Ejemplos válidos en esta columna: {list(valores_muestra)})")
            
            if filtrado.startswith('stats.'):
                print(f"\nLa columna '{filtrado}' es de tipo estadístico, filtraremos segun el rango elegido.")
                try:
                    min_input = input("Introduce el valor mínimo: ").strip()
                    max_input = input("Introduce el valor maximo: ").strip()
                    
                    min_val = float(min_input) if min_input != "" else float('-inf')
                    max_val = float(max_input) if max_input != "" else float('inf')
                    
                    if min_val > max_val:
                        print("El valor mínimo no puede ser mayor que el máximo. Inténtalo de nuevo.")
                        continue
                    
                    df_filtrado = df_original[
                        (df_original[filtrado].astype(float) >= min_val) & 
                        (df_original[filtrado].astype(float) <= max_val)
                    ].copy()
                    
                    valor_buscado = f"rango_{min_val}_a_{max_val}"
                except ValueError:
                    print("Por favor, introduce números válidos para el rango.")
                    continue
            else:
                valor_buscado = input(f"¿Que valor buscas para filtrar en la columna '{filtrado}'?: ").strip()  
                df_filtrado = df_original[df_original[filtrado].astype(str).str.lower() == valor_buscado.lower()].copy()
            
            if not df_filtrado.empty:
                print(f"Filtrado con éxito. Se encontraron {len(df_filtrado)} filas.")

                nombre_carpeta_principal = f"resultados_zenodo_{params['q']}_{filtrado}_{valor_buscado}"
        
                while True:
                    otro = input("¿Deseas descargar los ficheros de dichos experimentos? (si/no): ").strip().lower()
                    if otro in ["si", "sí"]:
                        descargar_ficheros_filtrados(df_filtrado, cabeceras, params, filtrado, valor_buscado)
                        break
                    elif otro == "no":
                        print("Se omite la descarga de los ficheros.")
                        os.makedirs(nombre_carpeta_principal, exist_ok=True)
                        break
                    else:
                        print("Respuesta no válida. Por favor, introduce únicamente 'si' o 'no'.")

                nombre_archivo_csv = f"zenodo_{params['q']}_{filtrado}_{valor_buscado}.csv"
                ruta_csv_final = os.path.join(nombre_carpeta_principal, nombre_archivo_csv)
        
                df_filtrado.to_csv(ruta_csv_final, index=False, encoding='utf-8')
                print(f"\nArchivo CSV '{nombre_archivo_csv}' creado y guardado con éxito dentro de '{nombre_carpeta_principal}/'.")
                break
            else:
                print(f"No hay ningún registro que cumpla con el filtro especificado. Inténtalo de nuevo.")
    else:
        print(f"Error del servidor. Código: {r.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error de red: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")