# CRUD, update

from validaciones import comprobar_texto

def update(coleccion, name):
    print("\n----- ACTUALIZANDO REGISTRO DE ESTUDIANTES -----")
    try:
        resultados = list(coleccion.find({"nombre": name.title()}))
        
        if not resultados:
            print("Estudiante no encontrado para actualizar.")
            return

        elif len(resultados) == 1:
            estudiante_elegido = resultados[0]
        else:
            print(f"Se han encontrado {len(resultados)} estudiantes con el nombre '{name.title()}':")
            for indice, est in enumerate(resultados):
                id_limpio = str(est["_id"])
                print(f"[{indice + 1}] | licenciatura: {est['licenciatura']} | id: {id_limpio}")
            
            while True:
                try:
                    opcion = int(input("\nselecciona el indice del estudiante que deseas actualizar: "))
                    if 1 <= opcion <= len(resultados):
                        estudiante_elegido = resultados[opcion - 1]
                        break
                    print(f"Por favor, introduce un numero entre 1 y {len(resultados)}.")
                except ValueError:
                    print("Introduce un numero entero valido.")

        texto_error = "Entrada no valida, evita introducir numeros o caracteres extraños."
        nueva_licenciatura = comprobar_texto(f"Introduce la nueva licenciatura para {estudiante_elegido['nombre']} (actual: {estudiante_elegido['licenciatura']}): ", texto_error).title()
        
        resultado = coleccion.update_one({"_id": estudiante_elegido["_id"]}, {"$set": {"licenciatura": nueva_licenciatura}})
        
        if resultado.modified_count > 0:
            print(f"Registro actualizado con exito para el id: {estudiante_elegido['_id']}")
        else:
            print("No se realizaron cambios en el registro.")
            
    except Exception as e:
        print(f"Error de conexion: {str(e).lower()}")