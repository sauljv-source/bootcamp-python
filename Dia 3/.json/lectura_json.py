# Lectura de .json

import json

try:
    with open("lectura_escritura.json", "r", encoding="utf-8") as compra:
        ticket_compra = json.load(compra)
    
    print(json.dumps(ticket_compra, indent=2))
except FileNotFoundError:
    print("El archivo lectura_escritura.json no existe.")
except Exception as e:
    print(f"Ha ocurrido un error al procesar el archivo: {e}")