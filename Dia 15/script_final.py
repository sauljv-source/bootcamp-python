# Mini proyecto semana 3 Zenodo
# Script interactivo capaz de buscar, descargar, crear y postear, borrar, publicar y versionar.
# Es una unificacion de los scripts de esta semana en un menu interactivo
# Los scripts ndividuales esta reciclados y definidos como funciones
# Si los hubieramos definido asi los otros dias nos podriamos haber evitado estas definiciones repetitivas

import os
import requests
from dotenv import load_dotenv
import pandas as pd
import ast
import json

URL_DOWNLOAD = "https://sandbox.zenodo.org/api/records"
URL_DEPOSIT = "https://sandbox.zenodo.org/api/deposit/depositions"

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

def descargar_ficheros_filtrados(df_filtrado, query_busqueda, filtrado, valor_buscado):
    if 'files' not in df_filtrado.columns:
        print("La columna 'files' no existe en el DataFrame filtrado.")
        return None

    try:
        contador_descargas = 0
        nombre_carpeta_principal = f"resultados_zenodo_{query_busqueda}_{filtrado}_{valor_buscado}"
        os.makedirs(nombre_carpeta_principal, exist_ok=True)

        for idx, row in df_filtrado.iterrows():
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

            id_experimento = row.get('id', f"experimento_{idx}")
            valor_exp = row.get(filtrado)
            nombre_subcarpeta_exp = f"exp_{id_experimento}_{filtrado}_{valor_exp}"
            ruta_subcarpeta_exp = os.path.join(nombre_carpeta_principal, nombre_subcarpeta_exp)
            os.makedirs(ruta_subcarpeta_exp, exist_ok=True)

            for archivo in archivos_registro:
                if isinstance(archivo, dict):
                    url_self = archivo.get('links', {}).get('self')
                    if url_self:
                        contador_descargas += 1
                        nombre_original = archivo.get('key', f"fichero_{contador_descargas}.bin")
                        print(f"[{contador_descargas}] Descargando archivo: {nombre_original}")

                        ruta_guardado = os.path.join(ruta_subcarpeta_exp, nombre_original)
                        r_fichero = requests.get(url_self, headers=cabeceras_json, stream=True)

                        if r_fichero.status_code == 200:
                            with open(ruta_guardado, 'wb') as f_out:
                                for chunk in r_fichero.iter_content(chunk_size=8192):
                                    if chunk:
                                        f_out.write(chunk)
                        else:
                            print(f"Error {r_fichero.status_code} al descargar {nombre_original}.")

        print(f"\nProceso de descarga finalizado. Se guardaron {contador_descargas} ficheros.")
        return nombre_carpeta_principal

    except Exception as e:
        print(f"Error inesperado: {e}")
        return None


