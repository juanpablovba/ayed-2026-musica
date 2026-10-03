from src.tads.cola import Cola

class ColaReproduccion:
    """Cola de canciones pendientes de reproducción."""

    def __init__(self):
        self._canciones = Cola()

    def agregar(self, cancion):
        """Agrega una canción al final de la cola."""
        self._canciones.encolar(cancion)

    def reproducir_siguiente(self):
        """Quita y devuelve la próxima canción a reproducir."""
        return self._canciones.desencolar()

    def ver_proxima(self):
        """Devuelve la próxima canción sin quitarla."""
        return self._canciones.ver_frente()

    def esta_vacia(self):
        """Devuelve True si no hay canciones pendientes."""
        return self._canciones.esta_vacia()