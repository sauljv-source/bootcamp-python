# Consultas avanzadas de datos

import os
from dotenv import load_dotenv
from conexion import obtener_coleccion

def comprobar_texto(mensaje, error_mensaje):
    while True:
        entrada = input(mensaje).strip()
        texto_a_validar = entrada.replace(" ", "")     
        if texto_a_validar.isalpha() and entrada:
            return entrada
        print(error_mensaje)

def consultas_avanzadas():
    client, coleccion = obtener_coleccion()
    
    try:
        # $gt, mayor que
        # Esctrictamente mas de n asignaturas aprobadas n solo no vale), filtro_gt es un conjunto de diccionaarios, los alumnos
        while True:
            try:
                n = int(input("\nIntroduce la cota minima de asignaturas no contenida: ").strip())
                if 0 <= n < 40:
                    break
                else:
                    print("El valor tiene que estar entre 0 y 40.")
            except ValueError:
                print("El valor introducido tiene que ser numerico.")
        print(f"\n----- Estudiantes con más de {n} asignaturas aprobadas ($gt) -----")
        filtro_gt = {"asignaturas_aprobadas": {"$gt": n}}
        for est in coleccion.find(filtro_gt):
            # .get('nombre') en vez de ['nombre'] para que no se rompa el programa si no hay campo nombre definido en algun usuario
            print(f"- {est.get('nombre')}: {est.get('asignaturas_aprobadas')} asignaturas")
            
        # $eq, condicion de igualdad
        while True:
            try:
                age = int(input("\nIntroduce la edad del estudiante a buscar: ").strip())
                if 0 <= age:
                    break
                print("La edad no puede ser un numero negativo")
            except ValueError:
                print("La edad introducida tiene que ser un numero.")
        print(f"\n----- Estudiantes con {age} años ($eq) -----")
        filtro_eq = {"edad": {"$eq": age}}
        estudiantes = list(coleccion.find(filtro_eq))
        if estudiantes:
            for est in estudiantes:
                print(f"- {est.get('nombre')}: {est.get('edad')} años")
        else:
            print(f"No se encontró ningún estudiante con {age} años")

        # $in, dentro de una lista
        print("\n----- Estudiantes en Matemáticas o Física ($in) -----")
        # No incluimos ingenieria, esto se deberia hacer $regex ya que si contiene ingenieria nos devuelve ese resultado, $in no lo hace, y como todas las ingenierias son de algo, $in no encontraria ninguna y $regex si
        filtro_in = {"licenciatura": {"$in": ["Matemáticas", "Física"]}}
        for est in coleccion.find(filtro_in):
            print(f"- {est.get('nombre')} ({est.get('licenciatura')})")

        # $regex, busqueda por patrón / expresiones regulares
        # El flag "i" hace que no distinga entre mayúsculas y minúsculas (case-insensitive)
        while True:
            name = comprobar_texto("\nIntroduce nombre u apellido para filtar los estudiantes: ", "Todos los caracteres tienen que ser letras, no numeros. Intentalo de nuevo.")
            if len(name) >= 3:
                break
            print("El término de búsqueda debe tener al menos 3 caracteres.")
        print(f"\n----- Búsqueda con expresion regular ($regex): Nombres que contienen '{name}' -----")
        filtro_regex = {"nombre": {"$regex": name, "$options": "i"}}
        encontrados = False
        for est in coleccion.find(filtro_regex):
            print(f"- {est.get('nombre')}")
            encontrados = True
        if not encontrados:
            print(f"No se encontró ningún estudiante que coincida con '{name}'")

        # Con la proyección decidimos que campos queremos (1 para incluir, 0 para excluir) ya que MongoDB nos devuelve todos incluidos el id
        # No se puede mezclar 1 y 0 en la proyección, excepto para excluir el _id
        print("\n----- Proyección: Solo queremos el nombre y licenciatura (excluyendo el _id y los demas campos) de 5 alumnos ingresados al sistema -----")
        proyeccion = {"nombre": 1, "licenciatura": 1, "_id": 0}
        # Tomamos el conjunto completo (nuestra base de datos), proyeccion aplica el filtro de campos y .limit(5) nos reduce los resultados mostrados a solo 5 aunque haya mas
        for est in coleccion.find({}, proyeccion).limit(5):
            print(est)

        # Ordenar por nombre de forma ascendente (1, descendente seria -1) y limitar a los 3 primeros resultados
        print("\n----- Ordenado alfabéticamente (A-Z) y visualizacion del top 3 -----")
        # {"nombre": 1, "_id": 0} porque solo queremos mostrar el nombre, .sort(...) ordenar de forma ascendente los nombres
        resultados = coleccion.find({}, {"nombre": 1, "_id": 0}).sort("nombre", 1).limit(3)
        for est in resultados:
            print(f"- {est.get('nombre')}")

        # Sin índices, MongoDB tiene que leer todos los documentos de la colección, con un índice en el campo, la búsqueda es instantánea
        print("\n----- Creando índice en el campo 'nombre' -----")
        # El 1 indica índice ascendente. Esto solo se hace una vez (MongoDB ignora la petición si ya existe)
        nombre_indice = coleccion.create_index([("nombre", 1)])
        print(f"Índice creado exitosamente: {nombre_indice}")
        
        # Ver todos los índices activos en la colección
        print("\nÍndices actuales en la colección:")
        for index in coleccion.list_indexes():
            print(f"- {index['name']}: campos -> {index['key']}")

    except Exception as e:
        print(f"Error inesperado durante la ejercución: {e}")
    finally:
        client.close()
        print("\nConexión a MongoDB cerrada.")

if __name__ == "__main__":
    consultas_avanzadas()