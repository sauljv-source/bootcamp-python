import os
import time
from pymongo import MongoClient
from dotenv import load_dotenv

def conectar_con_reintentos(mongo_uri, max_intentos):
    espera = 1
    for intento in range(max_intentos):
        try:
            print(f"Intentando conectar a MongoDB (intento {intento + 1}/{max_intentos})...")
            client = MongoClient(mongo_uri)
            client.admin.command('ping')
            print("Conexion exitosa a MongoDB Atlas")
            return client
        except Exception as e:
            if intento == max_intentos - 1:
                print("Se agotaron los intentos. la base de datos no esta disponible.")
                raise
            print(f"No se pudo conectar a MongoDB. reintentando en {espera} segundos... error: {str(e).lower()}")
            time.sleep(espera)
            espera *= 2

def obtener_coleccion():
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")
    if not MONGO_URI:
        print("La variable de entorno 'MONGO_URI' no esta configurada.")
        exit(1)
    client = conectar_con_reintentos(MONGO_URI, 5)
    return client, client["test_database"]["estudiantes"]