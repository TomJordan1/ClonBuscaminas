import pygame  # Importar el módulo pygame
from settings import *  # Importar todas las configuraciones del archivo settings
from sprites import *  # Importar todas las clases y funciones del archivo sprites

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # Crear la pantalla del juego con las dimensiones especificadas
        
        pygame.display.set_caption(TITLE)
        # Establecer el título de la ventana del juego
        
        icon_path = os.path.join('assets', 'icon.png')
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
        # Cargar el icono desde la carpeta assets
        
        self.clock = pygame.time.Clock()
        # Crear un reloj para controlar la velocidad de actualización del juego
        
        self.font = pygame.font.Font(None, 36)
        # Fuente para el texto del botón
        
        self.wow_sound = pygame.mixer.Sound('wow.wav')
        # Cargar el sonido "wow"

    def new(self):
        self.board = Board()
        # Crear una nueva instancia del tablero
        
        self.board.display_board()
        # Mostrar el tablero en la pantalla

    def run(self):
        self.playing = True
        # Indicar que el juego está en marcha
        
        while self.playing:
            self.clock.tick(FPS)
            # Establecer la velocidad de fotogramas por segundo
        
            self.events()
            # Gestionar los eventos del juego
        
            self.draw()
            # Dibujar los elementos en la pantalla
        
        else:
            self.end_screen()
            # Mostrar la pantalla final si el juego ha terminado

    def draw(self):
        self.screen.fill(BGCOLOUR)
        # Rellenar la pantalla con el color de fondo
    
        self.board.draw(self.screen)
        # Dibujar el tablero en la pantalla
        
        pygame.display.flip()
        # Actualizar la pantalla

    def check_win(self):
        for row in self.board.board_list:
        # Recorrer cada fila del tablero
        
            for tile in row:
            # Recorrer cada casilla de la fila
        
                if tile.type != "X" and not tile.revealed:
                # Verificar si hay una casilla sin revelar que no sea una mina
        
                    return False
                # Si hay una casilla sin revelar, no hemos ganado
        
        return True
        # Si todas las casillas no minas están reveladas, hemos ganado

    def events(self):
        for event in pygame.event.get():
        # Gestionar los eventos de pygame
        
            if event.type == pygame.QUIT:
            # Si se cierra la ventana
        
                pygame.quit()
                # Cerrar pygame
                quit(0)
                # Salir del programa

            if event.type == pygame.MOUSEBUTTONDOWN:
            # Si se hace clic con el ratón
        
                mx, my = pygame.mouse.get_pos()
                # Obtener la posición del ratón
        
                mx //= TILESIZE
                # Convertir la posición en coordenadas de casilla
        
                my //= TILESIZE
                # Convertir la posición en coordenadas de casilla

                if event.button == 1:
                # Si se hace clic con el botón izquierdo
                
                    if not self.board.board_list[mx][my].flagged:
                    # Si la casilla no está marcada con una bandera
                    
                        if not self.board.dig(mx, my):
                        # Excavar la casilla y verificar si hay una mina
                        
                            pygame.mixer.music.load('perder.wav')
                            # Cargar el archivo de sonido de pérdida
                            
                            pygame.mixer.music.play()
                            # Reproducir el sonido de pérdida
                            
                            """ Si se ha hecho clic en una mina """
                            for row in self.board.board_list:
                            # Recorrer cada fila del tablero
                            
                                for tile in row:
                                # Recorrer cada casilla de la fila
                                
                                    if tile.flagged and tile.type != "X":
                                    # Si la casilla está marcada y no es una mina
                                    
                                        tile.flagged = False
                                        # Quitar la bandera
                                        
                                        tile.revealed = True
                                        # Revelar la casilla
                                        
                                        tile.image = tile_not_mine
                                        # Mostrar la imagen de casilla sin mina
                                        
                                    elif tile.type == "X":
                                    # Si la casilla es una mina
                                    
                                        tile.revealed = True
                                        # Revelar la mina
                                        
                            self.playing = False
                            # Terminar el juego
                            
                        else:
                            self.wow_sound.play()
                            # Reproducir el sonido "wow" si no es una mina

                if event.button == 3:
                # Si se hace clic con el botón derecho
                    
                    if not self.board.board_list[mx][my].revealed:
                        # Si la casilla no está revelada
                        
                        self.board.board_list[mx][my].flagged = not self.board.board_list[mx][my].flagged
                        # Marcar o desmarcar la casilla con una bandera

                if self.check_win():
                # Verificar si hemos ganado
                    
                    pygame.mixer.music.load('ganar.wav')
                    # Cargar el archivo de sonido de victoria
                    
                    pygame.mixer.music.play()
                    # Reproducir el sonido de victoria
                    
                    self.win = True
                    # Indicar que hemos ganado
                    
                    self.playing = False
                    # Terminar el juego
                    
                    for row in self.board.board_list:
                    # Recorrer cada fila del tablero
                    
                        for tile in row:
                        # Recorrer cada casilla de la fila
                        
                            if not tile.revealed:
                            # Si la casilla no está revelada
                            
                                tile.flagged = True
                                # Marcar la casilla con una bandera

    def end_screen(self):
        button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
        # Definir las dimensiones y posición del botón
        
        while pygame.mixer.music.get_busy():
            pygame.time.delay(100)
            # Esperar a que termine el sonido
        
        while True:
            for event in pygame.event.get():
            # Gestionar los eventos de pygame
                if event.type == pygame.QUIT:
                # Si se cierra la ventana
                    pygame.quit()
                    # Cerrar pygame
                    quit(0)
                    # Salir del programa

                if event.type == pygame.MOUSEBUTTONDOWN:
                # Si se hace clic con el ratón
                
                    if button_rect.collidepoint(event.pos):
                        # Si se hace clic en el botón
                        
                        return
                        # Volver al inicio del juego

            self.screen.fill(BGCOLOUR)
            # Rellenar la pantalla con el color de fondo
            
            pygame.draw.rect(self.screen, (0, 255, 0), button_rect)
            # Dibujar el botón en la pantalla
            
            text = self.font.render("Reiniciar :(", True, (255, 255, 255))
            # Crear el texto del botón
            
            text_rect = text.get_rect(center=button_rect.center)
            # Centrarse el texto en el botón
            
            self.screen.blit(text, text_rect)
            # Dibujar el texto en la pantalla
            
            pygame.display.flip()
            # Actualizar la pantalla

game = Game()
# Crear una instancia del juego

while True:
    game.new()
    # Iniciar un nuevo juego
    
    game.run()
    # Ejecutar el juego
    
