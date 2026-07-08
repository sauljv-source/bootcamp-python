# Escritura de .csv

import csv

def solicitar_linea_csv(columnas):
    while True:
        cadena = input("Introduce nombre, edad y rol del nuevo usuario separado por comas: ")
        lista = list(cadena.split(","))
        
        if len(lista) != len(columnas):
            print(f"Se esperaban {len(columnas)} campos separados por comas. Intentelo de nuevo.\n")
            continue
            
        nombre = lista[0]
        edad_str = lista[1]
        rol = lista[2]
        
        if not nombre.replace(" ", "").isalpha() or not rol.replace(" ", "").isalpha():
            print("El nombre y el rol solo pueden contener letras. Intentelo de nuevo.\n")
            continue
            
        try:
            edad = int(edad_str)
            if edad <= 0:
                print("La edad debe ser un número positivo. Intentelo de nuevo.\n")
                continue
        except ValueError:
            print("La edad debe ser un número entero válido. Intentelo de nuevo.\n")
            continue 

        return {"nombre": nombre.title(), "edad": edad, "rol": rol.title()}


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
    nuevo_contenido_dic = solicitar_linea_csv(columnas)
    escritor.writerow(nuevo_contenido_dic)

print("Archivo creado y guardado con éxito.")