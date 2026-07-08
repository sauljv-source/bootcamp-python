# Escritura de .csv

import csv

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
    nuevo_contenido_str = input("Introduce nombre, edad y rol del nuevo usuario separado por comas: ")
    nuevo_contenido_lst = list(nuevo_contenido_str.split(","))
    
    if len(nuevo_contenido_lst) == len(columnas):
        
        # Zip, crea parejas clave-valor, columnas-nuevo_contenido
        # Dict, te crea un diccionario con la lista que le has dado, lista de parez agrupados
        nuevo_contenido_dic = dict(zip(columnas, nuevo_contenido_lst))
        escritor.writerow(nuevo_contenido_dic)
    else:
        print(f"Error: Se esperaban {len(columnas)} datos y se recibieron {len(nuevo_contenido_lst)}.")

print("Archivo creado y guardado con éxito.")