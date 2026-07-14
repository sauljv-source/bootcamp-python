def comprobar_entero_mayor_que_1(mensaje, error_mensaje1, error_mensaje2):
    while True:
        try:
            entrada = int(input(mensaje).strip())
            if entrada >= 1:
                return entrada
            print(error_mensaje1)
        except ValueError:
            print(error_mensaje2)
            
def comprobar_texto(mensaje, error_mensaje, comas=False):
    while True:
        entrada = input(mensaje).strip()
        texto_a_validar = entrada.replace(" ", "")
        if comas:
            texto_a_validar = texto_a_validar.replace(",", "")
            
        if texto_a_validar.isalpha() and entrada:
            return entrada
        print(error_mensaje)