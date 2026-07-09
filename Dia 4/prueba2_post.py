# Primera prueba de escritura en una url publica con requests
import requests
import pandas as pd

def comprobar_texto(mensaje, error_mensaje, comas=False):
    while True:
        entrada = input(mensaje).strip()
        texto_a_validar = entrada.replace(" ", "")
        if comas:
            texto_a_validar = texto_a_validar.replace(",", "")
            
        if texto_a_validar.isalpha() and entrada:
            return entrada
        print(error_mensaje)

def comprobar_entero_positivo(mensaje, error_mensaje1, error_mensaje2):
    while True:
        try:
            entrada = int(input(mensaje).strip())
            if entrada >= 0:
                return entrada
            print(error_mensaje1)
        except ValueError:
            print(error_mensaje2)

url = 'https://jsonplaceholder.typicode.com/posts'

TOKEN = "token_secreto"

cabeceras = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json; charset=UTF-8'
}

nuevo_post = {
    'Nombre': comprobar_texto("Nombre: ", "El valor introducido no es un nombre válido.\nInténtalo de nuevo.").title(),
    'id': 101,
    'Edad': comprobar_entero_positivo("Edad: ", "El valor tiene que ser positivo", "El dato introducido no es un valor válido.\nInténtalo de nuevo."),
    'Titulo del post': input("Introduce el titulo de tu post: "),
    'Introducción': input("Introduce la introducción de tu post: "),
}

try:
    print("Enviando datos al servidor remoto")
    # Hacemos el POST pasando los datos (json) y las cabeceras de seguridad (headers)
    r = requests.post(url, json=nuevo_post, headers=cabeceras)
    
    # El código de estado 201 significa "Created" (Creado con éxito en REST API)
    print(f"Código de estado del servidor: {r.status_code}")
    
    if r.status_code == 201:
        print("\nRecurso creado con exito")
        print("Respuesta del servidor (ID asignado por la API):")
        print(pd.DataFrame([r.json()]).T)
    else:
        print(f"El servidor rechazó la petición. Estado: {r.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error de red: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")