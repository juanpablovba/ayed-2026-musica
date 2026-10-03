from pathlib import Path
from src.config import TEMA
from src.dominio.canciones import listar_catalogo
from src.dominio.cola_reproduccion import ColaReproduccion
from src.dominio.historial_reproduccion import HistorialReproduccion
from src.dominio.playlist import Playlist
from src.dominio.versiones import cargar_catalogo_musical
from src.excepciones import ColeccionLlenaError, ColaVaciaError, PilaVaciaError

TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}

def pendiente():
    print("Todavía no está implementado. Completar en la entrega que corresponde.")

def mostrar_menu():
    """Muestra las opciones disponibles del menú principal."""
    nombre = TEMAS.get(TEMA, TEMA or "(sin tema)")
    print()
    print(f"=== {nombre} — AyED C2 2026 ===")
    print("1. Listar catálogo")
    print("2. Ver detalle")
    print("3. Buscar")
    print("4. Ordenar")
    print("5. Operación recursiva")
    print("6. Playlist")
    print("7. Historial de reproducción")
    print("8. Cola de reproducción")
    print("9. Guardar / cargar archivos")
    print("0. Salir")

def obtener_cancion(catalogo):
    """Solicita un ID y devuelve la canción, o None si no es válida."""
    cancion_id = input("Ingrese el ID de la canción: ").strip()
    if not cancion_id.isdigit():
        print("ID inválido. Debe ser un número.")
        return None
    cancion = catalogo.obtener_cancion(cancion_id)
    if cancion is None:
        print(f"No se encontró la canción con ID {cancion_id}.")
    return cancion

def menu_playlist(playlist, catalogo):
    """Gestiona las opciones de la playlist."""
    opcion = None
    while opcion != "0":
        print()
        print("--- Playlist ---")
        print("1. Agregar canción")
        print("2. Listar playlist")
        print("0. Volver")
        opcion = input("> ").strip()
        if opcion == "0":
            return
        if opcion == "1":
            cancion = obtener_cancion(catalogo)

            if cancion is not None:
                try:
                    playlist.agregar(cancion)
                    print(f"Agregada a la playlist: {cancion.titulo}")
                except ColeccionLlenaError as error:
                    print(error)
        elif opcion == "2":
            if playlist.esta_vacia():
                print("La playlist está vacía.")
            else:
                playlist.listar()
        else:
            print("Opción inválida.")

def menu_historial(historial, catalogo):
    """Gestiona las opciones del historial de reproducción."""
    opcion = None
    while opcion != "0":
        print()
        print("--- Historial de reproducción ---")
        print("1. Registrar canción escuchada")
        print("2. Deshacer última reproducción")
        print("3. Ver última canción escuchada")
        print("0. Volver")
        opcion = input("> ").strip()
        if opcion == "0":
            return
        if opcion == "1":
            cancion = obtener_cancion(catalogo)
            if cancion is not None:
                historial.registrar(cancion)
                print(f"Registrada: {cancion.titulo}")
        elif opcion == "2":
            try:
                cancion = historial.deshacer()
                print(f"Se quitó del historial: {cancion.titulo}")
            except PilaVaciaError as error:
                print(error)
        elif opcion == "3":
            try:
                cancion = historial.ver_ultima()
                print(f"Última canción: {cancion}")
            except PilaVaciaError as error:
                print(error)
        else:
            print("Opción inválida.")

def menu_cola(cola, historial, catalogo):
    """Gestiona las opciones de la cola de reproducción."""
    opcion = None
    while opcion != "0":
        print()
        print("--- Cola de reproducción ---")
        print("1. Agregar canción a la cola")
        print("2. Reproducir siguiente canción")
        print("3. Ver próxima canción")
        print("0. Volver")
        opcion = input("> ").strip()
        if opcion == "0":
            return
        if opcion == "1":
            cancion = obtener_cancion(catalogo)
            if cancion is not None:
                cola.agregar(cancion)
                print(f"Agregada a la cola: {cancion.titulo}")
        elif opcion == "2":
            try:
                cancion = cola.reproducir_siguiente()
                historial.registrar(cancion)
                print(f"Reproduciendo: {cancion}")
            except ColaVaciaError as error:
                print(error)
        elif opcion == "3":
            try:
                cancion = cola.ver_proxima()
                print(f"Próxima canción: {cancion}")
            except ColaVaciaError as error:
                print(error)
        else:
            print("Opción inválida.")

def main():
    if TEMA not in TEMAS:
        print("Seteá TEMA en src/config.py: 'pokedex', 'recetario' o 'musica'.")
        return
    
    raiz = Path(__file__).resolve().parent.parent
    catalogo = cargar_catalogo_musical(
        raiz / "data" / "canciones.csv",
        raiz / "data" / "versiones.csv"
    )
    playlist = Playlist()
    historial = HistorialReproduccion()
    cola = ColaReproduccion()

    opcion = None

    while opcion != "0":
        mostrar_menu()
        opcion = input("> ").strip()

        if opcion == "0":
            print("Chau.")

        elif opcion == "1":
            print(f"Catálogo de canciones")
            listar_catalogo()

        elif opcion == "5":
            cancion = obtener_cancion(catalogo)
            if cancion is None:
                continue
            print(f"Versiones derivadas de '{cancion.titulo}':")
            derivadas = catalogo.listar_versiones(cancion.id)
            if not derivadas:
                print("No hay versiones derivadas.")

        elif opcion == "6":
            menu_playlist(playlist, catalogo)

        elif opcion == "7":
            menu_historial(historial, catalogo)

        elif opcion == "8":
            menu_cola(cola, historial, catalogo)

        elif opcion in {"2", "3", "4", "9"}:
            pendiente()

        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()

