from conexion import obtener_coleccion

def mostrar_menu():
    print("\n               CONSOLA DE ANÁLISIS METEOROLÓGICO")
    print("-"*63)
    print(" 1. Desglose mensual de una ciudad específica de nuestra lista")
    print(" 2. Ranking de temperaturas máximas, mínimas y media anual")
    print(" 3. Ranking de lluvias (precipitaciones acumuladas)")
    print(" 4. Ranking de humedad relativa por ciudad")
    print(" 5. Salir")

def generar_informe_clima():
    client, coleccion = obtener_coleccion("clima")
    
    try:
        ciudades_validas = coleccion.distinct("ciudad")
        if not ciudades_validas:
            print("La colección está vacía. Ejecuta primero 'poblar_clima.py'.")
            return
        
        while True:
            mostrar_menu()
            opcion = input("\nSelecciona una opción (1-5): ").strip()
            
            if opcion == "1":
                print(f"\nEstaciones disponibles bajo supervisión: {', '.join(ciudades_validas)}")
                print("(Escribe 'salir' para volver al menú principal)")
                
                volver_al_menu = False
                while True:
                    entrada = input("Introduce la ciudad a visualizar: ").strip()
                    if entrada.lower() == "salir":
                        volver_al_menu = True
                        break
                    ciudad_elegida = entrada.title()
                    if ciudad_elegida in ciudades_validas:
                        break
                    print(f"En {ciudad_elegida} no hay estación meteorológica. Inténtalo de nuevo.")
                
                if volver_al_menu:
                    continue
                
                pipeline = [
                    {"$match": {"ciudad": ciudad_elegida}},
                    {"$sort": {"num_mes": 1}},
                    {
                        "$project": {
                            "_id": 0,
                            "mes": 1,
                            "temp_media": "$temperatura_media",
                            "temp_max": "$temperatura_maxima",
                            "temp_min": "$temperatura_minima",
                            "precip": "$precipitaciones_mm",
                            "humedad": "$humedad_relativa"
                        }
                    }
                ]
                resultados = list(coleccion.aggregate(pipeline))
                
                print(f"\nREGISTRO MENSUAL DETALLADO PARA {ciudad_elegida.upper()}")
                print("="*77)
                print(f"| {'Mes':<12} | {'Temp. media'} | {'Temp. máx'} | {'Temp. mín'} | {'Lluvia':<6} | {'Humedad (%)'} | ")
                print("="*77)
                for mes in resultados:
                    print(f"| {mes['mes']:<12} | {mes['temp_media']:<11.1f} | {mes['temp_max']:<9.1f} | {mes['temp_min']:<9.1f} | {mes['precip']:<6.1f} | {mes['humedad']:<11} | ")
                print("="*77)
                
            elif opcion == "2":
                pipeline = [
                    {
                        "$group": {
                            "_id": "$ciudad",
                            "maxima_record": {"$max": "$temperatura_maxima"},
                            "minima_record": {"$min": "$temperatura_minima"},
                            "media_anual": {"$avg": "$temperatura_media"}
                        }
                    },
                ]

                datos_temperaturas = list(coleccion.aggregate(pipeline))

                print("\nRANKING DE TEMPERATURAS MÁXIMAS")
                print("-"*38)
                datos_temperaturas.sort(key=lambda x: x["maxima_record"], reverse=True)
                for r in datos_temperaturas:
                    print(f" - {r['_id']:<10} | Máxima Récord: {r['maxima_record']:>4.1f}°C")

                print("\nRANKING DE TEMPERATURAS MÍNIMAS")
                print("-"*38)
                # Sin reverse=True para que el menor vaya arriba, si no ponemos nada por convenio será False
                datos_temperaturas.sort(key=lambda x: x["minima_record"])
                for r in datos_temperaturas:
                    print(f" - {r['_id']:<10} | Mínima Récord: {r['minima_record']:>4.1f}°C")

                print("\nRANKING DE TEMPERATURA MEDIA ANUAL")
                print("-"*38)
                datos_temperaturas.sort(key=lambda x: x["media_anual"], reverse=True)
                for r in datos_temperaturas:
                    print(f" - {r['_id']:<10} | Media Anual:   {r['media_anual']:>4.1f}°C")
                
            elif opcion == "3":
                print("\nRANKING DE PRECIPITACIONES ANUALES ACUMULADAS")
                print("-"*51)
                pipeline = [
                    {
                        "$group": {
                            "_id": "$ciudad",
                            "total_lluvia": {"$sum": "$precipitaciones_mm"}
                        }
                    },
                    {"$sort": {"total_lluvia": -1}}  # De más lluviosa a más seca
                ]
                for r in coleccion.aggregate(pipeline):
                    print(f" - {r['_id']:<10} | Lluvia total: {r['total_lluvia']:>5.1f} mm acumulados")
                
            elif opcion == "4":
                print("\nRANKING DE HUMEDAD RELATIVA REGISTRADOS")
                print("-"*58)
                pipeline = [
                    {
                        "$group": {
                            "_id": "$ciudad",
                            "max_humedad": {"$max": "$humedad_relativa"},
                            "min_humedad": {"$min": "$humedad_relativa"}
                        }
                    },
                    {"$sort": {"max_humedad": -1}}
                ]
                for r in coleccion.aggregate(pipeline):
                    print(f" - {r['_id']:<10} | Humedad máxima: {r['max_humedad']}% | Humedad mínima: {r['min_humedad']}%")
                
            elif opcion == "5":
                print("\nCerrando aplicación de análisis.")
                break
            else:
                print("Opción no válida. Por favor, introduce un número del 1 al 5.")
                
    except Exception as e:
        print(f"Error inesperado en el análisis: {e}")
        
    finally:
        client.close()
        print("Conexión a MongoDB cerrada de forma segura.")

if __name__ == "__main__":
    generar_informe_clima()