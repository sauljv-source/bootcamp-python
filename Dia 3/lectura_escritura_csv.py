# Archivo .csv

import csv

# Vamos a guardar los datos de los usuarios de nuestra base de datos

usuarios = [
    {"nombre": "Saul", "edad": 22, "rol": "Alumno de practicas"},
    {"nombre": "Ana", "edad": 28, "rol": "Analista de datos"},
    {"nombre": "Carlos", "edad": 35, "rol": "Desarrollador"}
]

columnas = ["nombre", "edad", "rol"]

with open("lectura_escritura.csv", "w", newline="", encoding="utf-8") as archivo_csv:
    escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
    escritor.writeheader()
    escritor.writerows(usuarios)

print("Archivo creado y guardado con éxito.")

with open("lectura_escritura.csv", "r", encoding="utf-8") as archivo_csv:
    contenido = csv.DictReader(archivo_csv)
    
    for i in contenido:
        print(i)