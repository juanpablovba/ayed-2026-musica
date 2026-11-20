from src.persistencia.texto import guardar_texto
from pathlib import Path
from src.algoritmos.busqueda import busqueda_binaria, busqueda_lineal
from src.algoritmos.ordenamiento import ordenar_insercion, ordenar_seleccion
from src.config import TEMA
from src.dominio.canciones import Cancion, listar_catalogo
from src.dominio.cola_reproduccion import ColaReproduccion
from src.dominio.historial_reproduccion import HistorialReproduccion
from src.dominio.playlist import Playlist
from src.dominio.versiones import CatalogoMusical, cargar_catalogo_musical
from src.persistencia.binario import (
    cargar_binario,
    guardar_binario,
    actualizar_registro,
    alta_binario,
    baja_binario,
)
from src.excepciones import (
    ArchivoInvalidoError,
    ItemNoEncontradoError,
    ColeccionLlenaError,
    ColaVaciaError,
    PilaVaciaError,
)

TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}

ENCABEZADOS = ["id", "titulo", "artista", "album", "genero", "anio", "duracion_seg"]

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
    print("6. Gestionar catálogo / playlist")
    print("7. Historial de reproducción")
    print("8. Cola de reproducción")
    print("9. Guardar / cargar archivos")
    print("0. Salir")

def obtener_cancion(catalogo):
    """Solicita un ID y devuelve la canción, o None si no es válida."""
    try:
        cancion_id = int(input("Ingrese el ID de la canción: ").strip())
    except ValueError:
        print("ID inválido. Debe ser un número entero.")
        return None

    cancion = catalogo.obtener_cancion(cancion_id)

    if cancion is None:
        print(f"No se encontró la canción con ID {cancion_id}.")

    return cancion

def clave_titulo(cancion):
    return cancion.titulo.casefold()

CRITERIOS_ORDEN = {
    "1": ("título", clave_titulo),
    "2": ("artista", lambda cancion: cancion.artista.casefold()),
    "3": ("año", lambda cancion: int(cancion.anio)),
    "4": ("duración", lambda cancion: int(cancion.duracion)),
}

def menu_buscar(canciones, orden_actual):
    print()
    print("--- Buscar por título ---")
    print("1. Búsqueda lineal")
    print("2. Búsqueda binaria")
    print("0. Volver")
    opcion = input("> ").strip()
    if opcion not in {"1", "2"}:
        if opcion != "0":
            print("Opción inválida.")
        return canciones, orden_actual

    titulo = input("Ingrese el título: ").strip().casefold()
    if opcion == "1":
        cancion = busqueda_lineal(canciones, titulo, clave_titulo)
    else:
        if orden_actual != "título":
            canciones = ordenar_insercion(canciones, clave_titulo)
            orden_actual = "título"
            print("El catálogo no estaba ordenado por título: se ordenó para usar búsqueda binaria.")
        cancion = busqueda_binaria(canciones, titulo, clave_titulo)

    if cancion is None:
        print("No se encontró ninguna canción con ese título.")
    else:
        print(cancion)
    return canciones, orden_actual

def mostrar_canciones(canciones, limite=10):
    for cancion in canciones[:limite]:
        print(cancion)
    if len(canciones) > limite:
        print(f"... (se muestran {limite} de {len(canciones)})")

def menu_ordenar(canciones, orden_actual):
    print()
    print("--- Ordenar catálogo ---")
    print("Ordenar por: 1) Título  2) Artista  3) Año  4) Duración  0) Volver")
    criterio = input("> ").strip()
    if criterio == "0":
        return canciones, orden_actual
    if criterio not in CRITERIOS_ORDEN:
        print("Opción inválida.")
        return canciones, orden_actual

    print("Algoritmo: 1) Selección  2) Inserción")
    algoritmo = input("> ").strip()
    if algoritmo not in {"1", "2"}:
        print("Opción inválida.")
        return canciones, orden_actual

    nombre, clave = CRITERIOS_ORDEN[criterio]
    if algoritmo == "1":
        canciones = ordenar_seleccion(canciones, clave)
    else:
        canciones = ordenar_insercion(canciones, clave)
    print(f"Catálogo ordenado por {nombre}.")
    mostrar_canciones(canciones)
    return canciones, nombre

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

def filas_del_catalogo(catalogo):
    filas = []
    for cancion in catalogo:
        filas.append({
            "id": cancion.id,
            "titulo": cancion.titulo,
            "artista": cancion.artista,
            "album": cancion.album,
            "genero": cancion.genero,
            "anio": cancion.anio,
            "duracion_seg": cancion.duracion,
        })
    return filas

def menu_archivos(catalogo, ruta_txt, ruta_bin, ruta_versiones):
    print()
    print("--- Guardar / cargar archivos ---")
    print("a) Cargar catálogo desde .txt")
    print("b) Guardar catálogo en .txt")
    print("c) Guardar catálogo en binario (.bin)")
    print("d) Cargar catálogo desde binario (.bin)")
    print("0) Volver")
    sub = input("> ").strip().lower()
    try:
        if sub == "a":
            catalogo = cargar_catalogo_musical(ruta_txt, ruta_versiones)
            guardar_todo(catalogo, ruta_txt, ruta_bin)
            print(f"Catálogo cargado: {catalogo.tamanio()} canciones.")

        elif sub == "b":
            guardar_texto(ruta_txt, filas_del_catalogo(catalogo), ENCABEZADOS)
            print("Catálogo guardado en data/catalogo.txt.")
        elif sub == "c":
            guardar_binario(ruta_bin, catalogo)
            print("Catálogo guardado en data/catalogo.bin.")
        elif sub == "d":
            canciones = cargar_binario(ruta_bin)
            nuevo = CatalogoMusical(canciones, [])
            nuevo.versiones_por_origen = catalogo.versiones_por_origen
            catalogo = nuevo
            guardar_todo(catalogo, ruta_txt, ruta_bin)
            print(f"Catálogo cargado desde .bin: {len(catalogo.canciones_por_id)} canciones.")
        elif sub != "0":
            print("Opción inválida.")
    except (ArchivoInvalidoError, OSError) as error:
        print(f"Archivo inválido: {error}")
    return catalogo

def reconstruir_catalogo(catalogo, canciones):
    nuevo_catalogo = CatalogoMusical(canciones, [])
    nuevo_catalogo.versiones_por_origen = catalogo.versiones_por_origen
    return nuevo_catalogo

def guardar_todo(catalogo, ruta_txt, ruta_bin):
    """Guarda el mismo catálogo en texto y binario."""
    guardar_texto(ruta_txt, filas_del_catalogo(catalogo), ENCABEZADOS)
    guardar_binario(ruta_bin, catalogo)

def posicion_del_id(catalogo, id_buscado):
    """Devuelve la posición del registro, contando desde cero."""
    for posicion, cancion in enumerate(catalogo):
        if cancion.id == id_buscado:
            return posicion
    raise ItemNoEncontradoError(f"No hay canción con ID {id_buscado}.")

def pedir_datos_cancion(cancion_anterior=None):
    def leer_texto(nombre, valor_actual, ancho):
        valor = input(f"{nombre} [{valor_actual}]: ").strip()
        valor = valor or str(valor_actual)

        if not valor or "," in valor:
            raise ValueError(f"{nombre}: ingresá texto sin comas.")

        if len(valor.encode("utf-8")) > ancho:
            raise ValueError(f"{nombre}: máximo {ancho} bytes UTF-8.")

        return valor

    def leer_entero(nombre, valor_actual, minimo, maximo):
        entrada = input(f"{nombre} [{valor_actual}]: ").strip()

        try:
            valor = int(entrada or str(valor_actual))
        except ValueError:
            raise ValueError(
                f"{nombre} debe ser un número entero."
            ) from None

        if valor < minimo or valor > maximo:
            raise ValueError(
                f"{nombre}: debe estar entre {minimo} y {maximo}."
            )

        return valor

    identificador = (
        cancion_anterior.id if cancion_anterior is not None
        else leer_entero("ID", "", 1, 4294967295)
    )

    return Cancion(
        identificador,
        leer_texto("Título", cancion_anterior.titulo if cancion_anterior else "", 40),
        leer_texto("Artista", cancion_anterior.artista if cancion_anterior else "", 40),
        leer_texto("Álbum", cancion_anterior.album if cancion_anterior else "", 40),
        leer_texto("Género", cancion_anterior.genero if cancion_anterior else "", 15),
        leer_entero("Año", cancion_anterior.anio if cancion_anterior else "", 0, 65535),
        leer_entero("Duración", cancion_anterior.duracion if cancion_anterior else "", 1, 65535),
    )


