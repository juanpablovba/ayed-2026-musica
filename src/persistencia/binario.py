import struct
from pathlib import Path
from src.dominio.canciones import Cancion
from src.excepciones import ArchivoInvalidoError
from src.tads.lista_enlazada import ListaEnlazada

HEADER = struct.Struct("<4s 1s I")
FORMATO = struct.Struct("<I 40s 40s 40s 15s 2H")
MAGIA = b"AYED"
TEMA = b"M"

def _a_bytes(texto, ancho):
    return texto.encode("utf-8")[:ancho].ljust(ancho, b"\x00")

def _a_texto(datos):
    return datos.rstrip(b"\x00").decode("utf-8")

def _cancion_a_tupla(cancion):
    return (
        int(cancion.id),
        _a_bytes(cancion.titulo,40),
        _a_bytes(cancion.artista, 40),
        _a_bytes(cancion.album, 40),
        _a_bytes(cancion.genero, 15),
        int(cancion.anio),
        int(cancion.duracion),
    )

def _tupla_a_cancion(t):
    return Cancion(
        t[0],
        _a_texto(t[1]),
        _a_texto(t[2]),
        _a_texto(t[3]),
        _a_texto(t[4]),
        t[5],
        t[6],
    )

def guardar_binario(ruta, catalogo):
    """Escribe el header y los registros usando el iterador del catálogo."""
    with open(ruta, "wb") as archivo:
        archivo.write(
            HEADER.pack(MAGIA, TEMA, catalogo.tamanio())
        )

        for cancion in catalogo:
            archivo.write(
                FORMATO.pack(*_cancion_a_tupla(cancion))
            )


def cargar_binario(ruta):
    if not Path(ruta).exists():
        raise ArchivoInvalidoError(f"No existe el archivo: {ruta}")
    with open(ruta, "rb") as archivo:
        cabecera = archivo.read(HEADER.size)
        if len(cabecera) < HEADER.size:
            raise ArchivoInvalidoError("Binario truncado: no tiene el header completo.")
        magia, tema, cantidad = HEADER.unpack(cabecera)
        if magia != MAGIA:
            raise ArchivoInvalidoError("Magia incorrecta: este archivo no es de este TP.")
        if tema != TEMA:
            raise ArchivoInvalidoError("El archivo no es de una biblioteca musical.")
        
        catalogo = ListaEnlazada()

        for _ in range(cantidad):
            datos_registro = archivo.read(FORMATO.size)

            if len(datos_registro) < FORMATO.size:
                raise ArchivoInvalidoError(
                    "Binario truncado: faltan registros."
                )

            catalogo.insertar_al_final(
                _tupla_a_cancion(FORMATO.unpack(datos_registro))
            )

    return catalogo

def actualizar_registro(ruta, posicion, item):
    """Pisa un registro por posición (acceso directo). posicion es 0-based."""
    with open(ruta, "r+b") as archivo:
        cabecera = archivo.read(HEADER.size)
        cantidad = HEADER.unpack(cabecera)[2]
        if posicion < 0 or posicion >= cantidad:
            raise ArchivoInvalidoError("Posición fuera del archivo.")
        archivo.seek(HEADER.size + posicion * FORMATO.size)
        archivo.write(FORMATO.pack(*_cancion_a_tupla(item)))

def alta_binario(ruta, cancion):
    """Agrega un registro al final y actualiza la cantidad del header."""
    with open(ruta, "r+b") as archivo:
        cabecera = archivo.read(HEADER.size)
        magia, tema, cantidad = HEADER.unpack(cabecera)

        archivo.seek(0, 2)
        archivo.write(FORMATO.pack(*_cancion_a_tupla(cancion)))

        archivo.seek(0)
        archivo.write(HEADER.pack(magia, tema, cantidad + 1))


def baja_binario(ruta, posicion):
    """Quita un registro por posición y reescribe los restantes."""
    with open(ruta, "r+b") as archivo:
        cabecera = archivo.read(HEADER.size)
        magia, tema, cantidad = HEADER.unpack(cabecera)
        if posicion < 0 or posicion >= cantidad:
            raise ArchivoInvalidoError("Posición fuera del archivo.")
        registros = [
            archivo.read(FORMATO.size)
            for _ in range(cantidad)
        ]

        del registros[posicion]

        archivo.seek(0)
        archivo.truncate()

        archivo.write(HEADER.pack(magia, tema, len(registros)))

        for datos_registro in registros:
            archivo.write(datos_registro)

