# Lectura de .txt

try:
    with open("lectura_escritura.txt", "r", encoding="utf-8") as archivo_txt:
        contenido = archivo_txt.read()
    
        print(contenido)
        
# Exceptiom unifica todos los errores posibles, que no este el archivo, que este corrupto...        
except FileNotFoundError:
    print("El archivo lectura_escritura.txt no existe.")
except Exception as e:
    print(f"Ha ocurrido un error al procesar el archivo: {e}")