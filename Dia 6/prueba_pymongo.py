#Comprobacion de que este bien instalado y la versión sea la adecuada

import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargamos las variables ocultas del archivo .env para evitar compartir nuestro ususario y contraseña
load_dotenv()

print("Instalación realizada correctamente")
print(f"Versión actual: {pymongo.__version__}")

# Creamos nuestro primer cluster en MongoDB Atlas y accedemos a el desde phyton
# Python lee la URL en memoria sin que nadie pueda ver la contraseña en el código
MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')
    print("Conexión exitosa a MongoDB Atlas")
except Exception as e:
    print(f"Error de conexión: {e}")