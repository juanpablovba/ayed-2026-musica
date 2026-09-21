from pathlib import Path

from src.config import TEMA
from src.dominio.canciones import listar_catalogo
from src.dominio.versiones import cargar_catalogo_musical

TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}


def pendiente():
    print("Todavía no está implementado. Completar en la entrega que corresponde.")


def mostrar_menu():
    nombre = TEMAS.get(TEMA, TEMA or "(sin tema)")
    print()
    print(f"=== {nombre} — AyED C2 2026 ===")
    print("1. Listar catálogo")
    print("2. Ver detalle")
    print("3. Buscar")
    print("4. Ordenar")
    print("5. Operación recursiva")
    print("6. Colección principal (equipo / menú / playlist)")
    print("7. Historial (pila)")
    print("8. Cola")
    print("9. Guardar / cargar archivos")
    print("0. Salir")

def main():
    if TEMA not in TEMAS:
        print("Seteá TEMA en src/config.py: 'pokedex', 'recetario' o 'musica'.")
        return

    opcion = None

    raiz = Path(__file__).resolve().parent.parent

    catalogo = cargar_catalogo_musical(
        raiz / "data" / "canciones.csv",
        raiz / "data" / "versiones.csv"
    )

    while opcion != "0":
        mostrar_menu()
        opcion = input("> ").strip()
        if opcion == "0":
            print("Chau.")
        elif opcion == "1":
            listar_catalogo()
        elif opcion == "5":
            cancion_id = input("Ingrese el ID de la canción: ").strip()

            if not cancion_id.isdigit():
                print("ID inválido. Debe ser un número.")
                continue

            cancion = catalogo.obtener_cancion(cancion_id)

            if cancion is None:
                print(f"No se encontró la canción con ID {cancion_id}.")
                continue

            print(f"Versiones derivadas de '{cancion.titulo}':")
            derivadas = catalogo.listar_versiones(cancion_id)
            if not derivadas:
                print("No hay versiones derivadas.")

                
        elif opcion in {"2", "3", "4", "6", "7", "8", "9"}:
            pendiente()
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()

