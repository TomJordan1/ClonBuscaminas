import pygame # Importar el módulo pygame
import os # Importar el módulo para manipular rutas






###COLORES (r, g, b)


WHITE = (255, 255, 255)
# Definir color blanco

BLACK = (0, 0, 0)
# Definir color negro

DARKGREY = (40, 40, 40)
# Definir color gris oscuro

LIGHTGREY = (100, 100, 100)
# Definir color gris claro

GREEN = (0, 255, 0)
# Definir color verde

DARKGREEN = (0, 200, 0)
# Definir color verde oscuro

BLUE = (0, 0, 255)
# Definir color azul

RED = (255, 0, 0)
# Definir color rojo

YELLOW = (255, 255, 0)
# Definir color amarillo

BGCOLOUR = DARKGREY
# Definir color de fondo del juego






###CONFIGURACIÓN DEL JUEGO


TILESIZE = 32
# Tamaño de cada casilla

ROWS = 20
# Número de filas en el tablero

COLS = 20
# Número de columnas en el tablero

AMOUNT_MINES = 15
# Cantidad de minas en el tablero

WIDTH = TILESIZE * ROWS
# Ancho de la pantalla del juego

HEIGHT = TILESIZE * COLS
# Altura de la pantalla del juego

FPS = 60
# Velocidad de fotogramas por segundo

TITLE = "Buscaminas"
# Título de la ventana del juego



# Validación de configuraciones
try:
    if WIDTH <= 0:
        raise ValueError("WIDTH debe ser mayor que 0.")
    if HEIGHT <= 0:
        raise ValueError("HEIGHT debe ser mayor que 0.")
    if TILESIZE <= 0:
        raise ValueError("TILESIZE debe ser mayor que 0.")
    if FPS <= 0:
        raise ValueError("FPS debe ser mayor que 0.")
    if ROWS <= 0:
        raise ValueError("ROWS debe ser mayor que 0.")
    if COLS <= 0:
        raise ValueError("COLS debe ser mayor que 0.")
    if AMOUNT_MINES <= 0:
        raise ValueError("AMOUNT_MINES debe ser mayor que 0.")
    if AMOUNT_MINES >= ROWS * COLS:
        raise ValueError("AMOUNT_MINES debe ser menor que el número total de casillas.")
except ValueError as ve:
    print(f"Error en las configuraciones: {ve}")




###


tile_numbers = []
# Lista para las imágenes de los números de pistas

for i in range(1, 9):
# Recorrer los números del 1 al 8

    tile_numbers.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", f"Tile{i}.png")), (TILESIZE, TILESIZE)))
    # Cargar y escalar las imágenes de los números de pistas

tile_empty = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileEmpty.png")), (TILESIZE, TILESIZE))
# Cargar y escalar la imagen de la casilla vacía

tile_exploded = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileExploded.png")), (TILESIZE, TILESIZE))
# Cargar y escalar la imagen de la mina explotada

tile_flag = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileFlag.png")), (TILESIZE, TILESIZE))
# Cargar y escalar la imagen de la bandera

tile_not_mine = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileNotMine.png")), (TILESIZE, TILESIZE))
# Cargar y escalar la imagen de la casilla sin mina

tile_unknown = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileUnknown.png")), (TILESIZE, TILESIZE))
# Cargar y escalar la imagen de la casilla sin abrir

tile_mine = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileMine.png")), (TILESIZE, TILESIZE))
# Cargar y escalar la imagen de la mina
