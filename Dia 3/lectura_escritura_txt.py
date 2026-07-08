# Archivo .txt

# 'w' viene de write/escribir. Si el archivo no existe, Python lo crea

with open("lectura_escritura.txt", "w", encoding="utf-8") as archivo_txt:
    archivo_txt.write("Dia 3\nPrimera prueba para crear archivos desde phyton.\n")
    archivo_txt.write("Tambien de escritura de datos\n")
    nuevo_contenido = input("Escribe algo nuevo para incluirlo en el archivo: ")
    archivo_txt.write(nuevo_contenido)

print("Archivo creado y guardado con éxito.")

# Ahora vamos a leer el archivo

with open("lectura_escritura.txt", "r", encoding="utf-8") as archivo_txt:
    contenido = archivo_txt.read()
    
print(contenido)