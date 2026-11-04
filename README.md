Explicación del sistema de inventario en consola (sin interfaz gráfica)

1. Objetivo y resumen
El sistema gestiona el inventario de un laboratorio de electrónica desde la terminal: el usuario elige opciones de un menú escribiendo números, y los datos quedan guardados en SQLite3.
La versión de consola incluye:
• Persistencia en SQLite: los datos viven en db/inventario.db, con las tablas componentes, usuarios y prestamos.
• Dos roles: el Estudiante consulta el inventario y pide equipos prestados; el Encargado registra y elimina componentes y revisa usuarios y préstamos.
• Registro de usuarios: cada ingreso queda guardado, con la fecha del primer ingreso, la del último y el total de ingresos.
• Préstamos: si un estudiante tiene un equipo sin devolver y pide otro, no se le presta nada.
2. Estructura del proyecto
La versión de consola usa seis archivos. Cada uno tiene una sola responsabilidad, y solo sistema.py habla con la base de datos.
Archivo
Qué contiene
Papel en el sistema
main_consola.py
Función main() con el menú principal
Punto de entrada: pide el rol, crea al usuario y abre su menú
usuarios.py
Usuario, Estudiante, Encargado
Datos del usuario y el menú de cada rol
sistema.py
Clase SistemaInventario
Todo el acceso a SQLite: tablas, usuarios, componentes y préstamos
componentes.py
ComponenteElectronico y 9 subclases
Datos de cada tipo de equipo
utilidades.py
pedir_entero
Valida que la cantidad sea un número entero
config.py
ARCHIVO_DB
Ruta de la base de datos; crea la carpeta db si no existe
Si trabajas solo con la consola, interfaz.py no hace falta. Ningún archivo de la lista lo importa.
3. Cómo funciona el programa en la terminal
Al ejecutar main_consola.py, la función main() crea un SistemaInventario (que prepara la base de datos) y muestra el menú principal en un ciclo: 1 Estudiante, 2 Encargado, 3 Salir.
Si se elige un rol, el programa pide nombre, carnet o código, y carrera o cubículo con input(). Luego crea un objeto Estudiante o Encargado, llama a registrar_usuario() para guardarlo en SQLite y abre su menú con mostrar_menu_rol(). Al cerrar sesión, vuelve al menú principal.
Menú del Estudiante (Estudiante.mostrar_menu_rol):
Opción
Qué hace
Método que usa
1
Ver el inventario completo
mostrar_inventario()
2
Pedir un equipo prestado: muestra el inventario y pide el ID (Enter cancela)
prestar_item(self, id_item)
3
Devolver el equipo prestado
devolver_item(self)
4
Ver su préstamo actual
mostrar_prestamo_estudiante(self)
5
Cerrar sesión
Sale del menú
Menú del Encargado (Encargado.mostrar_menu_rol):
Opción
Qué hace
Método que usa
1 a 9
Registrar un componente: resistencia, condensador, bobina, diodo, transistor, circuito integrado, microcontrolador, sensor o instrumento
agregar_item() con la clase del tipo elegido
10
Eliminar un componente por ID
eliminar_item()
11
Ver el inventario completo
mostrar_inventario()
12
Ver los usuarios registrados
mostrar_usuarios()
13
Ver los préstamos de equipos
mostrar_prestamos()
14
Cerrar sesión
Sale del menú
Al registrar un componente, la cantidad se pide con pedir_entero(), que repite la pregunta hasta que se escriba un número entero.
4. Cómo se usa SQLite
Todo el acceso a la base está en SistemaInventario. Cada método abre la conexión con with sql.connect(ARCHIVO_DB) as conn, lo que guarda los cambios (commit) al terminar y los deshace si algo falla.
Las tres tablas se crean en inicializar_db(), que se llama desde el constructor:
Tabla
Qué guarda
Detalles
componentes
Un equipo por fila
Clave id (texto). attr1 y attr2 guardan las dos características propias de cada tipo, que entrega el método get_db_data() del componente
usuarios
Un usuario por rol y carnet
Restricción UNIQUE (rol, carnet); guarda primer ingreso, último ingreso y total de ingresos
prestamos
Un préstamo por fila
Si fecha_devolucion está vacía, el préstamo sigue pendiente
Métodos de SistemaInventario:
Método
Qué hace
inicializar_db()
Crea las tres tablas si no existen
registrar_usuario(usuario)
Inserta al usuario si es nuevo; si ya existe, actualiza su último ingreso y suma 1 al contador
mostrar_usuarios()
Lista los usuarios registrados
agregar_item(item)
Guarda un componente con INSERT OR REPLACE; un ID repetido reemplaza al anterior
eliminar_item(id_item)
Borra el componente, salvo que tenga unidades prestadas
mostrar_inventario()
Lee la tabla y reconstruye cada fila como objeto de su clase
_crear_instancia(fila)
Convierte una fila en Resistencia, Sensor, etc., según el campo tipo
prestar_item(estudiante, id_item)
Presta una unidad si se cumplen las reglas del préstamo
devolver_item(estudiante)
Registra la devolución y suma una unidad
mostrar_prestamo_estudiante(estudiante)
Muestra el equipo que el estudiante tiene prestado
mostrar_prestamos()
Lista todos los préstamos, pendientes y devueltos
_prestamo_activo(conn, carnet)
Busca si un carnet tiene un préstamo sin devolver
El archivo sistema.py también trae cuatro métodos obtener_* que devuelven datos para la ventana. La consola no los usa, así que no afectan su funcionamiento.
5. Relación con el diagrama de casos de uso
Cada caso de uso del diagrama corresponde a una opción del menú de la consola, y cada opción llama a un método de SistemaInventario.
Actor Estudiante
Caso de uso
Opción del menú
Método que lo ejecuta
Ingresar al sistema
Inicio en main_consola.py
registrar_usuario()
Ver inventario
1
mostrar_inventario()
Pedir equipo prestado
2
prestar_item()
Devolver equipo
3
devolver_item()
Ver mi préstamo
4
mostrar_prestamo_estudiante()
Cerrar sesión
5
Sale del menú
Actor Encargado
Caso de uso
Opción del menú
Método que lo ejecuta
Ingresar al sistema
Inicio en main_consola.py
registrar_usuario()
Registrar componente (9 tipos)
1 a 9
agregar_item()
Eliminar componente
10
eliminar_item()
Ver inventario
11
mostrar_inventario()
Ver usuarios registrados
12
mostrar_usuarios()
Ver préstamos
13
mostrar_prestamos()
Cerrar sesión
14
Sale del menú
Relaciones entre casos de uso
• include: Pedir equipo prestado incluye Ver inventario, porque el estudiante necesita ver la lista para elegir un ID. En el código, la opción 2 llama primero a mostrar_inventario().
• extend: las validaciones del préstamo (ya tiene un equipo, ID inexistente, sin unidades) extienden el caso Pedir equipo prestado. Solo se activan cuando se da esa condición y rechazan el préstamo.
• Eliminar componente tiene una condición parecida: no se ejecuta si hay unidades prestadas.
En la consola no hay pantalla de login con contraseña. El usuario elige su rol y escribe su nombre y carnet, y con eso el sistema lo registra.
6. Relación con el diagrama de clases
Clases por archivo
Archivo
Clases
Papel
componentes.py
ComponenteElectronico y sus 9 subclases
Modelan los equipos del laboratorio
usuarios.py
Usuario, Estudiante, Encargado
Modelan a las personas y contienen los menús de consola
sistema.py
SistemaInventario
Centraliza toda la lógica y el acceso a SQLite
main_consola.py
Ninguna (módulo con main())
Punto de entrada del programa
config.py, utilidades.py
Ninguna (módulos)
Ruta de la base de datos y pedir_entero()
Herencia
• Resistencia, Condensador, Bobina, Diodo, Transistor, CircuitoIntegrado, Microcontrolador, Sensor e InstrumentoLab heredan de ComponenteElectronico. Cada una agrega sus dos atributos propios y redefine obtener_detalles() y get_db_data() (polimorfismo).
• Estudiante y Encargado heredan de Usuario. Cada una define su atributo rol y su propio mostrar_menu_rol().
Dependencias
• main_consola.py crea SistemaInventario y los objetos Estudiante o Encargado.
• Usuario usa a SistemaInventario para ejecutar las opciones del menú.
• Encargado crea objetos de los 9 tipos de componente y usa pedir_entero().
• SistemaInventario crea instancias de componentes al leer la tabla y usa config.py para la ruta de la base.
• SistemaInventario lee y escribe en las tablas componentes, usuarios y prestamos. La tabla prestamos se enlaza con componentes por id_item y con usuarios por carnet.
Diferencia con el diagrama que ya tienes: el diagrama de clases hecho antes muestra el archivo de entrada como main.py. En la versión de consola ese archivo es main_consola.py. Las clases, la herencia y las tablas son exactamente las mismas.
7. Reglas del préstamo y dónde se aplican
Regla
Dónde se aplica
Cómo funciona
Un solo equipo sin devolver por carnet
prestar_item() con _prestamo_activo()
Si hay un préstamo con fecha_devolucion vacía, se rechaza la solicitud y no se presta nada
El equipo debe existir
prestar_item()
Si el ID no está en componentes, se avisa y se cancela
Debe haber unidades
prestar_item()
Si cantidad es 0, no se presta
Al prestar, baja el stock
prestar_item()
cantidad = cantidad - 1
Al devolver, sube el stock
devolver_item()
cantidad = cantidad + 1
No se borra un equipo prestado
eliminar_item()
Si hay préstamos pendientes de ese ID, no se elimina
El préstamo sobrevive al cierre del programa
Tabla prestamos
Está guardado en el archivo .db; al volver a entrar con el mismo carnet, el préstamo sigue pendiente
Todas las reglas viven en SistemaInventario, no en el menú. Por eso la versión con interfaz gráfica, que usa la misma clase, se comporta igual.
8. Cómo ejecutarlo, limitaciones y diferencias con la versión gráfica
Cómo ejecutarlo
1. Pon en la misma carpeta main_consola.py, usuarios.py, sistema.py, componentes.py, utilidades.py y config.py, con esos nombres exactos.
2. Abre una terminal en esa carpeta y ejecuta python main_consola.py.
3. La carpeta db y el archivo inventario.db se crean solos la primera vez.
Limitaciones
• No hay contraseña: el rol se elige al entrar y cualquiera puede escoger el de Encargado.
• Un estudiante solo puede tener un equipo prestado a la vez y siempre se presta una unidad.
• Registrar un componente con un ID que ya existe lo reemplaza (INSERT OR REPLACE).
• La interacción es solo por texto: hay que escribir los datos y las opciones a mano.
Consola frente a interfaz gráfica
