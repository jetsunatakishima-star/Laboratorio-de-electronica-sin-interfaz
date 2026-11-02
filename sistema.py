import sqlite3 as sql
from datetime import datetime

from config import ARCHIVO_DB
from componentes import (
    ComponenteElectronico, Resistencia, Condensador, Bobina, Diodo,
    Transistor, CircuitoIntegrado, Microcontrolador, Sensor, InstrumentoLab,
)


class SistemaInventario:
    def __init__(self):
        self.inicializar_db() 

    def inicializar_db(self):
        print(f"Base de datos en: {ARCHIVO_DB}")
        with sql.connect(ARCHIVO_DB) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS componentes (
                    id TEXT PRIMARY KEY,
                    tipo TEXT,
                    nombre TEXT,
                    cantidad INTEGER,
                    ubicacion TEXT,
                    attr1 TEXT,
                    attr2 TEXT
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rol TEXT NOT NULL,
                    nombre TEXT NOT NULL,
                    carnet TEXT NOT NULL,
                    extra TEXT,
                    primer_ingreso TEXT,
                    ultimo_ingreso TEXT,
                    total_ingresos INTEGER DEFAULT 1,
                    UNIQUE (rol, carnet)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS prestamos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_item TEXT NOT NULL,
                    nombre_item TEXT NOT NULL,
                    carnet TEXT NOT NULL,
                    nombre_estudiante TEXT NOT NULL,
                    fecha_prestamo TEXT NOT NULL,
                    fecha_devolucion TEXT
                )
            ''')

    
    def registrar_usuario(self, usuario):
        """Guarda al usuario si es nuevo; si ya existía, actualiza su último ingreso."""
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with sql.connect(ARCHIVO_DB) as conn:
                existe = conn.execute(
                    "SELECT 1 FROM usuarios WHERE rol = ? AND carnet = ?",
                    (usuario.rol, usuario.carnet)
                ).fetchone()

                if existe:
                    conn.execute('''
                        UPDATE usuarios
                        SET nombre = ?, extra = ?, ultimo_ingreso = ?,
                            total_ingresos = total_ingresos + 1
                        WHERE rol = ? AND carnet = ?
                    ''', (usuario.nombre, usuario.extra, ahora,
                          usuario.rol, usuario.carnet))
                    print(f" Bienvenido de nuevo, {usuario.nombre}.")
                    return False
                else:
                    conn.execute('''
                        INSERT INTO usuarios
                        (rol, nombre, carnet, extra, primer_ingreso, ultimo_ingreso)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (usuario.rol, usuario.nombre, usuario.carnet,
                          usuario.extra, ahora, ahora))
                    print(f" Usuario {usuario.nombre} registrado por primera vez.")
                    return True
        except sql.Error as e:
            print(f" Error al registrar el usuario: {e}")
            return None

    def mostrar_usuarios(self):
        with sql.connect(ARCHIVO_DB) as conn:
            filas = conn.execute('''
                SELECT rol, nombre, carnet, extra, primer_ingreso,
                       ultimo_ingreso, total_ingresos
                FROM usuarios ORDER BY ultimo_ingreso DESC
            ''').fetchall()

        if not filas:
            print("\n No hay usuarios registrados todavía.")
            return

        print("\n--- USUARIOS REGISTRADOS (SQLITE) ---")
        for rol, nombre, carnet, extra, primero, ultimo, total in filas:
            print(f"[{rol}] {nombre} | ID: {carnet} | {extra} | "
                  f"Primer ingreso: {primero} | Último: {ultimo} | Ingresos: {total}")
        print("-------------------------------------")

   
    def agregar_item(self, item):
        tipo, attr1, attr2 = item.get_db_data()
        try:
            with sql.connect(ARCHIVO_DB) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO componentes
                    (id, tipo, nombre, cantidad, ubicacion, attr1, attr2)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (item.id, tipo, item.nombre, item.cantidad,
                      item.ubicacion, attr1, attr2))
            print(f" ¡{item.nombre} registrado correctamente en la base de datos!")
            return True
        except sql.Error as e:
            print(f" Error al registrar en la base de datos: {e}")
            return False

    def eliminar_item(self, id_item):
        with sql.connect(ARCHIVO_DB) as conn:
            pendientes = conn.execute(
                "SELECT COUNT(*) FROM prestamos WHERE id_item = ? AND fecha_devolucion IS NULL",
                (id_item,)
            ).fetchone()[0]
            if pendientes:
                print(f" No se puede eliminar '{id_item}': hay {pendientes} unidad(es) "
                      "prestada(s) sin devolver.")
                return False
            cursor = conn.execute("DELETE FROM componentes WHERE id = ?", (id_item,))
            eliminados = cursor.rowcount

        if eliminados > 0:
            print(f" Elemento con ID '{id_item}' eliminado correctamente.")
        else:
            print(f" No se encontró ningún elemento con el ID '{id_item}'.")
        return eliminados > 0

    
    def _prestamo_activo(self, conn, carnet):
        return conn.execute(
            """SELECT id, id_item, nombre_item, fecha_prestamo
               FROM prestamos WHERE carnet = ? AND fecha_devolucion IS NULL""",
            (carnet,)
        ).fetchone()

    def prestar_item(self, estudiante, id_item):
        """Presta 1 unidad. Si el estudiante tiene un equipo sin devolver, no presta nada."""
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with sql.connect(ARCHIVO_DB) as conn:
                activo = self._prestamo_activo(conn, estudiante.carnet)
                if activo:
                    _, id_prest, nombre_prest, desde = activo
                    print(f" No se le puede prestar otro equipo: aún tiene '{nombre_prest}' "
                          f"(ID {id_prest}) sin devolver desde {desde}.")
                    print(" Devuelva ese equipo antes de pedir otro.")
                    return False

                fila = conn.execute(
                    "SELECT nombre, cantidad FROM componentes WHERE id = ?", (id_item,)
                ).fetchone()
                if not fila:
                    print(f" No existe ningún equipo con el ID '{id_item}'.")
                    return False

                nombre, cantidad = fila
                if cantidad <= 0:
                    print(f" '{nombre}' no tiene unidades disponibles en este momento.")
                    return False

                conn.execute("UPDATE componentes SET cantidad = cantidad - 1 WHERE id = ?",
                             (id_item,))
                conn.execute(
                    """INSERT INTO prestamos
                       (id_item, nombre_item, carnet, nombre_estudiante, fecha_prestamo)
                       VALUES (?, ?, ?, ?, ?)""",
                    (id_item, nombre, estudiante.carnet, estudiante.nombre, ahora)
                )
            print(f" Préstamo realizado: '{nombre}' ({ahora}). Recuerde devolverlo.")
            return True
        except sql.Error as e:
            print(f" Error al registrar el préstamo: {e}")
            return False

    def devolver_item(self, estudiante):
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with sql.connect(ARCHIVO_DB) as conn:
                activo = self._prestamo_activo(conn, estudiante.carnet)
                if not activo:
                    print(" No tiene ningún equipo pendiente por devolver.")
                    return False
                id_prestamo, id_item, nombre, _ = activo
                conn.execute("UPDATE prestamos SET fecha_devolucion = ? WHERE id = ?",
                             (ahora, id_prestamo))
                conn.execute("UPDATE componentes SET cantidad = cantidad + 1 WHERE id = ?",
                             (id_item,))
            print(f" Devolución registrada: '{nombre}'. Ya puede pedir otro equipo.")
            return True
        except sql.Error as e:
            print(f" Error al registrar la devolución: {e}")
            return False

    def mostrar_prestamo_estudiante(self, estudiante):
        with sql.connect(ARCHIVO_DB) as conn:
            activo = self._prestamo_activo(conn, estudiante.carnet)
        if activo:
            _, id_item, nombre, desde = activo
            print(f"\n Tiene prestado: '{nombre}' (ID {id_item}) desde {desde}. Pendiente de devolver.")
        else:
            print("\n No tiene equipos prestados. Puede pedir uno.")

    def mostrar_prestamos(self):
        with sql.connect(ARCHIVO_DB) as conn:
            filas = conn.execute(
                """SELECT nombre_estudiante, carnet, nombre_item, id_item,
                          fecha_prestamo, fecha_devolucion
                   FROM prestamos ORDER BY fecha_prestamo DESC, id DESC"""
            ).fetchall()

        if not filas:
            print("\n No hay préstamos registrados.")
            return

        print("\n--- PRÉSTAMOS DE EQUIPOS (SQLITE) ---")
        for nombre_est, carnet, nombre_item, id_item, desde, hasta in filas:
            estado = f"Devuelto {hasta}" if hasta else "PENDIENTE DE DEVOLVER"
            print(f"{nombre_est} ({carnet}) | {nombre_item} (ID {id_item}) | "
                  f"Prestado: {desde} | {estado}")
        print("-------------------------------------")

    def mostrar_inventario(self):
        with sql.connect(ARCHIVO_DB) as conn:
            filas = conn.execute(
                "SELECT id, tipo, nombre, cantidad, ubicacion, attr1, attr2 FROM componentes"
            ).fetchall()

        if not filas:
            print("\n El inventario está vacío.")
            return

        print("\n--- INVENTARIO DETALLADO DEL LABORATORIO (SQLITE) ---")
        for row in filas:
            item = self._crear_instancia(row)
            if item:
                print(item.obtener_detalles())
        print("-----------------------------------------------------")

    def _crear_instancia(self, row):
        id_item, tipo, nombre, cantidad, ubicacion, attr1, attr2 = row
        clases = {
            "Resistencia": Resistencia,
            "Condensador": Condensador,
            "Bobina": Bobina,
            "Diodo": Diodo,
            "Transistor": Transistor,
            "CircuitoIntegrado": CircuitoIntegrado,
            "Microcontrolador": Microcontrolador,
            "Sensor": Sensor,
            "InstrumentoLab": InstrumentoLab,
        }
        clase = clases.get(tipo)
        if clase:
            return clase(id_item, nombre, cantidad, ubicacion, attr1, attr2)
        return ComponenteElectronico(id_item, nombre, cantidad, ubicacion)