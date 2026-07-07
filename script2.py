# Ejercicios con lista que contiene diccionarios, bucles for y modificaciones dinamicas

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

# Procedemos a cambiar la tarea realizada ahora como completada
id_a_cambiar = int(input("Introduce el id de la tarea completada: "))

for i in tareas_proyecto:
    if i["id"] == id_a_cambiar:
        i["completada"] = True



# RE RETO 3: Usa un bucle 'for' con el método '.items()' para mostrar los 
# datos de la tarea modificada línea por línea con el formato "Clave -> Valor".
# Pista del formato:
# for clave, valor in diccionario_modificado.items():
#     print(f"{clave} -> {valor}")

# Tu código aquí...