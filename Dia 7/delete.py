# CRUD, delete

def delete(coleccion, name):
    print("\n----- ELIMINANDO DEL REGISTRO DE ESTUDIANTES -----")
    try:
        resultados = list(coleccion.find({"nombre": name.title()}))
        
        if not resultados:
            print("Estudiante no encontrado para eliminar.")
            return

        elif len(resultados) == 1:
            estudiante_elegido = resultados[0]
            resultado = coleccion.delete_one({"_id": estudiante_elegido["_id"]})
            if resultado.deleted_count > 0:
                print(f"Estudiante con id: {estudiante_elegido['_id']} eliminado con exito")
            else:
                print("No se elimino al usuario del registro.")
            return

        else:
            print(f"Se han encontrado {len(resultados)} estudiantes con el nombre '{name.title()}':")
            for indice, est in enumerate(resultados):
                id_limpio = str(est["_id"])
                print(f"[{indice + 1}] | licenciatura: {est['licenciatura']} | id: {id_limpio}")
            
        while True:
            eleccion = input("¿Deseas eliminar a todos los estudiantes o a uno en concreto? (todos/uno): ").lower().strip()
            if eleccion == "todos":
                resultado = coleccion.delete_many({"nombre": name.title()})
                if resultado.deleted_count > 0:
                    print(f"Se eliminaron {resultado.deleted_count} registros con exito.")
                else:
                    print("No se eliminaron registros.")
                break
                
            elif eleccion == "uno":
                while True:
                    try:
                        opcion = int(input("\nselecciona el indice del estudiante que deseas eliminar: "))
                        if 1 <= opcion <= len(resultados):
                            estudiante_elegido = resultados[opcion - 1]
                            resultado = coleccion.delete_one({"_id": estudiante_elegido["_id"]})
                            if resultado.deleted_count > 0:
                                print(f"Estudiante con id: {estudiante_elegido['_id']} eliminado con exito")
                            else:
                                print("No se elimino al usuario del registro.")
                            break
                        print(f"Por favor, introduce un numero entre 1 y {len(resultados)}.")
                    except ValueError:
                        print("Introduce un numero entero valido.")
                break
            else:
                print("respuesta no valida. intentalo de nuevo.")
                
    except Exception as e:
        print(f"Error de conexion: {str(e).lower()}")