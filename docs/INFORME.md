# Informe del TP

Completar y hacer crecer en cada entrega. No hace falta prosa larga: oraciones claras y tablas.

## 1. Grupo y tema

- Tema: Biblioteca musical
- Por qué lo eligieron (5–8 líneas): Decidimos elegir la biblioteca musical como tema a desarrollar porque nos permitirá trabajar de manera clara los conceptos vistos en clase. La recursión, las pilas, las colas, la búsqueda y el ordenamiento podrán aplicarse dentro de un sistema de canciones, playlist y listas de reproducción. Al tratarse de un espacio de uso cotidiano, nos resulta más fácil imaginar casos de uso y nuevas funcionalidades para el sistema.

## 2. Modelo

Qué es un ítem del catálogo. Qué es mutable y qué no (E1). Cómo se relacionan catálogo, colección principal, pila y cola.

```text
Un ítem del catálogo es una canción. Cada canción se representa por la clase 'Cancion', la cual contiene los siguientes atributos: id, titulo, artista, album, genero, anio y duracion en segundos.
Aún no está decidido con certeza la mutabilidad/inmutabilidad de los objetos.
```

## 3. Recursión (E2)

Traza de un ejemplo real:

Llamada inicial: listar_versiones(1,0)

La canción con ID 1 es "De Musica Ligera"
Se buscar el ID 1 en versiones_por_origen
Se encuentra una versión:
    - cancion_id = 61
    - version_de_id = 1
    - tipo: live
Se muestra:
    - De Musica Ligera (Unplugged) | Soda Stereo | live

Se realiza la llamada recursiva: listar_versiones(61, 1)
La canción con ID 62 no tiene versiones derivadas.
-versiones- es una lista vacía.

Se cumple el caso base:
if nor versiones:
    return []

La llamada listar_versiones(62, 1) devuelve [].

La llamada inicial agrega la canción con ID 62 a la lista de derivadas y devuelve una lista con esa canción.

## 4. TADs (E3)

| TAD | Operaciones | Invariante |
| --- | --- | --- |
| ListaEnlazada | `esta_vacia`, `tamanio`, `insertar_al_inicio`, `insertar_al_final`, `insertar_ordenado`, `eliminar`, `buscar`, `__iter__` | `_cabeza` apunta al primer nodo o es `None` si la lista está vacía. `_tamanio` coincide con la cantidad de nodos alcanzables desde `_cabeza`. |
| Pila | `apilar`, `desapilar`, `ver_tope`, `esta_vacia` | La pila usa una `ListaEnlazada`. El tope siempre está en la cabeza de la lista, por lo que se respeta el orden LIFO. |
| Cola | `encolar`, `desencolar`, `ver_frente`, `esta_vacia` | La cola usa una `ListaEnlazada`. El frente siempre está en la cabeza; los nuevos elementos se agregan al final, por lo que se respeta el orden FIFO. |

- `ListaEnlazada` se usa internamente en `Playlist` para guardar canciones.
- `Pila` se usa en `HistorialReproduccion`: cada canción escuchada se apila y la última puede deshacerse primero.
- `Cola` se usa en `ColaReproduccion`: las canciones se agregan al final y se reproducen en el mismo orden en que fueron encoladas.
- La `Playlist` tiene un tope máximo de seis canciones. Al intentar superar ese límite, lanza `ColeccionLlenaError`.

## 5. Complejidad (E4)

| Operación | Tiempo | Espacio | Por qué |
| --- | --- | --- | --- |
|  |  |  |  |

Mediciones (`time.perf_counter`):

| Operación | n | segundos |
| --- | --- | --- |
|  |  |  |

## 6. Persistencia (E5)

- Layout del registro binario (campos, `struct`, anchos):
- Header:
- Cómo se actualiza un registro por posición:

## 7. Reparto de trabajo (E6)

| Integrante | Qué hizo | Qué puede defender |
| --- | --- | --- |
|  |  |  |
