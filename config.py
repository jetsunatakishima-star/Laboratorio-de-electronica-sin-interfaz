import os

CARPETA = os.path.dirname(os.path.abspath(__file__))


CARPETA_DB = os.path.join(CARPETA, "db")
os.makedirs(CARPETA_DB, exist_ok=True)

ARCHIVO_DB = os.path.join(CARPETA_DB, "inventario.db")