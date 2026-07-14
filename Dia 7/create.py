# CRUD, create

from validaciones import comprobar_texto

def create(coleccion, num):
    print("\n----- REGISTRANDO NUEVOS ESTUDIANTES -----")
    estudiantes_para_insertar = []
    
    texto_error = "Nombre no valido, evita introducir numeros o caracteres extraños. intentalo de nuevo."
    
    for i in range(num):
        print(f"Estudiante numero {i+1}")
        name = comprobar_texto("Introduce el nombre del estudiante: ", texto_error).title()
        degree = comprobar_texto("Introduce la licenciatura del estudiante: ", texto_error).title()
        
        estudiante_individual = {
            "nombre": name,
            "licenciatura": degree
        }
        estudiantes_para_insertar.append(estudiante_individual)
        
    try:
        if len(estudiantes_para_insertar) == 1:
            resultado = coleccion.insert_one(estudiantes_para_insertar[0])
            print(f"\nEstudiante unico insertado con id: {resultado.inserted_id}")
        else:
            resultado = coleccion.insert_many(estudiantes_para_insertar)
            ids_limpios = [str(id_mongo) for id_mongo in resultado.inserted_ids]
            print(f"\nSe insertaron {len(resultado.inserted_ids)} estudiantes de golpe con ids: {ids_limpios}")
    except Exception as e:
        print(f"Error de conexion: {str(e).lower()}")