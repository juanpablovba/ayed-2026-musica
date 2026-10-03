from src.tads.nodo import Nodo

class ListaEnlazada:
    def __init__(self):
        self._cabeza = None
        self._tamanio = 0

    def esta_vacia(self):
        return self._cabeza is None

    def tamanio(self):
        """Devuelve la cantidad de elementos de la lista."""
        return self._tamanio

    def insertar_al_inicio(self, dato):
        self._cabeza = Nodo(dato, self._cabeza)
        self._tamanio += 1

    def insertar_al_final(self, dato):
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self._cabeza = nuevo
        else:
            actual = self._cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self._tamanio += 1

    def insertar_ordenado(self, dato, clave):
        raise NotImplementedError("El método insertar_ordenado no está implementado.")

    def eliminar(self, dato):
        """Elimina la primera aparición del dato, si existe."""
        if self.esta_vacia():
            return
        if self._cabeza.dato == dato:
            self._cabeza = self._cabeza.siguiente
            self._tamanio -= 1
            return
        actual = self._cabeza
        while actual.siguiente is not None:
            if actual.siguiente.dato == dato:
                actual.siguiente = actual.siguiente.siguiente
                self._tamanio -= 1
                return
            actual = actual.siguiente

    def buscar(self, dato):
        """Devuelve el nodo que contiene el dato, o None si no existe."""
        actual = self._cabeza
        while actual is not None:
            if actual.dato == dato:
                return actual
            actual = actual.siguiente
        return None

    def __iter__(self):
        """Itera los datos desde la cabeza hasta el final."""
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente
