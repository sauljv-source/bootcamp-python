# Archivo json

import json

datos = '{"nombre": "Juan", "edad": 30}'

data = json.loads(datos)

print(data["nombre"])

with open("lectura.json", "r", encoding="utf-8") as compra:
    ticket_compra = json.load(compra)
    
    print(json.dumps(ticket_compra, indent=4))
    
usuarios = {
    "Primer usuario": {"nombre": "Saul", "edad": 22, "rol": "Alumno de practicas"},
    "Segundo usuario": {"nombre": "Ana", "edad": 28, "rol": "Analista de datos"},
    "Tercer usuario": {"nombre": "Carlos", "edad": 35, "rol": "Desarrollador"}
}
    
with open("escritura.json", "w", encoding="utf-8") as archivo:
    json.dump(usuarios, archivo, indent=2)
    
print(json.dumps(usuarios, indent=2))