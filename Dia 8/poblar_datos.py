# Script de prueba para poblar nuestra base de datos sin tener que ir a mano uno a uno

from conexion import obtener_coleccion
import random

def generar_alumno_aleatorio():
    nombres = ["Sofía", "Saul", "Alberto", "Iker", "Carmen", "Ana", "Lana", "Amelia", "Lucia", "Alejandro", "Mateo", "Valentina", "Lucas", "Lucía", "Santiago", "Daniela"]
    apellidos = ["García", "Rodríguez", "González", "Fernández", "López", "Martínez", "Sánchez", "Jimenez", "Hernandez", "Gutierrez", "Pardo", "San Segundo"]
    
    licenciatura = ["Matemáticas", "Física", "Química", "Ingenieria de Software", "Estadística", "Biologia", "Geologia", "Enologia", "Ingenieria Mecanica", "Magisterio", "Derecho", "Enfermeria", "Medicina", "Veterinaria"]
    
    nombre_completo = f"{random.choice(nombres)} {random.choice(apellidos)}"
    licenciatura_estudiada = random.choice(licenciatura)
    edad = random.randint(18, 26)
    cantidad_aprobadas = random.randint(0, 39)
    
    return {
        "nombre": nombre_completo,
        "licenciatura": licenciatura_estudiada,
        "edad": edad,
        "asignaturas_aprobadas": cantidad_aprobadas
    }

def poblar_datos_prueba():
    client, coleccion = obtener_coleccion()
    
    try:
        # Limpieza para garantizar que no haya duplicaciones
        print("Limpiando todos los datos anteriores de la coleccion...")
        resultado_borrado = coleccion.delete_many({})
        print(f"Se han eliminado {resultado_borrado.deleted_count} estudiantes antiguos.")
        
        estudiantes_nuevos = [generar_alumno_aleatorio() for i in range(30)]
        
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