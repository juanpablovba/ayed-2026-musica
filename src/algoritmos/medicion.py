# Entrega 4

import time
from pathlib import Path
from src.algoritmos.busqueda import busqueda_binaria, busqueda_lineal
from src.algoritmos.ordenamiento import ordenar_insercion, ordenar_seleccion
from src.dominio.versiones import cargar_catalogo_musical

FACTORES = (1, 10, 50)
TITULO_INEXISTENTE = "zzz no existe"


def clave_titulo(cancion):
    return cancion.titulo.casefold()


def medir(funcion, repeticiones):
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        funcion()
    fin = time.perf_counter()
    return (fin - inicio) / repeticiones


def main():
    raiz = Path(__file__).resolve().parent.parent.parent
    catalogo = cargar_catalogo_musical(
        raiz / "data" / "canciones.csv",
        raiz / "data" / "versiones.csv",
    )
    original = list(catalogo.canciones_por_id.values())

    print("| Operación | n | segundos |")
    print("| --- | --- | --- |")
    for factor in FACTORES:
        datos = original * factor
        n = len(datos)
        ordenados = ordenar_insercion(datos, clave_titulo)

        tiempo = medir(lambda: busqueda_lineal(datos, TITULO_INEXISTENTE, clave_titulo), 2000)
        print(f"| búsqueda lineal (peor caso) | {n} | {tiempo:.6f} |")
        tiempo = medir(lambda: busqueda_binaria(ordenados, TITULO_INEXISTENTE, clave_titulo), 2000)
        print(f"| búsqueda binaria (peor caso) | {n} | {tiempo:.6f} |")

        repeticiones = 20 if n < 1000 else 1
        tiempo = medir(lambda: ordenar_seleccion(datos, clave_titulo), repeticiones)
        print(f"| ordenar por selección | {n} | {tiempo:.6f} |")
        tiempo = medir(lambda: ordenar_insercion(datos, clave_titulo), repeticiones)
        print(f"| ordenar por inserción (desordenada) | {n} | {tiempo:.6f} |")
        tiempo = medir(lambda: ordenar_insercion(ordenados, clave_titulo), repeticiones)
        print(f"| ordenar por inserción (ya ordenada) | {n} | {tiempo:.6f} |")


if __name__ == "__main__":
    main()