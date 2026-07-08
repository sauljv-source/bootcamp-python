# Lectura de .csv

import csv

# Vamos a tratar de leer un archivo que no existe y evitar que se rompa el programa

try:
    with open("lectura_escritura.csv", "r", encoding="utf-8") as archivo_csv:
        contenido = csv.DictReader(archivo_csv)
    
        for i in contenido:
            print(i)

except FileNotFoundError:
    print("No se ha podido leer porque 'lectura_escritura.csv' no existe.")