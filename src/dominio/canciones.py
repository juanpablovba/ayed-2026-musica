class Cancion:
    def __init__(self, id, titulo, artista, album, genero, anio, duracion_seg):
        self.id = id
        self.titulo = titulo
        self.artista = artista
        self.album = album
        self.genero = genero
        self.anio = anio
        self.duracion = duracion_seg

    def __str__(self):
        return f"{self.id} - {self.titulo} ({self.artista}) - {self.album} - {self.genero} - {self.anio} - {self.duracion} segundos"

catalogo = [
    Cancion(1, "Todavia una cancion de amor", "Los Rodriguez", "Palabras mas, palabras menos", "Rock", 1995, 298),
    Cancion(2, "A estos hombres tristes", "Almendra", "Almendra", "Rock", 1970, 356),
    Cancion(3, "Pensando en llegar", "Almafuerte", "Toro y pampa", "Rock", 2006, 207),
    Cancion(4, "Flight 956", "Indio Solari", "Porco Rex", "Rock", 2007, 307),
    Cancion(5, "Envuelto en llamas", "Los Gardelitos", "En tierra de sueños", "Rock", 2004, 230),
]

def listar_catalogo():
    for cancion in catalogo:
        print(cancion)