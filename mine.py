from sistema import SistemaInventario
from usuarios import Estudiante, Encargado


def main():
    sistema = SistemaInventario()

    while True:
        print("\n=== SISTEMA DE GESTIÓN - LAB DE ELECTRÓNICA ===")
        print("1. Ingresar como Estudiante")
        print("2. Ingresar como Encargado de Laboratorio")
        print("3. Salir")

        rol = input("Seleccione una opción: ")

        if rol == "1":
            usuario = Estudiante(input("Nombre: "), input("Carnet: "), input("Carrera: "))
            sistema.registrar_usuario(usuario)
            usuario.mostrar_menu_rol(sistema)
        elif rol == "2":
            usuario = Encargado(input("Nombre: "), input("Código empleado: "), input("Cubículo: "))
            sistema.registrar_usuario(usuario)
            usuario.mostrar_menu_rol(sistema)
        elif rol == "3":
            print(" Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print(" Opción inválida.")


if __name__ == "__main__":
    main()