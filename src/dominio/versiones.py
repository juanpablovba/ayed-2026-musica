from src.dominio.canciones import Cancion
from src.persistencia.texto import cargar_texto
from src.tads.lista_enlazada import ListaEnlazada


class Version:
    def __init__(self, cancion_id, version_de_id, tipo):
        self.cancion_id = cancion_id
        self.version_de_id = version_de_id
        self.tipo = tipo


class CatalogoMusical:
    """Agrupa canciones y sus relaciones de versiones derivadas."""

    def __init__(self, canciones, versiones):
        if isinstance(canciones, ListaEnlazada):
            self._canciones = canciones
        else:
            self._canciones = ListaEnlazada()

            for cancion in canciones:
                self._canciones.insertar_al_final(cancion)

        self.canciones_por_id = {
            cancion.id: cancion
            for cancion in self._canciones
        }

        self.versiones_por_origen = {}

        for version in versiones:
            if version.version_de_id not in self.versiones_por_origen:
                self.versiones_por_origen[version.version_de_id] = []

            self.versiones_por_origen[version.version_de_id].append(
                version
            )

    def __iter__(self):
        """Permite recorrer el catálogo mediante su lista enlazada."""
        return iter(self._canciones)

    def tamanio(self):
        """Devuelve la cantidad de canciones del catálogo."""
        return self._canciones.tamanio()

    def obtener_cancion(self, cancion_id):
        """Devuelve una canción por su ID, o None si no existe."""
        return self.canciones_por_id.get(cancion_id)

    def listar_versiones(self, cancion_id):
        """Muestra y devuelve las versiones derivadas de una canción."""
        versiones = self.versiones_por_origen.get(cancion_id, [])

        if not versiones:
            return []

        derivadas = []

        for version in versiones:
            cancion = self.obtener_cancion(version.cancion_id)

            print(
                f"- {cancion.titulo} | "
                f"{cancion.artista} | {version.tipo}"
            )

            derivadas.append(cancion)
            derivadas.extend(self.listar_versiones(cancion.id))

        return derivadas


def armar_catalogo_desde_txt(ruta):
    """Lee el .txt y devuelve la ListaEnlazada con objetos del dominio."""
    catalogo = ListaEnlazada()

    for fila in cargar_texto(ruta):
        cancion = Cancion(
            id=int(fila["id"]),
            titulo=fila["titulo"],
            artista=fila["artista"],
            album=fila["album"],
            genero=fila["genero"],
            anio=int(fila["anio"]),
            duracion_seg=int(fila["duracion_seg"]),
        )

        catalogo.insertar_al_final(cancion)

    return catalogo


def cargar_catalogo_musical(ruta_canciones, ruta_versiones):
    """Carga canciones y versiones y crea el catálogo musical."""
    canciones = armar_catalogo_desde_txt(ruta_canciones)

    versiones = []

    for fila in cargar_texto(ruta_versiones):
        version = Version(
            cancion_id=int(fila["cancion_id"]),
            version_de_id=int(fila["version_de_id"]),
            tipo=fila["tipo"],
        )

        versiones.append(version)

    return CatalogoMusical(canciones, versiones)