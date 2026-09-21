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
| ListaEnlazada |  |  |
| Pila |  |  |
| Cola |  |  |

Dónde se usa cada uno en el dominio.

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
