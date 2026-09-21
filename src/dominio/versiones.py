from src.dominio.canciones import Cancion
from src.persistencia.texto import cargar_csv 

class Version:
    def __init__(self, cancion_id, version_de_id, tipo):
        self.cancion_id = cancion_id
        self.version_de_id = version_de_id
        self.tipo = tipo

class CatalogoMusical:
    def __init__(self, canciones, versiones):
        self.canciones_por_id = {cancion.id: cancion for cancion in canciones}
        self.versiones_por_origen = {}

        for version in versiones:
            if version.version_de_id not in self.versiones_por_origen:
                self.versiones_por_origen[version.version_de_id] = []
            self.versiones_por_origen[version.version_de_id].append(version)

    def obtener_cancion(self, cancion_id):
        return self.canciones_por_id.get(cancion_id)

    def listar_versiones (self, cancion_id):
        versiones = self.versiones_por_origen.get(cancion_id, [])

        if not versiones:
            return []

        derivadas = []

        for version in versiones:
            cancion = self.obtener_cancion(version.cancion_id)
            print(f"- {cancion.titulo} | {cancion.artista} | {version.tipo}")
            derivadas.append(cancion)
            derivadas.extend(self.listar_versiones(cancion.id))

        return derivadas

def cargar_catalogo_musical(ruta_canciones, ruta_versiones):
    filas_canciones = cargar_csv(ruta_canciones)
    filas_versiones = cargar_csv(ruta_versiones)

    canciones = [
            Cancion(
                fila["id"],
                fila["titulo"],
                fila["artista"],
                fila["album"],
                fila["genero"],
                fila["anio"],
                fila["duracion_seg"]
            )
            for fila in filas_canciones
        ]

    versiones = [
        Version(
            fila["cancion_id"],
            fila["version_de_id"],
            fila["tipo"]
        )
        for fila in filas_versiones
        ]

    return CatalogoMusical(canciones, versiones)