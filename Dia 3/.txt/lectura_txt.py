# Lectura de .txt

try:
    with open("lectura_escritura.txt", "r", encoding="utf-8") as archivo_txt:
        contenido = archivo_txt.read()
    
        print(contenido)
except FileNotFoundError:
    print("No se ha podido leer porque 'lectura_escritura.txt' no existe.")