def menu_abm(catalogo, playlist, ruta_txt, ruta_bin):
    print("1) Alta  2) Baja  3) Modificar  4) Playlist  0) Volver")
    opcion = input("> ").strip()

    if opcion == "4":
        menu_playlist(playlist, catalogo)
        return catalogo

    if opcion == "0":
        return catalogo

    if opcion not in {"1", "2", "3"}:
        print("Opción inválida.")
        return catalogo

    try:
        canciones = list(catalogo)

        if opcion == "1":
            nueva_cancion = pedir_datos_cancion()

            if catalogo.obtener_cancion(nueva_cancion.id) is not None:
                raise ValueError("Ya existe una canción con ese ID.")

            alta_binario(ruta_bin, nueva_cancion)
            canciones.append(nueva_cancion)

        else:
            cancion = obtener_cancion(catalogo)

            if cancion is None:
                return catalogo

            posicion = posicion_del_id(catalogo, cancion.id)

            if opcion == "2":
                if catalogo.tamanio() == 1:
                    raise ValueError(
                        "El catálogo debe conservar al menos una canción."
                    )

                baja_binario(ruta_bin, posicion)
                del canciones[posicion]

            else:
                print("Enter conserva el valor actual. El ID se mantiene.")
                nueva_cancion = pedir_datos_cancion(cancion)

                actualizar_registro(ruta_bin, posicion, nueva_cancion)

                # Actualizamos el objeto que también pueden usar
                # la playlist, el historial y la cola.
                cancion.titulo = nueva_cancion.titulo
                cancion.artista = nueva_cancion.artista
                cancion.album = nueva_cancion.album
                cancion.genero = nueva_cancion.genero
                cancion.anio = nueva_cancion.anio
                cancion.duracion = nueva_cancion.duracion

        nuevo_catalogo = reconstruir_catalogo(catalogo, canciones)
        guardar_texto(
            ruta_txt,
            filas_del_catalogo(nuevo_catalogo),
            ENCABEZADOS,
        )

    except (ArchivoInvalidoError, ItemNoEncontradoError, ValueError, OSError) as error:
        print(f"No se pudo completar la operación: {error}")
        return catalogo

    print("Cambio guardado en texto y binario.")
    return nuevo_catalogo

def main():
    if TEMA not in TEMAS:
        print("Seteá TEMA en src/config.py: 'pokedex', 'recetario' o 'musica'.")
        return
    
    raiz = Path(__file__).resolve().parent.parent
    ruta_txt = raiz / "data" / "catalogo.txt"
    ruta_versiones = raiz / "data" / "versiones.csv"
    ruta_bin = raiz / "data" / "catalogo.bin"
    ruta_canciones = ruta_txt

    if not ruta_canciones.exists():
        ruta_canciones = raiz / "data" / "canciones.csv"

    try:
        catalogo = cargar_catalogo_musical(
            ruta_canciones,
            ruta_versiones,
        )
        guardar_todo(catalogo, ruta_txt, ruta_bin)
    except (ArchivoInvalidoError, OSError) as error:
        print(f"Archivo inválido: {error}")
        return
    
    playlist = Playlist()
    historial = HistorialReproduccion()
    cola = ColaReproduccion()
    canciones = list(catalogo.canciones_por_id.values())
    orden_actual = None

    opcion = None

    while opcion != "0":
        mostrar_menu()
        opcion = input("> ").strip()

        if opcion == "0":
            print("Chau.")

        elif opcion == "1":
            print("Catálogo de canciones")
            listar_catalogo(catalogo)

        elif opcion == "3":
            canciones, orden_actual = menu_buscar(canciones, orden_actual)
            catalogo = reconstruir_catalogo(catalogo, canciones)
            guardar_todo(catalogo, ruta_txt, ruta_bin)

        elif opcion == "4":
            canciones, orden_actual = menu_ordenar(canciones, orden_actual)
            catalogo = reconstruir_catalogo(catalogo, canciones)
            guardar_todo(catalogo, ruta_txt, ruta_bin)
        
        elif opcion == "5":
            cancion = obtener_cancion(catalogo)
            if cancion is None:
                continue
            print(f"Versiones derivadas de '{cancion.titulo}':")
            versiones_presentes = []

            for versiones in catalogo.versiones_por_origen.values():
                for version in versiones:
                    if (version.version_de_id in catalogo.canciones_por_id
                            and version.cancion_id in catalogo.canciones_por_id):
                        versiones_presentes.append(version)

            catalogo_versiones = CatalogoMusical(catalogo, versiones_presentes)
            derivadas = catalogo_versiones.listar_versiones(cancion.id)
            if not derivadas:
                print("No hay versiones derivadas.")

        elif opcion == "6":
            catalogo = menu_abm(catalogo, playlist, ruta_txt, ruta_bin)
            canciones = list(catalogo)
            orden_actual = None

        elif opcion == "7":
            menu_historial(historial, catalogo)

        elif opcion == "8":
            menu_cola(cola, historial, catalogo)

        elif opcion == "9":
            catalogo = menu_archivos(catalogo, ruta_txt, ruta_bin, ruta_versiones)
            canciones= list(catalogo.canciones_por_id.values())
            orden_actual = None

        elif opcion == "2":
            cancion = obtener_cancion(catalogo)
            if cancion is not None:
                print(cancion)

        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()

