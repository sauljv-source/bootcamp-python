#Lista que contiene diccionarios

tareas_proyecto = [
    {"id": 1, "descripción": "Configurar Git en el equipo", "encargado": "Saúl", "completada": True},
    {"id": 2, "descripción": "Resolver ejercicios esenciales phyton", "encargado": "Saúl", "completada": True},
    {"id": 3, "descripción": "Ficheros y JSON", "encargado": "Saúl", "completada": False},
    {"id": 4, "descripción": "Peticiones HTTP y APIs REST", "encargado": "Saúl", "completada": False},
    {"id": 5, "descripción": "Miniproyecto semana 1", "encargado": "Saúl", "completada": False},
    {"id": 6, "descripción": "Evaluación final", "encargado": "Suso", "completada": False}
]

# Comprobamos si el encargado es "Saúl" y si la tarea no está completada, imprimir id y descripción si asi es

print("Estas son las tareas que Saúl no ha realizado todavia:")
for i in tareas_proyecto:
    if i["encargado"] == "Saúl" and i["completada"] == False:
        print(f"Id {i['id']} y descripción: {i['descripción']}.")

id_a_cambiar = int(input("Introduce el ID de la tarea que has completado (ej: 2): "))

# RE RETO 2: Recorre la lista de tareas. Busca el diccionario que tenga ese "id".
# Cuando lo encuentres, cambia su valor de "completada" a True.

# Tu código aquí...


# RE RETO 3: Usa un bucle 'for' con el método '.items()' para mostrar los 
# datos de la tarea modificada línea por línea con el formato "Clave -> Valor".
# Pista del formato:
# for clave, valor in diccionario_modificado.items():
#     print(f"{clave} -> {valor}")

# Tu código aquí...