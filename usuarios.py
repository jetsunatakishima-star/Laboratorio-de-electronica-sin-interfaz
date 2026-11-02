from utilidades import pedir_entero
from componentes import (
    Resistencia, Condensador, Bobina, Diodo, Transistor,
    CircuitoIntegrado, Microcontrolador, Sensor, InstrumentoLab,
)


class Usuario:
    rol = "Usuario"

    def __init__(self, nombre, carnet):
        self.nombre = nombre
        self.carnet = carnet

    @property
    def extra(self):
        return ""

    def mostrar_menu_rol(self, sistema):
        pass


class Estudiante(Usuario):
    rol = "Estudiante"

    def __init__(self, nombre, carnet, carrera):
        super().__init__(nombre, carnet)
        self.carrera = carrera

    @property
    def extra(self):
        return self.carrera

    def mostrar_menu_rol(self, sistema):
        while True:
            print(f"\n MÓDULO ESTUDIANTE: {self.nombre} ({self.carrera})")
            print("1. Ver Inventario Completo del Laboratorio")
            print("2. Pedir un equipo prestado")
            print("3. Devolver el equipo prestado")
            print("4. Ver mi préstamo actual")
            print("5. Cerrar Sesión")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                sistema.mostrar_inventario()
            elif opcion == "2":
                sistema.mostrar_inventario()
                id_item = input("\nIngrese el ID del equipo que desea (Enter para cancelar): ").strip()
                if id_item:
                    sistema.prestar_item(self, id_item)
            elif opcion == "3":
                sistema.devolver_item(self)
            elif opcion == "4":
                sistema.mostrar_prestamo_estudiante(self)
            elif opcion == "5":
                break
            else:
                print(" Opción no válida.")


class Encargado(Usuario):
    rol = "Encargado"

    def __init__(self, nombre, carnet, cubiculo):
        super().__init__(nombre, carnet)
        self.cubiculo = cubiculo

    @property
    def extra(self):
        return self.cubiculo

    def mostrar_menu_rol(self, sistema):
        while True:
            print(f"\n MÓDULO ENCARGADO: {self.nombre} (Cubículo: {self.cubiculo})")
            print("--- AGREGAR COMPONENTE ESPECÍFICO ---")
            print("1. Registrar Resistencia")
            print("2. Registrar Condensador")
            print("3. Registrar Bobina")
            print("4. Registrar Diodo")
            print("5. Registrar Transistor")
            print("6. Registrar Circuito Integrado (IC)")
            print("7. Registrar Microcontrolador")
            print("8. Registrar Sensor")
            print("9. Registrar Instrumento de Medición (Multímetro/Osciloscopio)")
            print("10. Eliminar Componente por ID")
            print("11. Ver Inventario Completo")
            print("12. Ver Usuarios Registrados")
            print("13. Ver Préstamos de Equipos")
            print("14. Cerrar Sesión")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                sistema.agregar_item(Resistencia(
                    input("ID: "), input("Nombre: "), pedir_entero("Cantidad: "), input("Ubicación: "),
                    input("Valor en Ohmios (ej. 220Ω, 10kΩ): "), input("Tolerancia (ej. 5): ")
                ))
            elif opcion == "2":
                sistema.agregar_item(Condensador(
                    input("ID: "), input("Nombre: "), pedir_entero("Cantidad: "), input("Ubicación: "),
                    input("Capacitancia (ej. 100uF, 22pF): "), input("Voltaje Máximo (ej. 50): ")
                ))
            elif opcion == "3":
                sistema.agregar_item(Bobina(
                    input("ID: "), input("Nombre: "), pedir_entero("Cantidad: "), input("Ubicación: "),
                    input("Inductancia (ej. 10mH): "), input("Corriente Máx (ej. 1): ")
                ))
            elif opcion == "4":
                sistema.agregar_item(Diodo(
                    input("ID: "), input("Nombre: "), pedir_entero("Cantidad: "), input("Ubicación: "),
                    input("Tipo de Diodo (ej. LED, Zener, Rectificador): "), input("Corriente Máx: ")
                ))
            elif opcion == "5":
                sistema.agregar_item(Transistor(
                    input("ID: "), input("Nombre: "), pedir_entero("Cantidad: "), input("Ubicación: "),
                    input("Tipo (ej. BJT o MOSFET): "), input("Encapsulado (ej. TO-92, TO-220): ")
                ))
            elif opcion == "6":
                sistema.agregar_item(CircuitoIntegrado(
                    input("ID: "), input("Nombre: "), pedir_entero("Cantidad: "), input("Ubicación: "),
                    input("Número de pines (ej. 8, 14, 40): "), input("Función principal (ej. Compuerta AND, Amplificador): ")
                ))
            elif opcion == "7":
                sistema.agregar_item(Microcontrolador(
                    input("ID: "), input("Nombre: "), pedir_entero("Cantidad: "), input("Ubicación: "),
                    input("Voltaje de operación (ej. 3.3 / 5): "), input("Velocidad de reloj (ej. 16MHz): ")
                ))
            elif opcion == "8":
                sistema.agregar_item(Sensor(
                    input("ID: "), input("Nombre: "), pedir_entero("Cantidad: "), input("Ubicación: "),
                    input("Magnitud que mide (ej. Temperatura, Distancia): "), input("Interfaz de comunicación (ej. I2C, Analógico): ")
                ))
            elif opcion == "9":
                sistema.agregar_item(InstrumentoLab(
                    input("ID: "), input("Nombre: "), pedir_entero("Cantidad: "), input("Ubicación: "),
                    input("Marca (ej. Fluke, Rigol): "), input("Precisión o Rango: ")
                ))
            elif opcion == "10":
                sistema.eliminar_item(input("Ingrese el ID del componente a eliminar: "))
            elif opcion == "11":
                sistema.mostrar_inventario()
            elif opcion == "12":
                sistema.mostrar_usuarios()
            elif opcion == "13":
                sistema.mostrar_prestamos()
            elif opcion == "14":
                break
            else:
                print(" Opción no válida.")