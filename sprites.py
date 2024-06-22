import random # Importar el módulo random para la generación de números aleatorios

import pygame # Importar el módulo pygame para la creación del juego

from settings import * # Importar todas las configuraciones del archivo settings

# Lista de tipos
    # "." -> desconocido
    # "X" -> mina
    # "C" -> pista



### Representa una casilla en el tablero

class Tile:
    def __init__(self, x, y, image, type, revealed=False, flagged=False):
        self.x, self.y = x * TILESIZE, y * TILESIZE
        # Coordenadas de la casilla multiplicadas por el tamaño de la casilla
        
        self.image = image
        # Imagen de la casilla
        
        self.type = type
        # Tipo de la casilla (mina, pista, etc.)
        
        self.revealed = revealed
        # Indica si la casilla está revelada
        
        self.flagged = flagged
        # Indica si la casilla está marcada con una bandera

    def draw(self, board_surface):
        if not self.flagged and self.revealed:
        # Si la casilla no está marcada y está revelada
            
            board_surface.blit(self.image, (self.x, self.y))
            # Dibujar la imagen de la casilla en la superficie del tablero
            
        elif self.flagged and not self.revealed:
        # Si la casilla está marcada y no está revelada
        
            board_surface.blit(tile_flag, (self.x, self.y))
            # Dibujar la imagen de bandera en la casilla
            
        elif not self.revealed:
        # Si la casilla no está revelada
        
            board_surface.blit(tile_unknown, (self.x, self.y))
            # Dibujar la imagen de casilla desconocida

    def __repr__(self):
        return self.type
        # Representar la casilla por su tipo


### Representa el tablero de juego

class Board:
    def __init__(self):
        self.board_surface = pygame.Surface((WIDTH, HEIGHT))
        # Crear una superficie para el tablero
        
        self.board_list = [[Tile(col, row, tile_empty, ".") for row in range(ROWS)] for col in range(COLS)]
        # Crear una lista de listas que representa el tablero con casillas vacías
        
        self.place_mines()
        # Colocar las minas en el tablero
        
        self.place_clues()
        # Colocar las pistas en el tablero
        
        self.dug = []
        # Lista de casillas excavadas

    def place_mines(self):
        for _ in range(AMOUNT_MINES):
        # Colocar la cantidad de minas especificadas
        
            while True:
                x = random.randint(0, ROWS-1)
                # Generar una coordenada aleatoria para la fila
                
                y = random.randint(0, COLS-1)
                # Generar una coordenada aleatoria para la columna

                if self.board_list[x][y].type == ".":
                # Verificar si la casilla está vacía
                
                    self.board_list[x][y].image = tile_mine
                    # Asignar la imagen de la mina a la casilla
                    
                    self.board_list[x][y].type = "X"
                    # Cambiar el tipo de la casilla a mina
                    
                    break
                    # Salir del bucle una vez colocada la mina

    def place_clues(self):
        for x in range(ROWS):
        # Recorrer todas las filas
        
            for y in range(COLS):
            # Recorrer todas las columnas
            
                if self.board_list[x][y].type != "X":
                # Verificar si la casilla no es una mina
                
                    total_mines = self.check_neighbours(x, y)
                    # Contar las minas en las casillas vecinas
                    
                    if total_mines > 0:
                    # Si hay al menos una mina en las casillas vecinas
                    
                        self.board_list[x][y].image = tile_numbers[total_mines-1]
                        # Asignar la imagen correspondiente al número de minas vecinas
                        
                        self.board_list[x][y].type = "C"
                        # Cambiar el tipo de la casilla a pista

    @staticmethod
    def is_inside(x, y):
        return 0 <= x < ROWS and 0 <= y < COLS
        # Verificar si las coordenadas están dentro del tablero

    def check_neighbours(self, x, y):
        total_mines = 0
        # Inicializar el contador de minas vecinas
        
        for x_offset in range(-1, 2):
            # Recorrer las filas vecinas
            
            for y_offset in range(-1, 2):
                # Recorrer las columnas vecinas
                
                neighbour_x = x + x_offset
                # Calcular la coordenada de la fila vecina
                
                neighbour_y = y + y_offset
                # Calcular la coordenada de la columna vecina
                
                if self.is_inside(neighbour_x, neighbour_y) and self.board_list[neighbour_x][neighbour_y].type == "X":  # Verificar si la casilla vecina es una mina
                    total_mines += 1
                    # Incrementar el contador de minas vecinas

        return total_mines
        # Devolver el número total de minas vecinas

    def draw(self, screen):
        for row in self.board_list:
            # Recorrer todas las filas del tablero
            
            for tile in row:
                # Recorrer todas las casillas de la fila
                
                tile.draw(self.board_surface)
                # Dibujar cada casilla en la superficie del tablero
                
        screen.blit(self.board_surface, (0, 0))
        # Dibujar la superficie del tablero en la pantalla

    def dig(self, x, y):
        self.dug.append((x, y))
        # Añadir la casilla a la lista de excavadas
        
        if self.board_list[x][y].type == "X":
            # Si la casilla es una mina
            
            self.board_list[x][y].revealed = True
            # Revelar la casilla
            
            self.board_list[x][y].image = tile_exploded
            # Cambiar la imagen a mina explotada
            
            return False
            # Devolver False indicando que se ha hecho clic en una mina
            
        elif self.board_list[x][y].type == "C":
        # Si la casilla es una pista
        
            self.board_list[x][y].revealed = True
            # Revelar la casilla
            
            return True
            # Devolver True indicando que la excavación fue segura

        self.board_list[x][y].revealed = True
        # Revelar la casilla

        for row in range(max(0, x-1), min(ROWS-1, x+1) + 1):
        # Recorrer las filas vecinas
        
            for col in range(max(0, y-1), min(COLS-1, y+1) + 1):
            # Recorrer las columnas vecinas
            
                if (row, col) not in self.dug:
                # Si la casilla vecina no ha sido excavada
                
                    self.dig(row, col)
                    # Excavar la casilla vecina
                    
        return True
        # Devolver True indicando que la excavación fue segura

    def display_board(self):
        for row in self.board_list:
        # Recorrer todas las filas del tablero
            
            print(row)
            # Imprimir cada fila del tablero
