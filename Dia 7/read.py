# CRUD, read

def read(coleccion, name):
    print(f"\n----- BUSCANDO ESTUDIANTES LLAMADOS '{name.title()}' -----")
    try:
        cursor_resultados = coleccion.find({"nombre": name.title()})
        resultados = list(cursor_resultados)
        
        if resultados:
            print(f"Se han encontrado {len(resultados)} estudiante(s):")
            for estudiante in resultados:
                id_limpio = str(estudiante["_id"])
                print(f"Nombre: {estudiante['nombre']} | Licenciatura: {estudiante['licenciatura']} | ID: {id_limpio}")
        else:
            print(f"No se encontro ningun estudiante con el nombre '{name.title()}'.")
    except Exception as e:
        print(f"Error de conexion: {str(e).lower()}")