import csv


def cargar_csv(ruta):
    """Carga secuencial. Devuelve una lista de dicts."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)


def guardar_csv(ruta, filas, encabezados):
    raise NotImplementedError
