import pygame  # Importar el módulo pygame
import logging  # Importar el módulo logging para el log de errores
from settings import *  # Importar todas las configuraciones del archivo settings
from sprites import *  # Importar todas las clases y funciones del archivo sprites

# Configurar el sistema de log
logging.basicConfig(level=logging.ERROR, filename='game_errors.log', 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Game:
    def __init__(self):
        """
        Inicializa el juego, configurando la pantalla, el icono, el reloj, la fuente y los sonidos.
        """
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Configura la pantalla del juego
            pygame.display.set_caption(TITLE)  # Establece el título de la ventana
            icon_path = os.path.join('assets', 'icon.png')
            icon = pygame.image.load(icon_path)  # Carga el icono del juego
            pygame.display.set_icon(icon)  # Establece el icono de la ventana
            self.clock = pygame.time.Clock()  # Inicializa el reloj para controlar la velocidad del juego
            self.font = pygame.font.Font(None, 36)  # Inicializa la fuente de texto
            self.wow_sound = pygame.mixer.Sound('wow.wav')  # Carga el sonido "wow"
        except Exception as e:
            logging.error("Error en la inicialización del juego", exc_info=True)  # Registra el error
            raise e

    def new(self):
        """
        Inicia un nuevo juego creando un nuevo tablero y mostrándolo en la pantalla.
        """
        try:
            self.board = Board()  # Crea un nuevo tablero
            self.board.display_board()  # Muestra el tablero en la pantalla
        except Exception as e:
            logging.error("Error al crear un nuevo juego", exc_info=True)  # Registra el error
            raise e

    def run(self):
        """
        Corre el bucle principal del juego.
        """
        self.playing = True
        try:
            while self.playing:
                self.clock.tick(FPS)  # Controla la velocidad del bucle del juego
                self.events()  # Maneja los eventos del juego
                self.draw()  # Dibuja los elementos en la pantalla
            else:
                self.end_screen()  # Muestra la pantalla final
        except Exception as e:
            logging.error("Error durante la ejecución del juego", exc_info=True)  # Registra el error
            raise e

    def draw(self):
        """
        Dibuja los elementos del juego en la pantalla.
        """
        try:
            self.screen.fill(BGCOLOUR)  # Rellena la pantalla con el color de fondo
            self.board.draw(self.screen)  # Dibuja el tablero en la pantalla
            pygame.display.flip()  # Actualiza la pantalla
        except Exception as e:
            logging.error("Error al dibujar en la pantalla", exc_info=True)  # Registra el error
            raise e

    def check_win(self):
        """
        Verifica si el jugador ha ganado el juego.

        Returns:
            bool: True si todas las casillas no-mina están reveladas, False de lo contrario.
        """
        try:
            for row in self.board.board_list:  # Recorre cada fila del tablero
                for tile in row:  # Recorre cada casilla de la fila
                    if tile.type != "X" and not tile.revealed:
                        return False  # Si hay una casilla no revelada que no es mina, el jugador no ha ganado
            return True  # Si todas las casillas no-mina están reveladas, el jugador ha ganado
        except Exception as e:
            logging.error("Error al verificar la condición de victoria", exc_info=True)  # Registra el error
            raise e

    def events(self):
        """
        Maneja los eventos del juego.
        """
        try:
            for event in pygame.event.get():  # Recorre todos los eventos
                if event.type == pygame.QUIT:  # Si el evento es de salida
                    pygame.quit() # Cerrar pygame
                    quit(0) # Salir del programa

                    
                if event.type == pygame.MOUSEBUTTONDOWN:  # Si se presiona un botón del mouse
                    mx, my = pygame.mouse.get_pos()  # Obtener la posición del ratón
                    mx //= TILESIZE  # Convertir la posición en coordenadas de casilla
                    my //= TILESIZE # Convertir la posición en coordenadas de casilla

                    if event.button == 1:  # Si se presiona el botón izquierdo
                        if not self.board.board_list[mx][my].flagged:  # Si la casilla no está marcada con bandera
                            if not self.board.dig(mx, my):  # Si excavar la casilla devuelve False (es una mina)
                                pygame.mixer.music.load('perder.wav') # Cargar el archivo de sonido de pérdida
                                pygame.mixer.music.play()# Reproducir el sonido de pérdida
                                for row in self.board.board_list:   # Recorrer cada fila del tablero
                                    for tile in row:# Recorrer cada casilla de la fila
                                        if tile.flagged and tile.type != "X": # Si la casilla está marcada y no es una mina
                                            tile.flagged = False  # Quitar la bandera
                                            tile.revealed = True # Revelar la casilla
                                            tile.image = tile_not_mine # Mostrar la imagen de casilla sin mina
                                        elif tile.type == "X": # Si la casilla es una mina
                                            tile.revealed = True  # Revelar la mina
                                self.playing = False  # Terminar el juego
                            else:
                                self.wow_sound.play()  # Reproduce el sonido "wow"


                    if event.button == 3:  # Si se presiona el botón derecho
                        if not self.board.board_list[mx][my].revealed:  # Si la casilla no está revelada
                            self.board.board_list[mx][my].flagged = not self.board.board_list[mx][my].flagged  # Cambia el estado de bandera


                    if self.check_win():  # Si se cumple la condición de victoria
                        pygame.mixer.music.load('ganar.wav')  # Cargar el archivo de sonido de victoria
                        pygame.mixer.music.play()# Reproducir el sonido de victoria
                        self.win = True  # Indicar que hemos ganado
                        self.playing = False # Terminar el juego

                        # Marca todas las casillas no reveladas con banderas
                        for row in self.board.board_list:  # Recorrer cada fila del tablero
                            for tile in row:  # Recorrer cada casilla de la fila
                                if not tile.revealed: # Verificar que la casilla no está revelada
                                    tile.flagged = True # Revelar la casilla
        except Exception as e:
            logging.error("Error durante el manejo de eventos", exc_info=True)  # Registra el error
            raise e

    def end_screen(self):
        """
        Muestra la pantalla final cuando el juego termina.
        """
        button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50) # Definir las dimensiones y posición del botón
        try:
            while pygame.mixer.music.get_busy():  # Espera a que termine la música
                pygame.time.delay(100)  # Esperar a que termine el sonido
            while True:
                for event in pygame.event.get():  # Recorre todos los eventos
                    if event.type == pygame.QUIT:  # Si el evento es de salida
                        pygame.quit() # Cerrar pygame
                        quit(0) # Salir del programa
                    if event.type == pygame.MOUSEBUTTONDOWN:  # Si se presiona un botón del mouse
                        if button_rect.collidepoint(event.pos):  # Si se presiona el botón de reiniciar
                            return
                self.screen.fill(BGCOLOUR)  # Rellena la pantalla con el color de fondo
                pygame.draw.rect(self.screen, (0, 255, 0), button_rect)  # Dibuja el botón de reiniciar
                text = self.font.render("Reiniciar :(", True, (255, 255, 255))  # Renderiza el texto del botón
                text_rect = text.get_rect(center=button_rect.center)  # Calcula la posición del texto
                self.screen.blit(text, text_rect)  # Dibuja el texto en la pantalla
                pygame.display.flip()  # Actualiza la pantalla
        except Exception as e:
            logging.error("Error durante la pantalla final", exc_info=True)  # Registra el error
            raise e

game = Game()

while True:
    try:
        game.new()  # Inicia un nuevo juego
        game.run()  # Corre el bucle principal del juego
    except Exception as e:
        logging.critical("Error crítico en el bucle principal del juego", exc_info=True)  # Registra el error crítico
        break


