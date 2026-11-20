# TP integrador — AyED C2 2026

## Integrantes

| Nombre              | Mail                       | GitHub                  |
| ---                 | ---                        | ---                     | 
| Camila Rondon       | rondoncordova321@gmail.com | github.com/CamiRondon   |
| Juan Pablo Villalba | juanpablovba@gmail.com     | github.com/juanpablovba |

**Tema elegido:** Biblioteca musical 

## Cómo ejecutar

Desde la raíz del repo, con Python 3.10 o superior:

```text
python -m src.main
```

En Windows, si `python` no anda: `py -3 -m src.main`.

Solo biblioteca estándar. No hay `requirements.txt` a propósito.

## Qué hace

Gestor de una biblioteca musical por consola. Permite:

1. Listar el catálogo mediante el iterador de la lista enlazada.
2. Consultar una canción por ID.
3. Buscar por título mediante búsqueda lineal o binaria.
4. Ordenar por título, artista, año o duración, usando selección o inserción.
5. Consultar versiones derivadas mediante recursión.
6. Realizar altas, bajas y modificaciones persistentes y gestionar una playlist.
7. Registrar y deshacer reproducciones mediante una pila.
8. Gestionar canciones pendientes mediante una cola FIFO.
9. Guardar y cargar texto y binario con registros de longitud fija.
10. Salir del programa.

## Limitaciones conocidas

- Se gestionan datos de canciones; no se reproducen archivos de audio.
- La playlist, el historial y la cola se mantienen solamente durante la ejecución.
- Las búsquedas ignoran mayúsculas y minúsculas, pero distinguen tildes.
- Los campos de texto ingresados desde el ABM no admiten comas y tienen los límites de tamaño documentados en el informe.

## Entregas

Cada vencimiento se marca con un tag. Ver `GIT.md`.

| Tag | Vence |
| --- | --- |
| `preentrega` (opcional, solo repo) | domingo 30-ago-2026 23:59 |
| `entrega-1` | domingo 06-sep-2026 23:59 |
| `entrega-2` | domingo 20-sep-2026 23:59 |
| `entrega-3` | domingo 04-oct-2026 23:59 |
| `entrega-4` | domingo 01-nov-2026 23:59 |
| `entrega-5` | domingo 15-nov-2026 23:59 |
| `entrega-6` | domingo 22-nov-2026 23:59 |

Defensa oral (reemplaza el 2do parcial): 25 y 27-nov-2026.

La cátedra corrige el **tag**, no el último commit suelto de `main`.

El grupo se avisa por mail a diego.ambrossio@unab.edu.ar **y** angel.bianco@unab.edu.ar. Ver `GIT.md`.
