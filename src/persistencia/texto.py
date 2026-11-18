from pathlib import Path
from src.excepciones import ArchivoInvalidoError


# RAIZ = la carpeta del repo (donde está README.md).
# texto.py está en src/persistencia/, así que subimos 3 niveles:
# parents[0]=persistencia parents[1]=src parents[2]=repo
RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data"


def cargar_texto(ruta):
    """Lee un .txt secuencial y devuelve una LISTA DE DICTS, uno por registro.

    La primera línea es el encabezado; cada línea siguiente es un registro
    con campos separados por coma. Si el archivo no existe o una línea
    tiene más/menos campos que el encabezado, lanza ArchivoInvalidoError.
    """
    ruta = Path(ruta)

    if not ruta.exists():
        raise ArchivoInvalidoError(f"No existe el archivo: {ruta}")

    filas = []

    with ruta.open("r", encoding="utf-8") as archivo:
        encabezado = archivo.readline().strip().split(",")

        for linea in archivo:
            linea = linea.strip()

            if not linea:
                continue

            valores = linea.split(",")

            if len(valores) != len(encabezado):
                raise ArchivoInvalidoError(
                    f"Línea con {len(valores)} campos "
                    f"(se esperaban {len(encabezado)}): {linea}"
                )

            fila = dict(zip(encabezado, valores))
            filas.append(fila)

    return filas


def guardar_texto(ruta, filas, encabezados):
    """Escribe el catálogo en .txt: encabezado + un registro por línea.

    filas: iterable de dicts. encabezados: lista con el orden de las columnas.
    """
    ruta = Path(ruta)

    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        archivo.write(",".join(encabezados) + "\n")

        for fila in filas:
            campos = [str(fila[clave]) for clave in encabezados]
            archivo.write(",".join(campos) + "\n")

def cargar_csv(ruta):
    return cargar_texto(ruta)


def guardar_csv(ruta, filas, encabezados):
    return guardar_texto(ruta, filas, encabezados)
