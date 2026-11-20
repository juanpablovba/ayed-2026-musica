# Informe del TP

## 1. Grupo y tema

- Tema: Biblioteca musical
- Desarrollo realizado por: Camila Rondon y Juan Pablo Villalba.
- Decidimos elegir la biblioteca musical como tema a desarrollar porque nos permitirá trabajar de manera clara los conceptos vistos en clase. La recursión, las pilas, las colas, la búsqueda y el ordenamiento podrán aplicarse dentro de un sistema de canciones, playlist y listas de reproducción. Al tratarse de un espacio de uso cotidiano, nos resulta más fácil imaginar casos de uso y nuevas funcionalidades para el sistema.

## 2. Modelo

Un ítem del catálogo es una canción. Cada canción se representa por la clase 'Cancion', la cual contiene los siguientes atributos: id, titulo, artista, album, genero, anio y duracion en segundos.
La clase Cancion es mutable: el ABM modifica título, artista, álbum, género, año y duración, manteniendo el ID estable. Las cadenas y los enteros son inmutables; cambiar un atributo reasigna su valor. Las colecciones utilizadas, como listas y diccionarios, son mutables.

## 3. Recursión (E2)

Traza de un ejemplo real:

Llamada inicial: listar_versiones(1)
La canción con ID 1 es "De Música Ligera"

Se buscar el ID 1 en versiones_por_origen
Se encuentra una versión:
    - cancion_id = 62
    - version_de_id = 1
    - tipo: "live"

Se muestra:
    - De Musica Ligera (Unplugged) | Soda Stereo | live

Se realiza la llamada recursiva: listar_versiones(62)
La canción con ID 62 no tiene versiones derivadas.
-versiones- es una lista vacía.

Se cumple el caso base:
if not versiones:
    return []

La llamada listar_versiones(62) devuelve [].

La llamada inicial agrega la canción con ID 62 a la lista de derivadas y devuelve una lista con esa canción.

## 4. TADs (E3)

| TAD | Operaciones | Invariante |
| --- | --- | --- |
| ListaEnlazada | `esta_vacia`, `tamanio`, `insertar_al_inicio`, `insertar_al_final`, `insertar_ordenado`, `eliminar`, `buscar`, `__iter__` | `_cabeza` apunta al primer nodo o es `None` si la lista está vacía. `_tamanio` coincide con la cantidad de nodos alcanzables desde `_cabeza`. |
| Pila | `apilar`, `desapilar`, `ver_tope`, `esta_vacia` | La pila usa una `ListaEnlazada`. El tope siempre está en la cabeza de la lista, por lo que se respeta el orden LIFO. |
| Cola | `encolar`, `desencolar`, `ver_frente`, `esta_vacia` | La cola usa una `ListaEnlazada`. El frente siempre está en la cabeza; los nuevos elementos se agregan al final, por lo que se respeta el orden FIFO. |

- `ListaEnlazada` se usa en `CatalogoMusical` para almacenar el catálogo y en `Playlist` para guardar las canciones seleccionadas.
- `Pila` se usa en `HistorialReproduccion`: cada canción escuchada se apila y la última puede deshacerse primero.
- `Cola` se usa en `ColaReproduccion`: las canciones se agregan al final y se reproducen en el mismo orden en que fueron encoladas.
- La `Playlist` tiene un tope máximo de seis canciones. Al intentar superar ese límite, lanza `ColeccionLlenaError`.

## 5. Complejidad (E4)

| Operación | Tiempo | Espacio | Por qué |
| --- | --- | --- | --- |
| Listar catálogo | O(n) | O(1) | Recorre las n canciones una vez. |
| Ver detalle por ID | O(1) | O(1) | Acceso directo al diccionario por id. |
| Búsqueda lineal | O(n) | O(1) | Compara de a una; en el peor caso mira todas. |
| Búsqueda binaria | O(log n) | O(1) | Cada paso descarta la mitad (requiere lista ordenada). |
| Ordenar por selección | O(n²) | O(n) | Dos bucles anidados, siempre ~n²/2 comparaciones. Trabaja sobre una copia. |
| Ordenar por inserción | O(n) mejor / O(n²) peor | O(n) | Si ya está ordenada compara una vez por elemento; si está al revés, desplaza todo. Trabaja sobre una copia. |

