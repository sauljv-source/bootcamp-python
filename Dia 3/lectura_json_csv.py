import pandas as pd

def leer_cualquier_fichero(ruta_archivo):
    try:
        if ruta_archivo.endswith('.csv'):
            df = pd.read_csv(ruta_archivo) #DataFrame (df)
            
        elif ruta_archivo.endswith('.json'):
            df = pd.read_json(ruta_archivo)
            
        else:
            print("Formato no compatible.")
            return None
            
        return df

    except FileNotFoundError:
        print(f"El archivo {ruta_archivo} no existe.")
    except Exception as e:
        print(f"Error crítico al procesar el archivo: {e}")


datos_desde_csv = leer_cualquier_fichero("lectura_escritura.csv")
datos_desde_json = leer_cualquier_fichero("lectura_escritura.json")

print(datos_desde_csv)
print(datos_desde_json)