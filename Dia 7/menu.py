# Menu para poder elegir que hacer sin estar ejecutando codigos cada vez

from conexion import obtener_coleccion
from validaciones import comprobar_texto, comprobar_entero_mayor_que_1
from create import create
from read import read
from update import update
from delete import delete

def mostrar_menu():
    client, coleccion = obtener_coleccion()
    try:
        while True:
            print("\n----- SISTEMA DE GESTIÓN DE ESTUDIANTES -----")
            print("[1] Registrar Estudiantes (Create)")
            print("[2] Buscar Estudiante (Read)")
            print("[3] Actualizar Licenciatura (Update)")
            print("[4] Eliminar Estudiante (Delete)")
            print("[5] Salir")
            
            opcion = comprobar_entero_mayor_que_1("Selecciona una opcion (1-5): ", "Opcion no valida.", "Introduce un numero entero.")
            
            if opcion == 1:
                num = comprobar_entero_mayor_que_1("¿Cuantos deseas registrar?: ", "Minimo 1.", "Numero no valido.")
                create(coleccion, num)
            elif opcion == 2:
                nombre = comprobar_texto("Nombre a buscar: ", "Texto no valido.")
                read(coleccion, nombre)
            elif opcion == 3:
                nombre = comprobar_texto("Nombre a actualizar: ", "Texto no valido.")
                update(coleccion, nombre)
            elif opcion == 4:
                nombre = comprobar_texto("Nombre a eliminar: ", "Texto no valido.")
                delete(coleccion, nombre)
            elif opcion == 5:
                print("Saliendo del sistema...")
                break
    finally:
        client.close()
        print("Conexion a mongodb cerrada de forma segura.")

if __name__ == "__main__":
    mostrar_menu()