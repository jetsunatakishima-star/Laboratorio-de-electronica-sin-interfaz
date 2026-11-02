class ComponenteElectronico:
    def __init__(self, id_item, nombre, cantidad, ubicacion):
        self.id = id_item
        self.nombre = nombre
        self.cantidad = int(cantidad)
        self.ubicacion = ubicacion

    def obtener_detalles(self):
        return f"ID: {self.id} | {self.nombre} | Cantidad: {self.cantidad} | Ubicación: {self.ubicacion}"

    def get_db_data(self):
        return ("General", None, None)


class Resistencia(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, valor_ohmios, tolerancia):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.valor_ohmios = valor_ohmios
        self.tolerancia = tolerancia

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Resistencia] Valor: {self.valor_ohmios} | Tolerancia: {self.tolerancia}%"

    def get_db_data(self):
        return ("Resistencia", self.valor_ohmios, self.tolerancia)


class Condensador(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, capacitancia, voltaje_max):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.capacitancia = capacitancia
        self.voltaje_max = voltaje_max

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Condensador] Capacitancia: {self.capacitancia} | Voltaje Máx: {self.voltaje_max}V"

    def get_db_data(self):
        return ("Condensador", self.capacitancia, self.voltaje_max)


class Bobina(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, inductancia, corriente_max):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.inductancia = inductancia
        self.corriente_max = corriente_max

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Bobina] Inductancia: {self.inductancia} | Corriente Máx: {self.corriente_max}A"

    def get_db_data(self):
        return ("Bobina", self.inductancia, self.corriente_max)


class Diodo(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, tipo_diodo, corriente_max):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.tipo_diodo = tipo_diodo
        self.corriente_max = corriente_max

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Diodo] Tipo: {self.tipo_diodo} | Corriente Máx: {self.corriente_max}A"

    def get_db_data(self):
        return ("Diodo", self.tipo_diodo, self.corriente_max)


class Transistor(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, tipo_transistor, encapsulado):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.tipo_transistor = tipo_transistor  # BJT o MOSFET
        self.encapsulado = encapsulado

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Transistor] Tipo: {self.tipo_transistor} | Encapsulado: {self.encapsulado}"

    def get_db_data(self):
        return ("Transistor", self.tipo_transistor, self.encapsulado)


class CircuitoIntegrado(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, numero_pines, funcion):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.numero_pines = numero_pines
        self.funcion = funcion

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Circuito Integrado] Pines: {self.numero_pines} | Función: {self.funcion}"

    def get_db_data(self):
        return ("CircuitoIntegrado", self.numero_pines, self.funcion)


class Microcontrolador(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, voltaje_operacion, velocidad_reloj):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.voltaje_operacion = voltaje_operacion
        self.velocidad_reloj = velocidad_reloj

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Microcontrolador] Voltaje: {self.voltaje_operacion}V | Reloj: {self.velocidad_reloj}"

    def get_db_data(self):
        return ("Microcontrolador", self.voltaje_operacion, self.velocidad_reloj)


class Sensor(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, magnitud_medida, interfaz):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.magnitud_medida = magnitud_medida
        self.interfaz = interfaz

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Sensor] Mide: {self.magnitud_medida} | Interfaz: {self.interfaz}"

    def get_db_data(self):
        return ("Sensor", self.magnitud_medida, self.interfaz)


class InstrumentoLab(ComponenteElectronico):
    def __init__(self, id_item, nombre, cantidad, ubicacion, marca, precision_o_rango):
        super().__init__(id_item, nombre, cantidad, ubicacion)
        self.marca = marca
        self.precision_o_rango = precision_o_rango

    def obtener_detalles(self):
        base = super().obtener_detalles()
        return f"{base} | [Instrumento] Marca: {self.marca} | Rango/Precisión: {self.precision_o_rango}"

    def get_db_data(self):
        return ("InstrumentoLab", self.marca, self.precision_o_rango)