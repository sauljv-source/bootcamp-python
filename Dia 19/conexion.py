# Mismo archivo que los demas dias pero hemos añadadido una configuración básica del logging para la conexión

import os
import time
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler("pipeline.log"), logging.StreamHandler()])

def conectar_con_reintentos(mongo_uri, max_intentos):
    espera = 1
    for intento in range(max_intentos):
        try:
            logging.info(f"Intentando conectar a MongoDB (intento {intento + 1}/{max_intentos})...")
            client = MongoClient(mongo_uri)
            client.admin.command('ping')
            logging.info("Conexion exitosa a MongoDB Atlas")
            return client
        except Exception as e:
            if intento == max_intentos - 1:
                logging.error("Se agotaron los intentos. la base de datos no esta disponible.")
                raise
            logging.warning(f"No se pudo conectar a MongoDB. reintentando en {espera} segundos... error: {str(e).lower()}")
            time.sleep(espera)
            espera *= 2

def obtener_coleccion(nombre_coleccion):
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")
    if not MONGO_URI:
        logging.error("La variable de entorno 'MONGO_URI' no esta configurada.")
        exit(1)
    client = conectar_con_reintentos(MONGO_URI, 5)
    return client, client["test_database"][nombre_coleccion]