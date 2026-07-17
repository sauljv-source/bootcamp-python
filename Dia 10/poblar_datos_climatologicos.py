import math
import random
from conexion import obtener_coleccion

def calcular_clima_realista(ciudad, indice_mes):
    # Simula el clima real de cada ciudad
    # Curva estacional, usamos el seno para que el mínimo sea en Enero (0) y el máximo en Julio (6)
    factor_termico = -math.cos(2 * math.pi * (indice_mes - 0.5) / 12)
    factor_pluvial = -math.cos(2 * math.pi * indice_mes / 12)

    # Perfiles climatológicos por ciudad
    perfiles = {
        "Badajoz": {
            "temp_anual_media": 16.5,    # Grados celsius
            "amplitud_termica": 11.5,    # Gran diferencia entre invierno y verano (no nos habla sobre el dia o la noche)
            "lluvia_anual_media": 40.0,  # Lluvias moderadas, en mm
            "humedad_base": 55,          # Aire más seco
            "seco_en_verano": True       # El verano desploma la lluvia y la humedad
        },
        "Sevilla": {
            "temp_anual_media": 18.5,
            "amplitud_termica": 11.0,    # Veranos extremadamente calurosos
            "lluvia_anual_media": 45.0,
            "humedad_base": 50,          # Seco
            "seco_en_verano": True
        },
        "Bilbao": {
            "temp_anual_media": 12.5,
            "amplitud_termica": 6.0,     # Temperaturas muy suaves, curva mas plana
            "lluvia_anual_media": 100.0, # Llueve muchísimo
            "humedad_base": 78,          # Humedad altísima constante
            "seco_en_verano": False      # Sigue lloviendo bastante en verano
        },
        "Madrid": {
            "temp_anual_media": 14.5,
            "amplitud_termica": 10.5,    # Clima continental de interior
            "lluvia_anual_media": 35.0,
            "humedad_base": 52,
            "seco_en_verano": True
        },
        "Barcelona": {
            "temp_anual_media": 16.0,
            "amplitud_termica": 7.5,     # El mar suaviza las temperaturas
            "lluvia_anual_media": 50.0,
            "humedad_base": 68,          # Humedad costera constante
            "seco_en_verano": False      # Veranos con lluvias, por el mediterraneo
        }
    }

    perfil = perfiles.get(ciudad)
    
    # Temperatura
    
    # Temp media = media anual + (amplitud * factor_estacional)
    temp_media = perfil["temp_anual_media"] + (perfil["amplitud_termica"] * factor_termico)
    # Sumamos aleatoriamente un numero entre -1,2 y 1,2 por ruido semanal (para que no todos los meses den igual), y round para quedarnos solo con un decimal (debido al random.uniform)
    temp_media = round(temp_media + random.uniform(-1.2, 1.2), 1)
    # Maximas y minimas en cada ciudad
    # En Badajoz/Sevilla la amplitud diurna en verano es salvaje (13) mayor a las demas ciudades
    rango_diario = 13.0 if (perfil["seco_en_verano"] and factor_termico > 0.5) else 8.5
    # Inestabilidad de la atmósfera y el albedo del suelo en algunos dias, round de nuevo para solo un decimal
    ruido_diario = random.uniform(0.5, 2.5)
    temp_max = round(temp_media + (rango_diario / 2) + ruido_diario, 1)
    temp_min = round(temp_media - (rango_diario / 2) - ruido_diario, 1)

    # Precipitaciones
    
    # Si factor_estacional es -1.0 (invierno), el factor_lluvia sube a 1.5, si es 1.0 (verano), el factor_lluvia baja a 0.5
    factor_lluvia = 1.0 - (0.5 * factor_pluvial)
    # En el sur/centro peninsular no llueve casi nada en verano (factor_estacional alto)
    if perfil["seco_en_verano"] and factor_pluvial > 0.3:
        # Veranos secos (casi 0 mm la mayoria de vecesn 70% de las veces)
        precip = random.uniform(0.0, 5.0) if random.random() > 0.3 else 0.0
    else:
        # Random.uniform(), variabilidad interanular (años de sequias y de borrascas, gran consecuencia de la NAO)
        precip = perfil["lluvia_anual_media"] * factor_lluvia * random.uniform(0.6, 1.4)
    
    # Garantizamos ningun numero negativo y redondear a un decimal
    precip = round(max(0.0, precip), 1)

    # Humedad
    # La humedad es inversamente proporcional a la temperatura (el aire caliente retiene más vapor pero baja la humedad relativa)
    # La humedad tambien depende del perfil de la ciudad (ya sea costera o del interior)
    if perfil["seco_en_verano"]:
        humedad_offset = -20 * factor_termico
    else:
        humedad_offset = -12 * factor_termico
    humedad = int(perfil["humedad_base"] + humedad_offset + random.randint(-5, 5))
    # Acotamos los valores entre unos límites reales (15% - 99%)
    humedad = max(15, min(99, humedad))

    return {
        "ciudad": ciudad,
        "mes": [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ][indice_mes],
        "num_mes": indice_mes + 1,
        "temperatura_media": temp_media,
        "temperatura_maxima": temp_max,
        "temperatura_minima": temp_min,
        "precipitaciones_mm": precip,
        "humedad_relativa": humedad
    }

def poblar_clima():
    client, coleccion = obtener_coleccion("clima")
    
    try:
        print("Limpiando registros climatológicos antiguos...")
        coleccion.delete_many({})
        
        ciudades = ["Madrid", "Badajoz", "Bilbao", "Sevilla", "Barcelona"]
        documentos = []
        
        for ciudad in ciudades:
            for indice_mes in range(12):
                doc = calcular_clima_realista(ciudad, indice_mes)
                documentos.append(doc)
                
        print(f"Insertando {len(documentos)} registros mensuales simulados científicamente...")
        coleccion.insert_many(documentos)
        print("Base de datos climatológica poblada con éxito")
        
    except Exception as e:
        print(f"Error al poblar la colección: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    poblar_clima()