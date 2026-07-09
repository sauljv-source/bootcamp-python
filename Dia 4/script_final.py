# Buscamos en la web nuestro usuario para modificar un dato erroneo y lo imprimimos por pantalla para comprobar que todo funciona correctamente

import requests
import pandas as pd

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


while True:
    id_usuario = comprobar_entero_entre_1_y_10("Introduce el id del usuario de la pagina web que quieres modificar (del 1 al 10): ", "El valor tiene que estar entre 1 y 10", "El dato introducido no es un valor válido.\nInténtalo de nuevo.")

    try:
        r = requests.get(f'{url}/{id_usuario}')
        print(f"Código de estado: {r.status_code}")
    
        if r.status_code == 200:
            print("Contenido de la id introducida:")
            df = pd.json_normalize(r.json())
            print(df.T)
            comprobacion = true_false("¿Es esta la id que quieres modificar? (si o no): ", "Respuesta no válida. Escribe 'sí' o 'no'.")
            if comprobacion:
                break
            else:
                print("De acuerdo, busquemos otro id.\n")
            
        else:
            print(f"Error en el servidor: {r.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error de red: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

entradas = [ 
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
]

while True:
    cambio = input("¿Que entrada quieres modificar?: ").strip()
    if cambio in entradas:
        break
    elif cambio == 'id':
        print("No es posible cambiar el id.\nIntroduce otra entrada.")
    else:
        print("La entrada escrita no existe en el registro de datos.\nIntroduce una entrada que si exista para modificarla.")
        
      
modificacion = input("Introduce el nuevo texto que quieras guardar: ")

# Vamos a la posicion exacta de la tabla que hay que cambiar
df.at[0, cambio] = modificacion

# Pasamos los datos de la fila 0 a formato diccionario
datos_planos = df.iloc[0].to_dict()

nuevo_post = {
    "id": datos_planos["id"],
    "name": datos_planos["name"],
    "username": datos_planos["username"],
    "email": datos_planos["email"],
    "phone": datos_planos["phone"],
    "website": datos_planos["website"],
    "address": {
        "street": datos_planos["address.street"],
        "suite": datos_planos["address.suite"],
        "city": datos_planos["address.city"],
        "zipcode": datos_planos["address.zipcode"],
        "geo": {
            "lat": datos_planos["address.geo.lat"],
            "lng": datos_planos["address.geo.lng"]
        }
    },
    "company": {
        "name": datos_planos["company.name"],
        "catchPhrase": datos_planos["company.catchPhrase"],
        "bs": datos_planos["company.bs"]
    }
}

try:
    print("Enviando nuevos datos al servidor remoto")
    r = requests.post(url, json=nuevo_post, headers=cabeceras)
    print(f"Código de estado del servidor: {r.status_code}")
    if r.status_code == 201:
        print("\nDatos actualizados con exito")
        respuesta_servidor = r.json()
        respuesta_servidor['id'] = id_usuario
        print(pd.json_normalize(respuesta_servidor).T)
    else:
        print(f"El servidor rechazó la petición. Estado: {r.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error de red: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
    
# Los datos no se van a quedar guardados en la web
# Si volvemos a pedirlos van a ser los datos originales
# Es una web publica para practicar que no permite postear cosas nuevas
# Lo que hemos hecho es hacer un nuevo post modificando el id para que parezca una actualizacion de datos ya escritos