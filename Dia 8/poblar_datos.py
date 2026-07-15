# Script de prueba para poblar nuestra base de datos sin tener que ir a mano uno a uno

from conexion import obtener_coleccion

def poblar_datos_prueba():
    client, coleccion = obtener_coleccion()
    
    try:
        # Limpieza para garantizar que no haya duplicaciones
        print("Limpiando todos los datos anteriores de la coleccion...")
        resultado_borrado = coleccion.delete_many({})
        print(f"Se han eliminado {resultado_borrado.deleted_count} estudiantes antiguos.")
        
        estudiantes_nuevos = [
            {"nombre": "Saul Jimenez", "licenciatura": "Fisica", "edad": 21, "asignaturas_aprobadas": 31},
            {"nombre": "Saul Gomez", "licenciatura": "Quimica", "edad": 18, "asignaturas_aprobadas": 6},
            {"nombre": "Carmen", "licenciatura": "Biologia", "edad": 19, "asignaturas_aprobadas": 14},
            {"nombre": "Saul", "licenciatura": "Ingenieria Industrial", "edad": 22, "asignaturas_aprobadas": 35},
            {"nombre": "Saul", "licenciatura": "Ingenieria de Software", "edad": 20, "asignaturas_aprobadas": 22},
            {"nombre": "Antonio", "licenciatura": "Historiador", "edad": 18, "asignaturas_aprobadas": 2},
            {"nombre": "Saul", "licenciatura": "Geologia", "edad": 20, "asignaturas_aprobadas": 18},
            {"nombre": "Ana Gomez", "licenciatura": "Ingenieria de Sistemas", "edad": 21, "asignaturas_aprobadas": 15},
            {"nombre": "Carlos Perez", "licenciatura": "Matematicas", "edad": 20, "asignaturas_aprobadas": 8},
            {"nombre": "Sofia Rodriguez", "licenciatura": "Fisica", "edad": 23, "asignaturas_aprobadas": 24},
            {"nombre": "Juan Gomez", "licenciatura": "Ingenieria Industrial", "edad": 19, "asignaturas_aprobadas": 3},
            {"nombre": "Maria Gomez", "licenciatura": "Derecho", "edad": 21, "asignaturas_aprobadas": 12},
            {"nombre": "Luis Hernandez", "licenciatura": "Ingenieria de Software", "edad": 25, "asignaturas_aprobadas": 32},
            {"nombre": "Laura Martinez", "licenciatura": "Matematicas", "edad": 18, "asignaturas_aprobadas": 5},
            {"nombre": "Pedro Ruiz", "licenciatura": "Fisica", "edad": 22, "asignaturas_aprobadas": 19},
            {"nombre": "Lucia Gomez", "licenciatura": "Administracion de Empresas", "edad": 20, "asignaturas_aprobadas": 9},
            {"nombre": "Diego Diaz", "licenciatura": "Ingenieria Civil", "edad": 21, "asignaturas_aprobadas": 11},
            {"nombre": "Elena Torres", "licenciatura": "Medicina", "edad": 26, "asignaturas_aprobadas": 38},
            {"nombre": "Javier Morales", "licenciatura": "Matematicas", "edad": 22, "asignaturas_aprobadas": 20},
            {"nombre": "Clara Sancho", "licenciatura": "Fisica", "edad": 19, "asignaturas_aprobadas": 7},
            {"nombre": "Marcos Gomez", "licenciatura": "Ingenieria Mecanica", "edad": 21, "asignaturas_aprobadas": 14},
            {"nombre": "Beatriz Ortiz", "licenciatura": "Quimica", "edad": 20, "asignaturas_aprobadas": 10},
            {"nombre": "Alejandro Flores", "licenciatura": "Historia", "edad": 19, "asignaturas_aprobadas": 4},
            {"nombre": "Patricia Castro", "licenciatura": "Psicologia", "edad": 22, "asignaturas_aprobadas": 18},
            {"nombre": "Roberto Vargas", "licenciatura": "Ingenieria Electronica", "edad": 23, "asignaturas_aprobadas": 22},
            {"nombre": "Irene Leon", "licenciatura": "Matematicas", "edad": 18, "asignaturas_aprobadas": 0},
            {"nombre": "Manuel Mendez", "licenciatura": "Fisica", "edad": 21, "asignaturas_aprobadas": 13},
            {"nombre": "Lucia Fernandez", "licenciatura": "Ingenieria Aeronautica", "edad": 24, "asignaturas_aprobadas": 27}
        ]
        
        print(f"\nInsertando {len(estudiantes_nuevos)} alumnos en la base de datos...")
        resultado_insercion = coleccion.insert_many(estudiantes_nuevos)
        print(f"Se han insertado {len(resultado_insercion.inserted_ids)} estudiantes nuevos.")
        
    except Exception as e:
        print(f"Error al poblar la base de datos: {e}")
    finally:
        client.close()
        print("Conexion a MongoDB cerrada.")

if __name__ == "__main__":
    poblar_datos_prueba()