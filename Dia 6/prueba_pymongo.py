#Comprobacion de que este bien instalado y la versión sea la adecuada

import pymongo
from pymongo import MongoClient

print("Instalación realizada correctamente")
print(f"Versión actual: {pymongo.__version__}")

# Creamos nuestro orimer cluster en MongoDB Atlas y accedemos a el desde phyton
MONGO_URI = "mongodb+srv://sauljv04:Bilbao35avila@cluster0.fduhqvc.mongodb.net/?appName=Cluster0"

try:
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')
    print("Conexión exitosa a MongoDB Atlas")
except Exception as e:
    print(f"Error de conexión: {e}")