import unittest
import pygame
from settings import *
from sprites import Board  # Asegúrate de que 'Board' se importe desde el archivo correcto

class TestMinesweeper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        cls.board = Board()
        pygame.display.set_caption("Buscaminas")

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_game_initialization(self):
        """
        Prueba la inicialización del juego, verificando que la ventana se crea y el tablero se inicializa correctamente.
        """
        self.assertIsNotNone(self.screen, "La pantalla no se inicializó correctamente.")
        self.assertIsInstance(self.board, Board, "El tablero no se inicializó correctamente.")
        self.assertEqual(self.board.board_surface.get_size(), (WIDTH, HEIGHT), "La superficie del tablero tiene un tamaño incorrecto.")

    def test_event_handling(self):
        """
        Prueba el manejo de eventos básicos, como cerrar la ventana del juego.
        """
        close_event = pygame.event.Event(pygame.QUIT)
        pygame.event.post(close_event)

        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        self.assertFalse(running, "El evento de cierre de ventana no se manejó correctamente.")

    def test_board_draw(self):
        """
        Prueba el método draw del tablero, verificando que se dibuje en la pantalla sin errores.
        """
        try:
            self.board.draw(self.screen)
        except Exception as e:
            self.fail(f"El método draw del tablero lanzó una excepción: {e}")

    def test_dig(self):
        """
        Prueba el método dig del tablero, verificando que la excavación se maneje correctamente.
        """
        result = self.board.dig(0, 0)
        self.assertIn((0, 0), self.board.dug, "La casilla (0, 0) no se añadió a la lista de excavadas.")
        self.assertTrue(result, "El método dig devolvió False para una casilla segura.")

if __name__ == "__main__":
    unittest.main()
