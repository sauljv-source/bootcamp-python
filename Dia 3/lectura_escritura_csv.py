# Archivo .csv

import csv

# Vamos a guardar los datos de los usuarios de nuestra base de datos

usuarios = [
    {"nombre": "Saúl", "edad": 22, "rol": "Alumno de prácticas"},
    {"nombre": "Ana", "edad": 28, "rol": "Analista de datos"},
    {"nombre": "Carlos", "edad": 35, "rol": "Desarrollador"}
]

columnas = ["nombre", "edad", "rol"]

with open("prueba.csv", "w", newline="", encoding="utf-8") as archivo_csv:
    escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
    escritor.writeheader()
    escritor.writerows(usuarios)

print("Archivo creado y guardado con éxito.")

with open("prueba.csv", "r", encoding="utf-8") as archivo_csv:
    contenido = csv.DictReader(archivo_csv)
    
    for i in contenido:
        print(i)