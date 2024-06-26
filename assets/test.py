import unittest
from sprites import Board, Tile
from settings import *

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_place_mines(self):
        """
        Prueba que la cantidad de minas colocadas sea la esperada.
        """
        mines = sum(1 for row in self.board.board_list for tile in row if tile.type == "X")
        self.assertEqual(mines, AMOUNT_MINES, f"Se esperaban {AMOUNT_MINES} minas, pero se encontraron {mines}.")
        print("Listo test_place_mines.")

    def test_clues(self):
        """
        Prueba que las pistas (números) se coloquen correctamente.
        """
        for x in range(ROWS):
            for y in range(COLS):
                if self.board.board_list[x][y].type == "C":
                    expected_clues = self.board.check_neighbours(x, y)
                    image_clues = tile_numbers.index(self.board.board_list[x][y].image) + 1
                    self.assertEqual(expected_clues, image_clues, f"Se esperaban {expected_clues} pistas, pero se encontraron {image_clues}.")
        print("Listo test_clues.")

    def test_dig_mine(self):
        """
        Prueba que excavar una mina devuelve False.
        """
        for x in range(ROWS):
            for y in range(COLS):
                if self.board.board_list[x][y].type == "X":
                    result = self.board.dig(x, y)
                    self.assertFalse(result, "Excavar una mina debería devolver False.")
                    print("Listo test_dig_mine.")
                    break

    def test_dig_safe(self):
        """
        Prueba que excavar una casilla segura devuelve True.
        """
        for x in range(ROWS):
            for y in range(COLS):
                if self.board.board_list[x][y].type == ".":
                    result = self.board.dig(x, y)
                    self.assertTrue(result, "Excavar una casilla segura debería devolver True.")
                    print("Listo test_dig_safe.")
                    break

if __name__ == "__main__":
    unittest.main()

