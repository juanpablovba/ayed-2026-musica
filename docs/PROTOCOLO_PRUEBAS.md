# Protocolo de pruebas

Pruebas **manuales**. Cada fila es un caso. Ejecutar sobre el tag que entregan.

Leyenda de resultado: `pasa` / `no pasa` / `no corrido`.

Mínimos: 8 casos escritos en E2; ejecutados en E3; 15 de regresión en E6 (pila, cola, archivos, recursión, búsquedas).

| ID | Entrega | Acción (pasos en el CLI) | Datos | Resultado esperado | Resultado | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| P01 | E1 | Arrancar el programa y listar catálogo | dataset de la cátedra | lista no vacía, sin traceback |  |  |
| P02 | E1 | Elegir un ítem inexistente | id = -1 | mensaje claro, el menú sigue |  |  |
| P03 | E2 | Elegir opción 5 e ingresar ID existente con versión live | id = 1 | Se lista De Musica Ligera como versión live | pasa |  |
| P04 | E2 | Elegir opción 5 e ingresar ID existente con versión cover | id = 31 | Se lista Black Space como versión cover | pasa |  |
| P05 | E2 | Elegir opción 5 e ingresar ID existente con versión remix | id = 51 | Se lista Billie Jean como versión remix | pasa | | 
| P06 | E2 | Elegir opción 5 e ingresar ID existente sin versiones | id = 2 | Se imprime que la canción no tiene versiones derivadas | pasa | caso base |
| P07 | E2 | Elegir opción 5 e ingresar ID no existente | id = 500 | Se imprime que no existe una canción con ese ID y vuelve al menú | pasa | |
| P08 | E2 | Elegir opción 5 e ingresar texto en lugar de un ID numérico | id = hola | Se imprime que el ID tiene que ser un número y vuelve al menú | pasa | 
| P09 | E2 | Elegir opción 5 e ingresar ID existente de una versión sin derivaciones | id = 62 | se imprime que no hay versiones derivadas y vuelve al menú | pasa | 
| P10 | E2 | Elegir opción 5 e ingresar ID existente con una versión de live distinta | id = 32 | Se lista Bohemian Rhapsody como versión live | pasa | 
| P11 | E3 | Agregar a la colección principal hasta el tope | agregar más de 6 IDs de canciones | el séptimo falla con excepción propia | pasa |  |
| P12 | E3 | Desapilar historial vacío | pila vacía | excepción propia, menú sigue | pasa |  |
| P13 | E3 | Desencolar cola vacía | cola vacía | excepción propia, menú sigue | pasa |  |
| P14 | E3 | Listar colección con el iterador | 2+ ítems | el orden coincide con las inserciones | pasa |  |
| P15 | E4 | Búsqueda lineal de un nombre que existe | titulo = De Musica Ligera | lo encuentra | pasa |  |
| P16 | E4 | Búsqueda lineal de un nombre que no existe | titulo = Cancion que no existe | no encontrado, sin traceback | pasa |  |
| P17 | E4 | Búsqueda binaria con catálogo desordenado | titulo = Bohemian Rhapsody | avisa o reordena; no da un falso hit | pasa | avisó que ordenó el catálogo y la encontró |
| P18 | E4 | Ordenar por un criterio y después por otro | titulo (selección) y año (inserción) | el orden cambia | pasa |  |
| P19 | E5 | Guardar CSV, salir, volver a entrar |  | los datos siguen |  |  |
| P20 | E5 | Guardar binario y modificar un registro por id |  | al recargar, ese campo cambió |  |  |
| P21 | E5 | Abrir un binario truncado o con magia mala | archivo basura | excepción de archivo inválido |  |  |
