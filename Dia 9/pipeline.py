# Pipeline de agregación: $match, $group, $sort, $project. Cálculo de estadísticas simples (conteos, medias)

from conexion import obtener_coleccion

# Ingreso total de cada componente vendido en cada sucursal

def analisis_productos_sucursal():
    client, coleccion = obtener_coleccion("ventas_tecnológicas")
    
    try:
        sucursales_validas = coleccion.distinct("sucursal")
    
        if not sucursales_validas:
            print("La colección está vacía. Por favor, ejecuta 'poblar_datos.py' antes de realizar análisis.")
            return
        
        while True:
            print("\nREGISTRO DE VENTAS, SUCURSALES DISPONIBLES")
            print("-"*50)
            print(", ".join(sucursales_validas))
            
            while True:
                sucursal_elegida = input("\nIntroduce la sucursal que deseas visualizar: ").strip().title()
                if sucursal_elegida in sucursales_validas:
                    break
                print(f"En {sucursal_elegida} no hay una sucursal de nuestra empresa. Intentalo de nuevo.")
            
            pipeline = [
                {
                    "$match": {
                        "sucursal": sucursal_elegida
                    }
                },
                {
                    "$group": {
                        "_id": "$producto",
                        "total_unidades": { "$sum": "$cantidad" },
                        "ingreso_acumulado": { 
                            "$sum": { "$multiply": ["$precio_unidad", "$cantidad"] } 
                        }
                    }
                },
                {
                    "$sort": {
                        "ingreso_acumulado": -1
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "producto": "$_id",
                        "unidades_vendidas": "$total_unidades",
                        "ingresos_euros": { "$round": ["$ingreso_acumulado", 2] }
                    }
                }
            ]

            resultados = list(coleccion.aggregate(pipeline))
            
            if not resultados:
                print("No hay datos en la colección 'ventas'.")
                continue
                
            print(f"\nRENDIMIENTO DE PRODUCTOS VENDIDOS EN {sucursal_elegida.upper()}")
            print("-"*50)
            print(f"{'Producto':<15} | {'Uds. Vendidas':<15} | {'Ingresos':<10}")
            print("-"*50)
            
            for i in resultados:
                print(f"{i['producto']:<15} | {i['unidades_vendidas']:<15} | {i['ingresos_euros']:<10.2f} €")
            print("="*55)
              
            salir_programa = False
            while True:
                otro = input("¿Deseas consultar alguna otra sucursal? (si/no): ").strip().lower()
                if otro in ["si", "sí"]:
                    break
                elif otro == "no":
                    salir_programa = True
                    break
                else:
                    print("Respuesta no válida. Por favor, introduce únicamente 'si' o 'no'.")

            if salir_programa:
                break
                
    except Exception as e:
        print(f"Error inesperado: {e}")
    
    finally:
        client.close()
        print("\nConexión a MongoDB cerrada.")

if __name__ == "__main__":
    analisis_productos_sucursal()