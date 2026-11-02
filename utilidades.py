def pedir_entero(mensaje):
    """Pide un número entero y vuelve a preguntar si el dato no es válido."""
    while True:
        valor = input(mensaje)
        try:
            return int(valor)
        except ValueError:
            print(" Debe ingresar un número entero.")