Mediciones (`time.perf_counter`), con el dataset original y una copia agrandada (se repiten las filas). Las búsquedas se miden en el peor caso - Entrega 4

| Operación | n | segundos |
| --- | --- | --- |
| búsqueda lineal | 67 | 0.000021 |
| búsqueda lineal | 3350 | 0.001148 |
| búsqueda binaria | 67 | 0.000003 |
| búsqueda binaria | 3350 | 0.000005 |
| ordenar por selección | 67 | 0.001894 |
| ordenar por selección | 3350 | 2.635739 |
| ordenar por inserción | 67 | 0.000728 |
| ordenar por inserción | 3350 | 1.587905 |

Con 50 veces más canciones, la búsqueda lineal tarda unas 55 veces más (crece como n), la binaria casi no cambia (log n) y los ordenamientos tardan miles de veces más (n²).


## 6. Persistencia (E5)

El catálogo se guarda en `data/catalogo.txt` y `data/catalogo.bin`.
Las relaciones de versiones se leen desde `data/versiones.csv`.

Al arrancar se carga `catalogo.txt`. Si todavía no existe, se utiliza
`canciones.csv`. Después se guardan ambos formatos.

### Texto simple

Se utiliza UTF-8, con encabezado y un registro por línea.
Los campos se separan por comas. Al cargar se valida que cada registro
tenga la misma cantidad de campos que el encabezado.

### Header binario

Formato: `struct.Struct("<4s 1s I")`. Tamaño: 9 bytes.

| Campo | Tipo | Tamaño | Contenido |
| --- | --- | --- | --- |
| Magia | 4s | 4 bytes | AYED |
| Tema | 1s | 1 byte | M |
| Cantidad | I | 4 bytes | Número de registros |

### Registro binario

Formato: `struct.Struct("<I 40s 40s 40s 15s 2H")`.
Cada registro ocupa 143 bytes.

| Campo | Tipo | Tamaño |
| --- | --- | --- |
| ID | I | 4 bytes |
| Título | 40s | 40 bytes |
| Artista | 40s | 40 bytes |
| Álbum | 40s | 40 bytes |
| Género | 15s | 15 bytes |
| Año | H | 2 bytes |
| Duración en segundos | H | 2 bytes |

El prefijo `<` establece little endian y evita alineación automática.
Las cadenas se codifican en UTF-8 y se recortan o rellenan con `\x00`
hasta alcanzar el ancho fijo. El ingreso desde el ABM rechaza cadenas
que excedan esos anchos.

### Actualización y ABM persistente

La posición se cuenta desde cero. El desplazamiento se calcula como:

`HEADER.size + posicion * FORMATO.size`, equivalente a `9 + posicion * 143`.

`actualizar_registro` abre con `r+b`, utiliza `seek` y escribe únicamente
el registro elegido. Esa escritura es O(1), una vez conocida la posición.
Buscar la posición por ID requiere O(n).

El alta agrega al final y actualiza la cantidad del header.
La baja reescribe el archivo sin el registro eliminado: O(n).
Después de cada ABM se guarda el catálogo completo en texto.

Después de cargar u ordenar se guardan ambos formatos, manteniendo
el mismo orden en memoria y en el binario.

### Archivos inválidos

Se utiliza `ArchivoInvalidoError` para archivos inexistentes, cabeceras
incompletas, magia o tema incorrectos, registros binarios incompletos
y líneas de texto con una cantidad incorrecta de campos.

El menú 9 captura la excepción, muestra el mensaje y conserva
el catálogo anterior cuando falla una carga.

## 7. Reparto de trabajo (E6)

El desarrollo fue realizado por Camila Rondon y Juan Pablo Villalba.

| Integrante | Aportes |
| --- | --- |
| Camila Rondon | Búsquedas, ordenamientos, mediciones, protocolo de pruebas y primeras implementaciones de persistencia de texto y binario. |
| Juan Pablo Villalba | Modelo y recursión, integración de los TADs, playlist, historial, cola, ABM persistente y revisión de documentación. |
