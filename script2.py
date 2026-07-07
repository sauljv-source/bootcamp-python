# =====================================================================
# STEP 1: La Estructura Compleja (Lista que contiene Diccionarios)
# =====================================================================
# Esto simula una base de datos con las tareas del bootcamp.
tareas_proyecto = [
    {"id": 1, "descripcion": "Configurar Git en el equipo", "encargado": "Saúl", "completada": True},
    {"id": 2, "descripcion": "Resolver ejercicios del Día 2", "encargado": "Saúl", "completada": False},
    {"id": 3, "descripcion": "Subir entregable a GitHub", "encargado": "Tutor", "completada": False}
]

# =====================================================================
# STEP 2: Filtrado con Bucle 'for' y condicionales
# =====================================================================
print("--- TAREAS PENDIENTES DE SAÚL ---")

# RE RETO 1: Haz un bucle 'for' que recorra 'tareas_proyecto'.
# Debe comprobar si el encargado es "Saúl" y si la tarea NO está completada (completada == False).
# Si cumple las condiciones, imprime su descripción.

# Tu código aquí...


# =====================================================================
# STEP 3: Modificación Dinámica y Método .items()
# =====================================================================
print("\n--- ACTUALIZAR ESTADO DE TAREA ---")

# El usuario decide qué tarea ha terminado
id_a_cambiar = int(input("Introduce el ID de la tarea que has completado (ej: 2): "))

# RE RETO 2: Recorre la lista de tareas. Busca el diccionario que tenga ese "id".
# Cuando lo encuentres, cambia su valor de "completada" a True.

# Tu código aquí...


print("\n--- INFORME FINAL DE LA TAREA MODIFICADA ---")
# RE RETO 3: Usa un bucle 'for' con el método '.items()' para mostrar los 
# datos de la tarea modificada línea por línea con el formato "Clave -> Valor".
# Pista del formato:
# for clave, valor in diccionario_modificado.items():
#     print(f"{clave} -> {valor}")

# Tu código aquí...