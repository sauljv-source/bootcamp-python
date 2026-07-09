# Ejercicios con lista que contiene diccionarios, bucles for y modificaciones dinamicas

tareas_proyecto = [
    {"id": 1, "descripción": "Configurar Git en el equipo", "encargado": "Saúl", "completada": True},
    {"id": 2, "descripción": "Resolver ejercicios esenciales phyton", "encargado": "Saúl", "completada": True},
    {"id": 3, "descripción": "Ficheros y JSON", "encargado": "Saúl", "completada": False},
    {"id": 4, "descripción": "Peticiones HTTP y APIs REST", "encargado": "Saúl", "completada": False},
    {"id": 5, "descripción": "Miniproyecto semana 1", "encargado": "Saúl", "completada": False},
    {"id": 6, "descripción": "Evaluación final", "encargado": "Suso", "completada": False}
]
print("-----REGISTRO DE TAREAS-----")
# Comprobamos si el encargado es "Saúl" y si la tarea no está completada, imprimir id y descripción si asi es
print("Estas son las tareas que Saúl no ha realizado todavia:")
for i in tareas_proyecto:
    if i["encargado"] == "Saúl" and i["completada"] == False:
        print(f"Id {i['id']} y descripción: {i['descripción']}.")

while True:
    eleccion = input("¿Quieres registrar alguna tarea completada recientemente?: ").strip().lower()
    if eleccion in ["sí", "si"]:
        # Procedemos a cambiar la tarea realizada ahora como completada
        id_a_cambiar = int(input("Introduce el id de la tarea completada: "))
        
        tarea_encontrada = False

        for i in tareas_proyecto:
            if i["id"] == id_a_cambiar:
                tarea_encontrada = True
                
                if i["completada"] == True:
                    print(f"La tarea con id {id_a_cambiar} ya está completada.")
                    tarea_encontrada = False
                    
                else:
                    i["completada"] = True
                    print("Resumen de la actualización en el sistema:")
                    for clave, valor in i.items():
                        print(f"{clave.capitalize()}: {valor}")
                    break

        # Por si se introduce un id que no este en nuestras tareas, para que no salga del bucle while
        if tarea_encontrada:
            break
            
    elif eleccion == "no":
        print("Registro perfectamente actualizado.")
        break
    else:
        print("Respuesta no valida. Escribe 'si' o 'no'.")