def busqueda_lineal(coleccion, clave, obtener_clave):
    """Devuelve el ítem cuya clave coincide, o None."""
    for elemento in coleccion:
        if obtener_clave(elemento) == clave:
            return elemento
    return None
        

def busqueda_binaria(coleccion_ordenada, clave, obtener_clave):
    """La colección tiene que estar ordenada por obtener_clave."""
    raise NotImplementedError
