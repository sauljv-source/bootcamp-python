# Escritura de .json

import json

usuarios = [
     {"nombre": "Saul", "edad": 22, "rol": "Alumno de practicas"},
     {"nombre": "Ana", "edad": 28, "rol": "Analista de datos"},
     {"nombre": "Carlos", "edad": 35, "rol": "Desarrollador"}
]
    
with open("lectura_escritura.json", "w", encoding="utf-8") as archivo:
    json.dump(usuarios, archivo, indent=2)
    
print(json.dumps(usuarios, indent=2))

print("Archivo creado con exito.")