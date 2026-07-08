# Mas ejercicios para manejo de sets

requisitos_puesto = {"Python", "Git", "SQL"}
mis_habilidades = {"Python", "Git"}
futuras_habilidades = {"Docker", "HTML", "JavaScript"}

# Mis habilidades es un subconjunto de los requisitos

if mis_habilidades.issubset(requisitos_puesto):
    print("Contratado")
else:
    print("Faltan competencias para ser contratado")
    
# Mis habilidades no es el mismo conjunto que el de los requisitos

if mis_habilidades == requisitos_puesto:
    print("Contratado")
else:
    print("Falta saber usar SQL para ser contratado")
    
# Añadimos el termino que falta

nueva_habilidad = input("Introduce la nueva habilidad aprendida: ")
mis_habilidades.add(nueva_habilidad)

if mis_habilidades == requisitos_puesto:
    print("Contratado")
else:
    print("Faltan competencias para ser contratado")
    
# Añadimos las habilidades que se necesitaran en el futuro

requisitos_puesto = requisitos_puesto.union(futuras_habilidades)
print(requisitos_puesto)
print(mis_habilidades)

# Que habilidades nos faltan ahora

lista_habilidades = list(mis_habilidades)
lista_requisitos = list(requisitos_puesto)
faltantes = []

for requisito in lista_requisitos:
    if requisito not in lista_habilidades:
        faltantes.append(requisito)

print(f"Habilidades faltantes: {faltantes}")

# Intersección y actualiza el primer conjunto con el resultado, eliminamos las habilidades que faltan

requisitos_puesto.intersection_update(mis_habilidades)
print(requisitos_puesto)
print(mis_habilidades)

lista_requisitos = list(requisitos_puesto)
faltantes = []

for requisito in lista_requisitos:
    if requisito not in lista_habilidades:
        faltantes.append(requisito)

print(f"Habilidades faltantes: {faltantes}")

if len(faltantes) == 0:
    print("Contratado")
else:
    print("Faltan competencias")