# Entrega 4

def ordenar_seleccion(coleccion, clave):
    """Ordenamiento por selección. Devuelve una nueva secuencia, no usa sorted."""
    resultado = list(coleccion)
    for i in range(len(resultado) - 1):
        posicion_min = i
        for j in range(i + 1, len(resultado)):
            if clave(resultado[j]) < clave(resultado[posicion_min]):
                posicion_min = j
        resultado[i], resultado[posicion_min] = resultado[posicion_min], resultado[i]
    return resultado


def ordenar_insercion(coleccion, clave):
    """Ordenamiento por inserción. Devuelve una nueva secuencia, no usa sorted."""
    resultado = list(coleccion)
    for i in range(1, len(resultado)):
        actual = resultado[i]
        j = i - 1
        while j >=0 and clave(resultado[j]) > clave(actual):
            resultado[j + 1] = resultado[j]
            j -= 1
        resultado[j + 1] = actual
    return resultado

