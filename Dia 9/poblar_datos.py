# Script de prueba para poblar nuestra base de datos sin tener que ir a mano uno a uno

from conexion import obtener_coleccion
import random

def generar_venta_tecnológica():
    productos_con_precios = {
        "Teclado": (15.0, 80.0),
        "Computador": (500.0, 1200.0),
        "Portatil": (400.0, 1500.0),
        "Telefono movil": (150.0, 1000.0),
        "Telefono fijo": (15.0, 45.0),
        "Ratón": (10.0, 50.0),
        "Pantalla": (100.0, 350.0),
        "Tablet": (120.0, 600.0),
        "Auriculares": (20.0, 150.0),
        "Televisor": (250.0, 1200.0),
        "Altavoces": (30.0, 200.0)
    }
    sucursales = ["Madrid", "Barcelona", "Sevilla", "Navarra", "Bilbao", "Murcia", "Salamanca", "Cordoba", "Badajoz"]
    metodos_pago = ["Efectivo", "Tarjeta", "Transferencia bancaria", "Bizum", "Paypal"]
    
    producto = random.choice(list(productos_con_precios.keys()))
    categoria = "Tecnología"
    
    precio_min, precio_max = productos_con_precios[producto]
    precio_unidad = round(random.uniform(precio_min, precio_max), 2)

    cantidad = random.randint(1,3)
    sucursal = random.choice(sucursales)
    metodo_pago = random.choice(metodos_pago)
    
    return {
  "producto": producto,
  "categoria": categoria,
  "precio_unidad": precio_unidad,
  "cantidad": cantidad,
  "sucursal": sucursal,
  "metodo_pago": metodo_pago
}

def poblar_datos():
    client, coleccion = obtener_coleccion("ventas_tecnológicas")
    
    try:
        # Limpieza para garantizar que no haya duplicaciones
        print("Limpiando todos los datos anteriores de la coleccion...")
        resultado_borrado = coleccion.delete_many({})
        print(f"Se han eliminado {resultado_borrado.deleted_count} ventas tecnológicas.")
        
        ventas_nuevas = [generar_venta_tecnológica() for i in range(100)]
        
        print(f"\nInsertando {len(ventas_nuevas)} ventas en la base de datos...")
        resultado_insercion = coleccion.insert_many(ventas_nuevas)
        print(f"Se han insertado {len(resultado_insercion.inserted_ids)} ventas nuevas.")
        
    except Exception as e:
        print(f"Error al poblar la base de datos: {e}")
    finally:
        client.close()
        print("Conexion a MongoDB cerrada.")

if __name__ == "__main__":
    poblar_datos()