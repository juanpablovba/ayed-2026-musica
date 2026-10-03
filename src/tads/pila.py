from src.excepciones import PilaVaciaError
from src.tads.lista_enlazada import ListaEnlazada

class Pila:
    """Pila implementada sobre una lista enlazada."""

    def __init__(self):
        """Crea una pila vacía."""
        self._items = ListaEnlazada()

    def apilar(self, dato):
        """Agrega un dato al tope de la pila."""
        self._items.insertar_al_inicio(dato)

    def desapilar(self):
        """Quita y devuelve el tope de la pila."""
        if self.esta_vacia():
            raise PilaVaciaError("No hay elementos para deshacer.")
        tope = self.ver_tope()
        self._items.eliminar(tope)
        return tope

    def ver_tope(self):
        """Devuelve el tope sin quitarlo."""
        if self.esta_vacia():
            raise PilaVaciaError("La pila está vacía.")
        return self._items._cabeza.dato

    def esta_vacia(self):
        return self._items.esta_vacia()
