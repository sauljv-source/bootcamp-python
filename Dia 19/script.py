# Script de consultas sobre nuestros datos en MongoDB

import logging
from dotenv import load_dotenv
from conexion import obtener_coleccion

def ejecutar_consultas():
    query_busqueda = input("Introduce el nombre de la colección a consultar: ").strip()
    client, coleccion = obtener_coleccion(f"zenodo_registros_{query_busqueda}")

    try:
        total_docs = coleccion.count_documents({})
        logging.info(f"Total de documentos en la colección: {total_docs}")

        logging.info("Buscando un documento de ejemplo...")
        ejemplo = coleccion.find_one()
        if ejemplo:
            logging.info(f"ID del primer registro encontrado: {ejemplo.get('id')}")
            # Aquí puedes inspeccionar las claves principales del JSON de Zenodo
            logging.info(f"Claves principales del documento: {list(ejemplo.keys())}")

        filtro_ejemplo = input("\nIntroduce una palabra clave para buscar en los títulos o descripciones: ").strip()
        if filtro_ejemplo:
            query_filtro = {
                "$or": [
                    {"metadata.title": {"$regex": filtro_ejemplo, "$options": "i"}},
                    {"metadata.description": {"$regex": filtro_ejemplo, "$options": "i"}}
                ]
            }
            
            # Usamos proyección para traer solo el título y la fecha
            proyeccion = {"id": 1, "metadata.title": 1, "metadata.publication_date": 1, "_id": 0}
            
            resultados = list(coleccion.find(query_filtro, proyeccion).limit(5))
            logging.info(f"Se encontraron {len(resultados)} resultados de ejemplo para '{filtro_ejemplo}':")
            for res in resultados:
                meta = res.get('metadata', {})
                logging.info(f"Título: {meta.get('title')} (Fecha: {meta.get('publication_date')})")

    except Exception as e:
        logging.error(f"Error al ejecutar las consultas: {e}")
    finally:
        client.close()
        logging.info("Conexión a MongoDB cerrada.")

if __name__ == "__main__":
    ejecutar_consultas()