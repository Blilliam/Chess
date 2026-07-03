import os
import sys
import unittest
from types import SimpleNamespace

import pygame

pygame.init()
pygame.display.set_mode((1, 1))

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from GameObject import GameObject


class GameObjectSelectionTests(unittest.TestCase):
    def test_clicking_piece_selects_it_and_marks_moves(self):
        game = GameObject()

        game.handleClick(SimpleNamespace(pos=(0, 64)))

        self.assertIsNotNone(game.cPiece)
        self.assertTrue(game.cPiece.isSelected)
        self.assertTrue(game.mainBoard.board[2][0].isMoveable)

    def test_clicking_move_target_moves_selected_piece(self):
        game = GameObject()

        game.handleClick(SimpleNamespace(pos=(0, 64)))
        game.handleClick(SimpleNamespace(pos=(0, 128)))

        self.assertIsNone(game.mainBoard.board[1][0].piece)
        self.assertIsNotNone(game.mainBoard.board[2][0].piece)
        self.assertEqual(game.mainBoard.board[2][0].piece.x, 0)
        self.assertEqual(game.mainBoard.board[2][0].piece.y, 2)


if __name__ == "__main__":
    unittest.main()
