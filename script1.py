# Programa para buscar tu clasificación laboraral como X profesión (trabajamos con los tipos de datos, diccionarios, funciones y f-strings)
    
# Definimos funciones para no repetir procesos iguales en el codigo
def comprobar_texto(mensaje, error_mensaje, comas=False):
    while True:
        entrada = input(mensaje).strip()
        texto_a_validar = entrada.replace(" ", "")
        if comas:
            texto_a_validar = texto_a_validar.replace(",", "")
            
        if texto_a_validar.isalpha() and entrada:
            return entrada
        print(error_mensaje)

def comprobar_entero_positivo(mensaje, error_mensaje1, error_mensaje2):
    while True:
        try:
            entrada = int(input(mensaje).strip())
            if entrada >= 0:
                return entrada
            print(error_mensaje1)
        except ValueError:
            print(error_mensaje2)

def comprobar_float_rango(mensaje, error_mensaje1, error_mensaje2):
    while True:
        try:
            valor = float(input(mensaje).strip())
            if 5.0 <= valor <= 10.0:
                return valor
            print(error_mensaje1)
        except ValueError:
            print(error_mensaje2)
            
def master(mensaje1, mensaje2, error_mensaje1, error_mensaje2):
    while True:
        entrada1 = input(mensaje1).strip().lower()
        if entrada1 in ["sí", "si"]:
            entrada2 = comprobar_texto(mensaje2, error_mensaje1)
            return True, entrada2
        elif entrada1 == "no":
            entrada2 = "Ninguno"
            return False, entrada2
        else:
            print(error_mensaje2)


# Creamos un diccionario para agrupar los tipos de datos
print("\n----- REGISTRO DE DATOS -----")
estudiante = {
    "nombre": comprobar_texto("Nombre: ", "El valor introducido no es un nombre válido.\nInténtalo de nuevo.").title(),
    "profesion": comprobar_texto("¿Cuál es su trabajo?: ", "No es una profesión válida.\nInténtalo de nuevo.").lower(),
    "años_de_experiencia": comprobar_entero_positivo("Años de experiencia: ", "El valor tiene que ser positivo", "El dato introducido no es un valor válido.\nInténtalo de nuevo."),
    "nota_media_licenciatura": comprobar_float_rango("Nota media de su licenciatura: ", "El número debe estar entre 5.0 y 10.0.", "El dato introducido no es un número válido.\nInténtalo de nuevo.")
}

tiene_master, nombre_del_master = master("¿Has cursado un máster? (sí/no): ", "¿Cuál?: ", "El valor introducido no es un nombre válido.\nInténtalo de nuevo.", "Respuesta no válida. Escribe 'sí' o 'no'.")

# Añadimos la tupla master como datos por separados al diccionario
estudiante["estudio_master"] = tiene_master
estudiante["nombre_master"] = nombre_del_master

# Lista de idiomas
idiomas = comprobar_texto("Introduce todos los idiomas que sabe hablar fluidamente separados por comas: ", "El valor introducido no es un nombre válido.\nInténtalo de nuevo.", True)
estudiante["idiomas"] = [h.strip().title() for h in idiomas.split(",")]

idiomas_puesto = {"Español", "Ingles", "Portugues", "Frances", "Aleman"}
idiomas_set = set(estudiante["idiomas"])

idiomas_en_comun = idiomas_set.intersection(idiomas_puesto)
idiomas_faltantes = idiomas_puesto.difference(idiomas_set)

#Tupla de requisitos minimos
requisitos_junior = (0, 5.0)
requisitos_semi_senior = (2, 5.0)
requisitos_senior = (6, 5.0)

print("\n----- PROCESADO DE DATOS Y VEREDICTO FINAL -----")

print(f"Hola {estudiante['nombre']},\ncomprobemos tu clasificación laboral como {estudiante['profesion']}.")

if requisitos_junior[0] <= estudiante["años_de_experiencia"] < requisitos_semi_senior[0]:
    print(f"Tienes los años de experiencia suficientes como para ser {estudiante['profesion']} junior.")
elif requisitos_semi_senior[0] <= estudiante["años_de_experiencia"] < requisitos_senior[0]:
    print(f"Tienes los años de experiencia suficientes como para ser {estudiante['profesion']} semi senior.")
else:
    print(f"Tienes los años de experiencia suficientes como para ser {estudiante['profesion']} senior.") 

    
if len(idiomas_en_comun) >= 3 or estudiante["nota_media_licenciatura"] - requisitos_junior[1] >= 2 or estudiante["estudio_master"]:
    print("Tambien sobresales por encima de la media ya sea por los idiomas, el haber cursado un master o tu nota media durante la licenciatura.\nTu perfil estará bien valorado.")

# Listas y comprensiones de listas