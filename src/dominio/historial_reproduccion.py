from src.tads.pila import Pila

class HistorialReproduccion:
    """Historial de canciones escuchadas implementado como una pila."""

    def __init__(self):
        self._canciones = Pila()

    def registrar(self, cancion):
        """Registra una canción como la última reproducida."""
        self._canciones.apilar(cancion)

    def deshacer(self):
        """Quita y devuelve la última canción registrada."""
        return self._canciones.desapilar()

    def ver_ultima(self):
        """Devuelve la última canción registrada sin quitarla."""
        return self._canciones.ver_tope()

    def esta_vacio(self):
        return self._canciones.esta_vacia()