def buscar_y_filtrar_registros():
    query = input("\nIntroduce el término de búsqueda: ").strip()

    params = {
        "q": query,
        "type": "dataset",
        "size": 100,
        "page": 1
    }

    try:
        r = requests.get(URL_DOWNLOAD, headers=cabeceras_json, params=params)
        if r.status_code != 200:
            print(f"Error del servidor: {r.text}")
            return

        data = r.json()
        registros = data.get('hits', {}).get('hits', [])
        print(f"Se han encontrado {len(registros)} registros para '{query}'.")

        if not registros:
            return

        df_original = pd.json_normalize(registros)
        archivo_total = f"zenodo_{query}_todos_los_registros.csv"
        df_original.to_csv(archivo_total, index=False, encoding='utf-8')
        print(f"Archivo original guardado como: {archivo_total}")

        # Selección de columnas filtrables
        columnas_utiles = []
        for col in df_original.columns:
            muestra = df_original[col].dropna()
            if muestra.empty or isinstance(muestra.iloc[0], (list, dict)):
                continue
            if 1 < muestra.nunique() < 40 and muestra.astype(str).str.len().mean() < 40:
                columnas_utiles.append(col)

        print("\nColumnas útiles disponibles para filtrar:")
        for col in columnas_utiles:
            print(f" - {col} ({df_original[col].nunique()} valores únicos)")

        mapeo_columnas = {col.lower(): col for col in columnas_utiles}

        while True:
            filtrado = input("\n¿Por qué categoría quieres filtrar los datos?: ").strip().lower()
            if filtrado in mapeo_columnas:
                filtrado = mapeo_columnas[filtrado]
                break
            print(f"'{filtrado}' no es válido. Elige una de las columnas mostradas.")

        while True:
            valores_muestra = [
                item.item() if hasattr(item, 'item') else item 
                for item in df_original[filtrado].dropna().unique()[:5]
            ]
            print(f"(Ejemplos válidos en '{filtrado}': {valores_muestra})")

            if filtrado.startswith('stats.'):
                try:
                    min_input = input("Introduce el valor mínimo: ").strip()
                    max_input = input("Introduce el valor máximo: ").strip()
                    min_val = float(min_input) if min_input != "" else float('-inf')
                    max_val = float(max_input) if max_input != "" else float('inf')

                    if min_val > max_val:
                        print("[-] El valor mínimo no puede ser mayor que el máximo.")
                        continue

                    df_filtrado = df_original[(df_original[filtrado].astype(float) >= min_val) & (df_original[filtrado].astype(float) <= max_val)].copy()
                    valor_buscado = f"rango_{min_val}_a_{max_val}"
                except ValueError:
                    print("Introduce números válidos para el rango.")
                    continue
            else:
                valor_buscado = input(f"¿Qué valor buscas en '{filtrado}'?: ").strip()
                df_filtrado = df_original[df_original[filtrado].astype(str).str.lower() == valor_buscado.lower()].copy()

            if not df_filtrado.empty:
                print(f"Filtrado con éxito. Se encontraron {len(df_filtrado)} filas.")
                nombre_carpeta_principal = f"resultados_zenodo_{query}_{filtrado}_{valor_buscado}"

                opcion_descarga = input("¿Deseas descargar los ficheros de dichos experimentos? (si/no): ").strip().lower()
                if opcion_descarga in ["si", "sí"]:
                    descargar_ficheros_filtrados(df_filtrado, query, filtrado, valor_buscado)
                else:
                    os.makedirs(nombre_carpeta_principal, exist_ok=True)

                nombre_archivo_csv = f"zenodo_{query}_{filtrado}_{valor_buscado}.csv"
                ruta_csv_final = os.path.join(nombre_carpeta_principal, nombre_archivo_csv)
                df_filtrado.to_csv(ruta_csv_final, index=False, encoding='utf-8')
                print(f"Archivo CSV guardado en: {ruta_csv_final}")
                break
            else:
                print("No hay registros que cumplan con el filtro. Inténtalo de nuevo.")

    except requests.exceptions.RequestException as e:
        print(f"Error de red: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

def crear_y_publicar_nuevo_deposito():
    
    if not os.path.exists("metadata.json"):
        print("Error crítico, no se encuentra el archivo metadata.json' en el directorio.")
        return
    
    try:
        print("\nCreando nuevo borrador en Zenodo Sandbox")
        r = requests.post(URL_DEPOSIT, json={}, headers=cabeceras_json)
        
        if r.status_code != 201:
            print(f"Rechazado por el servidor: {r.text}")
            return

        data = r.json()
        deposito_id = data['id']
        bucket_url = data['links']['bucket']
        print(f"Borrador creado con ID: {deposito_id}")

        # Creación del archivo local de prueba
        archivo_local = "fichero_prueba.txt"
        with open(archivo_local, "wb") as f:
            f.write(b"Contenido de prueba para el Zenodo Sandbox.")

        # Subida del archivo al bucket
        url_subida = f"{bucket_url}/{archivo_local}"
        with open(archivo_local, "rb") as fp:
            r_file = requests.put(url_subida, data=fp, headers=cabeceras_archivo)

        if r_file.status_code not in [200, 201, 202]:
            print(f"Error al subir fichero: {r_file.text}")
            return
        print("Fichero subido correctamente al bucket.")

        # Carga de metadatos
        archivo_metadatos = "metadata.json"
        try:
            with open(archivo_metadatos, "r", encoding="utf-8") as fp:
                datos_metadatos = json.load(fp)
        except Exception as e:
            print(f"Error al leer el archivo de metadatos: {e}")
            return

        r_meta = requests.put(f"{URL_DEPOSIT}/{deposito_id}", headers=cabeceras_json, json=datos_metadatos)
        if r_meta.status_code != 200:
            print(f"Error al actualizar metadatos: {r_meta.text}")
            return
        print("Metadatos registrados correctamente.")

        # Publicación
        r_pub = requests.post(f"{URL_DEPOSIT}/{deposito_id}/actions/publish", headers=cabeceras_json)
        if r_pub.status_code == 202:
            print("Depósito publicado oficialmente en Zenodo Sandbox.")
            print(f"Enlace: {r_pub.json().get('links', {}).get('html', 'No disponible')}")
        else:
            print(f"Error al publicar: {r_pub.text}")
            
        if os.path.exists(archivo_local):
            os.remove(archivo_local)

    except Exception as e:
        print(f"Error inesperado: {e}")


def crear_nueva_version():
    deposito_id = input("\nIntroduce el ID del depósito publicado a versionar: ").strip()
    if not deposito_id:
        print("ID no válido.")
        return
    
    if not os.path.exists("metadata.json"):
        print("Error crítico: No se encuentra el archivo 'metadata.json' en el directorio.")
        return

    try:
        url_version = f"{URL_DEPOSIT}/{deposito_id}/actions/newversion"
        r = requests.post(url_version, headers=cabeceras_json)

        if r.status_code != 201:
            print(f"El servidor rechazó la solicitud de versionado: {r.text}")
            return

        print("Solicitud de nueva versión aceptada.")
        data = r.json()
        url_nuevo_borrador = data['links']['latest_draft']

        # Obtener detalles del nuevo borrador
        r_detalles = requests.get(url_nuevo_borrador, headers=cabeceras_json)
        nuevo_deposito_data = r_detalles.json()
        nuevo_id = nuevo_deposito_data['id']
        nuevo_bucket = nuevo_deposito_data['links']['bucket']

        print(f"Nuevo depósito borrador generado con ID: {nuevo_id}")

        # Eliminar ficheros heredados de la versión anterior
        url_archivos = f"{URL_DEPOSIT}/{nuevo_id}/files"
        r_files = requests.get(url_archivos, headers=cabeceras_json)
        
        if r_files.status_code == 200:
            archivos_heredados = r_files.json()
            for archivo_viejo in archivos_heredados:
                file_id = archivo_viejo['id']
                r_del = requests.delete(f"{URL_DEPOSIT}/{nuevo_id}/files/{file_id}", headers=cabeceras_json)
                if r_del.status_code == 204:
                    print(f"Archivo heredado ID {file_id} eliminado.")

        # Crear y subir el nuevo fichero
        nuevo_archivo = "fichero_nuevo.txt"
        with open(nuevo_archivo, "wb") as f:
            f.write(b"Contenido actualizado para la nueva version en Zenodo Sandbox.")

        url_subida = f"{nuevo_bucket}/{nuevo_archivo}"
        with open(nuevo_archivo, "rb") as fp:
            r_file = requests.put(url_subida, data=fp, headers=cabeceras_archivo)

        if r_file.status_code not in [200, 201, 202]:
            print(f"Error al subir el nuevo fichero: {r_file.text}")
            return
        print("Nuevo fichero subido al bucket correctamente.")
        
        # Carga y actualización de metadatos para la nueva versión
        archivo_metadatos = "metadata.json"
        try:
            with open(archivo_metadatos, "r", encoding="utf-8") as fp:
                datos_metadatos = json.load(fp)
        except Exception as e:
            print(f"Error al leer el archivo de metadatos: {e}")
            return

        r_meta = requests.put(f"{URL_DEPOSIT}/{nuevo_id}", headers=cabeceras_json, json=datos_metadatos)
        if r_meta.status_code != 200:
            print(f"Error al actualizar metadatos de la nueva versión: {r_meta.text}")
            return
        print("Metadatos de la nueva versión registrados correctamente.")

        # Publicar la nueva versión
        r_pub = requests.post(f"{URL_DEPOSIT}/{nuevo_id}/actions/publish", headers=cabeceras_json)
        if r_pub.status_code == 202:
            print("Nueva versión publicada oficialmente.")
            print(f"Enlace: {r_pub.json().get('links', {}).get('html', 'No disponible')}")
        else:
            print(f"Error al publicar la nueva versión: {r_pub.text}")
            
        if os.path.exists(nuevo_archivo):
            os.remove(nuevo_archivo)

    except Exception as e:
        print(f"Error inesperado: {e}")
        
def listar_depositos():
    try:
        print("\nListado de depósitos")
        params = {"page": 1, "size": 100}
        r = requests.get(URL_DEPOSIT, headers=cabeceras_json, params=params)
        
        if r.status_code != 200:
            print(f"Error al listar depósitos: {r.text}")
            return None

        depositos = r.json()
        if not depositos:
            print("No se encontraron depósitos asociados a esta cuenta.")
            return []

        for dep in depositos:
            dep_id = dep.get('id')
            estado = dep.get('state', 'unknown')
            submitted = dep.get('submitted', False)
            # Determinar visualmente si es borrador o publicado
            tipo_estado = "PUBLICADO" if submitted else f"BORRADOR ({estado})"
            
            # Obtener título (desde metadata o primer nivel)
            titulo = dep.get('title') or dep.get('metadata', {}).get('title', 'Sin título')
            print(f"ID: {dep_id} | Estado: {tipo_estado} | Título: {titulo}")
            
        return depositos

    except Exception as e:
        print(f"Error inesperado: {e}")
        return None


def borrar_borrador():
    try:
        # Mostramos primero la lista para facilitar la selección del ID
        depositos = listar_depositos()
        if not depositos:
            return

        dep_id = input("\nIntroduce el ID del borrador que deseas borrar: ").strip()
        if not dep_id:
            print("ID no válido.")
            return

        confirm = input(f"¿Seguro que quieres borrar permanentemente el borrador {dep_id}? (si/no): ").strip().lower()
        if confirm not in ["si", "sí"]:
            print("Operación de borrado cancelada.")
            return

        r = requests.delete(f"{URL_DEPOSIT}/{dep_id}", headers=cabeceras_json)
        if r.status_code == 204:
            print(f"Borrador {dep_id} eliminado correctamente.")
        else:
            print(f"Error al borrar el borrador {dep_id} (Código {r.status_code}): {r.text}")

    except Exception as e:
        print(f"Error inesperado: {e}")

def menu_principal():
    while True:
        print("\nMenu interactivo Zenodo Sandbox\n")
        print("1. Buscar, filtrar y descargar registros de Zenodo")
        print("2. Listar todos mis depósitos")
        print("3. Crear, subir fichero, metadatos y publicar nuevo depósito")
        print("4. Versionar depósito publicado (borrar heredados, subir nuevo y publicar)")
        print("5. Borrar un depósito en borrador")
        print("6. Salir")
        
        opcion = input("\nSelecciona una opción (1-6): ").strip()

        if opcion == "1":
            buscar_y_filtrar_registros()
        elif opcion == "2":
            listar_depositos()
        elif opcion == "3":
            crear_y_publicar_nuevo_deposito()
        elif opcion == "4":
            crear_nueva_version()
        elif opcion == "5":
            borrar_borrador()
        elif opcion == "6":
            break
        else:
            print("Opción no válida. Introduce un número del 1 al 6.")

if __name__ == "__main__":
    menu_principal()