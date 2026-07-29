# script con una busqueda en zenodo + mongodb + logging profesional

import os
import requests
import logging
from dotenv import load_dotenv
from conexion import obtener_coleccion

URL = "https://sandbox.zenodo.org/api/records"

load_dotenv()
TOKEN = os.getenv("Token_Zenodo_Sandbox")
if not TOKEN:
    logging.error("La variable de entorno 'TOKEN' no está configurada.")
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

    logging.info(f"Iniciando búsqueda y paginación en Zenodo para '{query}'")

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
                logging.error(f"Error del servidor en la página {page}: {r.text}")
                break

            data = r.json()
            hits_container = data.get('hits', {})
            registros = hits_container.get('hits', [])
            total_en_servidor = hits_container.get('total', 0)

            if page == 1:
                logging.info(f"Se han encontrado un total de {total_en_servidor} registros en el servidor de Zenodo.\n")

            if not registros:
                break

            logging.info(f"Procesando página {page} ({len(registros)} registros)")

            insertados_lote = 0
            actualizados_lote = 0

            for registro in registros:
                reg_id = registro.get('id')# Aseguramos que cada registro tenga un identificador único para el filtro
                if not reg_id:
                    logging.warning("Registro omitido por falta de identificador único ('id').")
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

        logging.info(f"Registros totales evaluados: {total_registros_procesados}")
        logging.info(f"Documentos nuevos insertados: {insertados_totales}")
        logging.info(f"Documentos existentes actualizados: {actualizados_totales}")
        logging.info(f"Documentos existentes no actualizados: {total_registros_procesados - insertados_totales - actualizados_totales}\n")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error de red durante la petición a Zenodo: {e}")
    except Exception as e:
        logging.error(f"Error inesperado en el pipeline: {e}")
    finally:
        try:
            client.close()
            logging.info("Conexión a MongoDB cerrada.")
        except NameError:
            pass

def menu_principal():
    while True:
        opcion = input("¿Deseas realizar una búsqueda completa en Zenodo e ingestar los datos en MongoDB? (si/no): ").strip().lower()

        if opcion in ["si", "sí"]:
            ingesta_zenodo()
        elif opcion == "no":
            logging.info("Saliendo del programa.")
            break
        else:
            logging.warning("Opción no válida. Introduce 'si' o 'no'.")

if __name__ == "__main__":
    menu_principal()