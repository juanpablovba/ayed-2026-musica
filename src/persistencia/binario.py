"""Registros de longitud fija con struct.

Layout sugerido (documentar el definitivo en docs/INFORME.md):

Header:
  magia     4s   b'AYED'
  tema      1s   b'P' | b'R' | b'M'
  cantidad  I    unsigned int

El registro depende del tema. Ejemplo Pokédex:
  id          I
  nombre     20s
  tipo1      12s
  tipo2      12s
  hp          H
  ataque      H
  defensa     H
  velocidad   H
  generacion  H
"""

import struct

from pathlib import Path
from src.dominio.canciones import Cancion
from src.excepciones import ArchivoInvalidoError

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
        str(t[0]),
        _a_texto(t[1]),
        _a_texto(t[2]),
        _a_texto(t[3]),
        _a_texto(t[4]),
        str(t[5]),
        str(t[6]),
    )

def guardar_binario(ruta, items):
    items = list(items)
    with open(ruta, "wb") as archivo:
        archivo.write(HEADER.pack(MAGIA, TEMA, len(items)))
        for cancion in items:
            archivo.write(FORMATO.pack(*_cancion_a_tupla(cancion)))


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
        canciones = []
        for _ in range(cantidad):
            datos = archivo.read(FORMATO.size)
            if len(datos) < FORMATO.size:
                raise ArchivoInvalidoError("Binario truncado: faltan registros.")
            canciones.append(_tupla_a_cancion(FORMATO.unpack(datos)))
    return canciones

def actualizar_registro(ruta, posicion, item):
    """Pisa un registro por posición (acceso directo). posicion es 0-based."""
    with open(ruta, "r+b") as archivo:
        cabecera = archivo.read(HEADER.size)
        cantidad = HEADER.unpack(cabecera)[2]
        if posicion < 0 or posicion >= cantidad:
            raise ArchivoInvalidoError("Posición fuera del archivo.")
        archivo.seek(HEADER.size + posicion * FORMATO.size)
        archivo.write(FORMATO.pack(*_cancion_a_tupla(item)))

