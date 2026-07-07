# 1. Una LISTA que contiene DICCIONARIOS (Estructura de datos compleja)
# Cada tarea es un diccionario con: "id", "descripcion", "encargado" y "completada" (booleano)
tareas_proyecto = [
    {"id": 1, "descripcion": "Configurar Git en el equipo", "encargado": "Saúl", "completada": True},
    {"id": 2, "descripcion": "Resolver ejercicios del Día 2", "encargado": "Saúl", "completada": False},
    {"id": 3, "descripcion": "Subir entregable a GitHub", "encargado": "Tutor", "completada": False}
]

print("--- RECORRIENDO ESTRUCTURAS COMPLEJAS ---")
# RETO: Usa un bucle 'for' para mostrar solo las tareas que NO están completadas
# Tu código aquí...


print("\n--- MODIFICACIÓN DINÁMICA DE DICCIONARIOS ---")
# RETO: Pídele al usuario el 'id' de una tarea y cambia su estado de 'completada' a True.
# Muestra el diccionario modificado usando el método .items() para pintarlo bonito:
# Ejemplo:
# id -> 2
# descripcion -> Resolver ejercicios del Día 2...
# Tu código aquí...