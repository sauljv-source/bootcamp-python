# Buscamos en la web nuestro usuario para modificar un dato erroneo y lo imprimimos por pantalla para comprobar que todo funciona correctamente

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

def comprobar_entero_entre_1_y_10(mensaje, error_mensaje1, error_mensaje2):
    while True:
        try:
            entrada = int(input(mensaje).strip())
            if 1 <= entrada <= 10:
                return entrada
            print(error_mensaje1)
        except ValueError:
            print(error_mensaje2)
            
def true_false(mensaje, error_mensaje):
    while True:
        entrada1 = input(mensaje).strip().lower()
        if entrada1 in ["sí", "si"]:
            return True
        elif entrada1 == "no":
            return False
        else:
            print(error_mensaje)

url = 'https://jsonplaceholder.typicode.com/users'

TOKEN = 'token_secreta'

cabeceras = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json; charset=utf-8'
}

busqueda_usuario = True
while busqueda_usuario:
    id = comprobar_entero_entre_1_y_10("Introduce el id del usuario de la pagina web que quieres modificar (del 1 al 10): ", "El valor tiene que estar entre 1 y 10", "El dato introducido no es un valor válido.\nInténtalo de nuevo.")

    try:
        r = requests.get(f'{url}/{id}')
        print(f"Código de estado: {r.status_code}")
    
        if r.status_code == 200:
            print("Contenido de la id introducida:")
            print(pd.json_normalize(r.json()).T)
            comprobacion = true_false("¿Es esta la id que quieres modificar? (si o no): ", "Respuesta no válida. Escribe 'sí' o 'no'.")
            if comprobacion:
                busqueda_usuario = False
            else:
                print("De acuerdo, busquemos otro id.\n")
            
        else:
            print(f"Error en el servidor: {r.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error de red: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

entradas = {'id', 
    'name', 
    'username', 
    'email', 
    'phone', 
    'website', 
    'address.street', 
    'address.suite', 
    'address.city', 
    'address.zipcode', 
    'address.geo.lat', 
    'address.geo.lng', 
    'company.name', 
    'company.catchPhrase', 
    'company.bs'
}

while True:
    cambio = input("¿Que quieres modificar?: ")
    if cambio.issubset(entradas):
        
        


nuevo_post = {
    'id': 'df.loc[0, "id"]',
    'name': 'df.loc[0, "name"]',
    'username': 'df.loc[0, "username"]',
    'email': 'df.loc[0, "email"]',
    'phone': 'df.loc[0, "phone"]',
    'website': 'df.loc[0, "website"]',
    'address.street': 'df.loc[0, "address.street"]',
    'address.suite': 'df.loc[0, "address.suite"]',
    'address.city': 'df.loc[0, "address.city"]',
    'address.zipcode': 'df.loc[0, "address.zipcode"]',
    'address.geo.lat': 'df.loc[0, "address.geo.lat"]',
    'address.geo.lng': 'df.loc[0, "address.geo.lng"]',
    'company.name': 'df.loc[0, "company.name"]',
    'company.catchPhrase': 'df.loc[0, "company.catchPhrase"]',
    'company.bs': 'df.loc[0, "company.bs"]'
}

try:
    print("Enviando nuevos datos al servidor remoto")
    r = requests.post(url, json=nuevo_post, headers=cabeceras)
    print(f"Código de estado del servidor: {r.status_code}")
    if r.status_code == 201:
        print("\nDatos actualizados con exito")
        print(pd.DataFrame([r.json()]).T)
    else:
        print(f"El servidor rechazó la petición. Estado: {r.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error de red: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")