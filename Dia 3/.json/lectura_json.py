# Lectura de .json

import json

try:
    with open("escritura_lectura.json", "r", encoding="utf-8") as compra:
        ticket_compra = json.load(compra)
    
    print(json.dumps(ticket_compra, indent=2))
except FileNotFoundError:
    print("No se ha podido leer porque 'escritura_lectura.json' no existe.")