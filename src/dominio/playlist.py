from src.excepciones import ColeccionLlenaError
from src.tads.lista_enlazada import ListaEnlazada

class Playlist:
    """Colección ordenada de canciones con una capacidad máxima."""

    def __init__(self, tope=6):
        """Crea una playlist vacía con el tope indicado."""
        self._canciones = ListaEnlazada()
        self._tope = tope

    def agregar(self, cancion):
        """Agrega una canción si la playlist no alcanzó su tope."""
        if self._canciones.tamanio() >= self._tope:
            raise ColeccionLlenaError(f"La playlist está llena (máximo {self._tope}).")
        self._canciones.insertar_al_final(cancion)

    def eliminar(self, cancion):
        """Elimina una canción de la playlist si existe."""
        self._canciones.eliminar(cancion)

    def listar(self):
        """Muestra las canciones en el orden en que fueron agregadas."""
        for cancion in self._canciones:
            print(cancion)

    def esta_vacia(self):
        return self._canciones.esta_vacia()

    def tamanio(self):
        """Devuelve la cantidad de canciones de la playlist."""
        return self._canciones.tamanio()

    def __iter__(self):
        """Itera las canciones de la playlist."""
        return iter(self._canciones)