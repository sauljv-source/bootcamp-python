# script con una busqueda en zenodo + mongodb

import os
import requests
from dotenv import load_dotenv
from conexion import obtener_coleccion

URL = "https://sandbox.zenodo.org/api/records"

load_dotenv()
TOKEN = os.getenv("Token_Zenodo_Sandbox")
if not TOKEN:
    print("La variable de entorno 'TOKEN' no está configurada.")
    exit(1)

cabeceras_json = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

def ingesta_zenodo():
    query = input("\nIntroduce el término de búsqueda en Zenodo: ").strip()
    client, coleccion = obtener_coleccion(f"zenodo_registros_{query}")

    page = 1
    size = 100
    total_registros_procesados = 0
    insertados_totales = 0
    actualizados_totales = 0

    print(f"\nIniciando búsqueda y paginación en Zenodo para '{query}'")

    try:
        while True:
            params = {
                "q": query,
                "type": "dataset",
                "size": size,
                "page": page
            }

            r = requests.get(URL, headers=cabeceras_json, params=params)
            if r.status_code != 200:
                print(f"Error del servidor en la página {page}: {r.text}")
                break

            data = r.json()
            hits_container = data.get('hits', {})
            registros = hits_container.get('hits', [])
            total_en_servidor = hits_container.get('total', 0)

            if page == 1:
                print(f"Se han encontrado un total de {total_en_servidor} registros en el servidor de Zenodo.\n")

            if not registros:
                break

            print(f"Procesando página {page} ({len(registros)} registros)")

            insertados_lote = 0
            actualizados_lote = 0

            for registro in registros:
                reg_id = registro.get('id')# Aseguramos que cada registro tenga un identificador único para el filtro
                if not reg_id:
                    continue
                resultado = coleccion.update_one({"id": reg_id}, {"$set": registro}, upsert=True) # upsert, si el id ya existe, actualiza, si no, lo inserta como documento nuevo
                if resultado.upserted_id:
                    insertados_lote += 1
                elif resultado.modified_count > 0:
                    actualizados_lote += 1

            insertados_totales += insertados_lote
            actualizados_totales += actualizados_lote
            total_registros_procesados += len(registros)

            if total_registros_procesados >= total_en_servidor or len(registros) < size:
                break

            page += 1

        print(f"\nRegistros totales evaluados: {total_registros_procesados}")
        print(f"Documentos nuevos insertados: {insertados_totales}")
        print(f"Documentos existentes actualizados: {actualizados_totales}")
        print(f"Documentos existentes no actualizados: {total_registros_procesados - insertados_totales - actualizados_totales}\n")

    except requests.exceptions.RequestException as e:
        print(f"Error de red: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        try:
            client.close()
            print("Conexión a MongoDB cerrada.")
        except NameError:
            pass

def menu_principal():
    while True:
        opcion = input("¿Deseas realizar una búsqueda completa en Zenodo e ingestar los datos en MongoDB? (si/no): ").strip().lower()

        if opcion in ["si", "sí"]:
            ingesta_zenodo()
        elif opcion == "no":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Introduce 'si' o 'no'.")

if __name__ == "__main__":
    menu_principal()