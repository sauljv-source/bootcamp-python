# Escritura de .json

import json

usuarios = {
    "Primer usuario": {"nombre": "Saul", "edad": 22, "rol": "Alumno de practicas"},
    "Segundo usuario": {"nombre": "Ana", "edad": 28, "rol": "Analista de datos"},
    "Tercer usuario": {"nombre": "Carlos", "edad": 35, "rol": "Desarrollador"}
}
    
with open("escritura_lectura.json", "w", encoding="utf-8") as archivo:
    json.dump(usuarios, archivo, indent=2)
    
print(json.dumps(usuarios, indent=2))

print("Archivo creado con exito.")